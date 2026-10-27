import re
from unittest.mock import Mock, patch

import pytest

from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sofa import Sofa
from services.tienda import TiendaMuebles


def mueble_que_falla():
    mock = Mock(spec=Silla)
    mock.nombre = "Roto"
    mock.material = "Madera"
    mock.calcular_precio.side_effect = RuntimeError("precio roto")
    return mock


class TestConstruccion:
    def test_nombre_por_defecto(self):
        assert TiendaMuebles().nombre == "Mueblería OOP"

    def test_nombre_personalizado(self, tienda_vacia):
        assert tienda_vacia.nombre == "Tienda Test"

    def test_inicia_vacia(self, tienda_vacia):
        assert tienda_vacia._inventario == []
        assert tienda_vacia._comedores == []
        assert tienda_vacia._ventas_realizadas == []
        assert tienda_vacia._descuentos_activos == {}


class TestAgregar:
    def test_agregar_mueble(self, tienda_vacia, mueble_mock):
        mensaje = tienda_vacia.agregar_mueble(mueble_mock)
        assert mensaje == "Mueble Mueble Mock agregado exitosamente al inventario"
        assert tienda_vacia._inventario == [mueble_mock]
        mueble_mock.calcular_precio.assert_called_once()

    def test_agregar_none(self, tienda_vacia):
        assert tienda_vacia.agregar_mueble(None) == "Error: El mueble no puede ser None"

    @pytest.mark.parametrize("precio", [0, -10])
    def test_agregar_precio_invalido(self, tienda_vacia, mueble_mock, precio):
        mueble_mock.calcular_precio.return_value = precio
        assert "precio válido" in tienda_vacia.agregar_mueble(mueble_mock)
        assert tienda_vacia._inventario == []

    def test_agregar_error_al_calcular_precio(self, tienda_vacia):
        mensaje = tienda_vacia.agregar_mueble(mueble_que_falla())
        assert mensaje == "Error al calcular precio del mueble: precio roto"
        assert tienda_vacia._inventario == []

    def test_agregar_comedor(self, tienda_vacia, comedor_basico):
        assert tienda_vacia.agregar_comedor(comedor_basico) == (
            "Comedor Comedor Familiar agregado exitosamente"
        )
        assert tienda_vacia._comedores == [comedor_basico]

    def test_agregar_comedor_none(self, tienda_vacia):
        assert tienda_vacia.agregar_comedor(None).startswith("Error")


class TestBusquedasYFiltros:
    @pytest.mark.parametrize("termino", ["silla", "SILLA", "  Sil  ", "básica"])
    def test_buscar_por_nombre(self, tienda_con_inventario, termino):
        resultados = tienda_con_inventario.buscar_muebles_por_nombre(termino)
        assert [m.nombre for m in resultados] == ["Silla Básica"]

    @pytest.mark.parametrize("termino", ["", "   ", None])
    def test_buscar_vacio(self, tienda_con_inventario, termino):
        assert tienda_con_inventario.buscar_muebles_por_nombre(termino) == []

    def test_buscar_sin_coincidencias(self, tienda_con_inventario):
        assert tienda_con_inventario.buscar_muebles_por_nombre("lámpara") == []

    def test_filtrar_por_precio_inclusivo(self, tienda_con_inventario):
        # Silla 110, Mesa 209.6, Sofá 1350
        resultados = tienda_con_inventario.filtrar_por_precio(110, 209.6)
        assert [m.nombre for m in resultados] == ["Silla Básica", "Mesa Comedor"]

    def test_filtrar_por_precio_sin_limites(self, tienda_con_inventario):
        assert len(tienda_con_inventario.filtrar_por_precio()) == 3

    def test_filtrar_por_precio_minimo_negativo(self, tienda_con_inventario):
        assert len(tienda_con_inventario.filtrar_por_precio(-100, 200)) == 1

    def test_filtrar_por_precio_ignora_errores(self, tienda_con_inventario):
        tienda_con_inventario._inventario.append(mueble_que_falla())
        assert len(tienda_con_inventario.filtrar_por_precio()) == 3

    @pytest.mark.parametrize("material", ["Madera", "madera", "  MADERA "])
    def test_filtrar_por_material(self, tienda_con_inventario, material):
        resultados = tienda_con_inventario.filtrar_por_material(material)
        assert {m.nombre for m in resultados} == {"Silla Básica", "Sofá Familiar"}

    @pytest.mark.parametrize("material", ["", "  ", None])
    def test_filtrar_por_material_vacio(self, tienda_con_inventario, material):
        assert tienda_con_inventario.filtrar_por_material(material) == []

    def test_filtrar_por_material_ignora_invalidos(self, tienda_vacia, silla_basica):
        sin_material = Mock(material=None)
        material_no_texto = Mock(material=123)
        tienda_vacia._inventario.extend([sin_material, material_no_texto, silla_basica])
        assert tienda_vacia.filtrar_por_material("madera") == [silla_basica]


class TestDescuentos:
    @pytest.mark.parametrize(
        "categoria,clave",
        [
            ("silla", "Silla"),
            ("Sillas", "Silla"),
            (" mesas ", "Mesa"),
            ("SOFA", "Sofa"),
        ],
    )
    def test_normaliza_categoria(self, tienda_vacia, categoria, clave):
        tienda_vacia.aplicar_descuento(categoria, 10)
        assert tienda_vacia._descuentos_activos == {clave: 0.10}

    def test_mensaje(self, tienda_vacia):
        assert tienda_vacia.aplicar_descuento("silla", 25) == (
            "Descuento del 25% aplicado a la categoría 'Silla'"
        )

    @pytest.mark.parametrize("porcentaje", [0, -5, 101])
    def test_porcentaje_invalido(self, tienda_vacia, porcentaje):
        assert tienda_vacia.aplicar_descuento("silla", porcentaje).startswith("Error")
        assert tienda_vacia._descuentos_activos == {}

    def test_porcentaje_limite_100(self, tienda_vacia):
        tienda_vacia.aplicar_descuento("mesa", 100)
        assert tienda_vacia._descuentos_activos["Mesa"] == 1.0


class TestVentas:
    def test_venta_sin_descuento(self, tienda_con_inventario, silla_basica):
        venta = tienda_con_inventario.realizar_venta(silla_basica, "Ana")
        assert venta["mueble"] == "Silla Básica"
        assert venta["cliente"] == "Ana"
        assert venta["precio_original"] == pytest.approx(110.0)
        assert venta["descuento"] == 0
        assert venta["precio_final"] == pytest.approx(110.0)
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", venta["fecha"])

    def test_venta_actualiza_estado(self, tienda_con_inventario, silla_basica):
        tienda_con_inventario.realizar_venta(silla_basica)
        assert silla_basica not in tienda_con_inventario._inventario
        assert len(tienda_con_inventario._ventas_realizadas) == 1
        assert tienda_con_inventario._total_muebles_vendidos == 1
        assert tienda_con_inventario._valor_total_ventas == pytest.approx(110.0)

    def test_venta_cliente_por_defecto(self, tienda_con_inventario, silla_basica):
        assert (
            tienda_con_inventario.realizar_venta(silla_basica)["cliente"]
            == "Cliente Anónimo"
        )

    def test_venta_con_descuento(self, tienda_con_inventario, silla_basica):
        tienda_con_inventario.aplicar_descuento("sillas", 10)
        venta = tienda_con_inventario.realizar_venta(silla_basica)
        assert venta["descuento"] == pytest.approx(10.0)
        assert venta["precio_final"] == pytest.approx(99.0)

    def test_descuento_clase_con_mayusculas_internas(self, tienda_vacia):
        from models.concretos.sofacama import SofaCama

        sc = SofaCama("SC", "Tela", "Gris", 1000.0)
        tienda_vacia.agregar_mueble(sc)
        tienda_vacia.aplicar_descuento("sofacamas", 20)
        assert tienda_vacia.realizar_venta(sc)["precio_final"] == pytest.approx(1600.0)

    def test_descuento_de_otra_categoria_no_aplica(
        self, tienda_con_inventario, silla_basica
    ):
        tienda_con_inventario.aplicar_descuento("mesa", 50)
        assert tienda_con_inventario.realizar_venta(silla_basica)["descuento"] == 0

    def test_venta_mueble_no_disponible(self, tienda_vacia, silla_basica):
        resultado = tienda_vacia.realizar_venta(silla_basica)
        assert resultado == {"error": "El mueble no está disponible en inventario"}

    def test_venta_mueble_sin_nombre_usa_tipo(
        self, tienda_con_inventario, silla_basica
    ):
        silla_basica._nombre = ""
        assert tienda_con_inventario.realizar_venta(silla_basica)["mueble"] == "Silla"

    def test_venta_error_al_calcular(self, tienda_vacia, mueble_mock):
        tienda_vacia.agregar_mueble(mueble_mock)
        mueble_mock.calcular_precio.side_effect = RuntimeError("falla")
        resultado = tienda_vacia.realizar_venta(mueble_mock)
        assert resultado == {"error": "Error al procesar la venta: falla"}
        assert mueble_mock in tienda_vacia._inventario


class TestEstadisticas:
    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_tienda_vacia(self, tienda_vacia, metodo):
        stats = getattr(tienda_vacia, metodo)()
        assert stats["total_muebles"] == 0
        assert stats["valor_inventario"] == 0
        assert stats["tipos_muebles"] == {}

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_con_inventario(
        self, tienda_con_inventario, comedor_basico, metodo
    ):
        tienda_con_inventario.agregar_comedor(comedor_basico)
        tienda_con_inventario.aplicar_descuento("silla", 10)
        stats = getattr(tienda_con_inventario, metodo)()
        assert stats["total_muebles"] == 3
        assert stats["total_comedores"] == 1
        assert stats["valor_inventario"] == pytest.approx(110 + 209.6 + 1350)
        assert stats["tipos_muebles"] == {"Silla": 1, "Mesa": 1, "Sofa": 1}
        assert stats["descuentos_activos"] == {"Silla": 0.1}

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_descuentos_es_copia(self, tienda_vacia, metodo):
        getattr(tienda_vacia, metodo)()["descuentos_activos"]["X"] = 1
        assert tienda_vacia._descuentos_activos == {}

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_acumulan_ventas(
        self, tienda_con_inventario, silla_basica, metodo
    ):
        tienda_con_inventario.realizar_venta(silla_basica)
        stats = getattr(tienda_con_inventario, metodo)()
        assert stats["ventas_realizadas"] == 1
        assert stats["total_muebles_vendidos"] == 1
        assert stats["valor_total_ventas"] == pytest.approx(110.0)

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_ignora_muebles_con_error(self, tienda_con_inventario, metodo):
        tienda_con_inventario._inventario.append(mueble_que_falla())
        stats = getattr(tienda_con_inventario, metodo)()
        assert stats["total_muebles"] == 4
        assert stats["valor_inventario"] == pytest.approx(110 + 209.6 + 1350)

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_sin_atributos_opcionales(self, tienda_vacia, metodo):
        del tienda_vacia._ventas_realizadas
        stats = getattr(tienda_vacia, metodo)()
        assert stats["ventas_realizadas"] == 0

    @pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
    def test_estadisticas_estado_corrupto_devuelve_valores_vacios(
        self, tienda_vacia, metodo
    ):
        tienda_vacia._inventario = None
        stats = getattr(tienda_vacia, metodo)()
        assert stats["total_muebles"] == 0
        assert stats["valor_total_ventas"] == 0.0


class TestReporte:
    def test_reporte_basico(self, tienda_con_inventario):
        reporte = tienda_con_inventario.generar_reporte_inventario()
        assert reporte.startswith("=== REPORTE DE INVENTARIO - Tienda Test ===")
        assert "Total de muebles: 3" in reporte
        assert "Valor total del inventario: $1669.60" in reporte
        assert "- Silla: 1 unidades" in reporte
        assert "DESCUENTOS ACTIVOS" not in reporte

    def test_reporte_con_descuentos(self, tienda_con_inventario):
        tienda_con_inventario.aplicar_descuento("mesa", 15)
        reporte = tienda_con_inventario.generar_reporte_inventario()
        assert "DESCUENTOS ACTIVOS:" in reporte
        assert "- Mesa: 15.0%" in reporte

    @pytest.mark.parametrize("valor_invalido", [None, "no es dict", []])
    def test_reporte_tolera_estadisticas_invalidas(self, tienda_vacia, valor_invalido):
        with patch.object(
            tienda_vacia, "obtener_estadisticas", return_value=valor_invalido
        ):
            reporte = tienda_vacia.generar_reporte_inventario()
        assert "Total de muebles: 0" in reporte
        assert "Valor total del inventario: $0.00" in reporte


# ---------------------------------------------------------------------------
# Funcionalidades nuevas desarrolladas con TDD (Red -> Green -> Refactor)
# ---------------------------------------------------------------------------


class TestObtenerMueblesPorTipo:
    def test_filtra_por_clase(self, tienda_con_inventario, silla_basica):
        assert tienda_con_inventario.obtener_muebles_por_tipo(Silla) == [silla_basica]

    def test_incluye_subclases(self, tienda_con_inventario):
        from models.categorias.asientos import Asiento

        tipos = {
            type(m) for m in tienda_con_inventario.obtener_muebles_por_tipo(Asiento)
        }
        assert tipos == {Silla, Sofa}

    def test_sin_coincidencias(self, tienda_vacia):
        assert tienda_vacia.obtener_muebles_por_tipo(Mesa) == []


class TestCalcularValorInventario:
    def test_tienda_vacia(self, tienda_vacia):
        assert tienda_vacia.calcular_valor_inventario() == 0

    def test_suma_muebles_y_comedores(self, tienda_con_inventario, comedor_basico):
        tienda_con_inventario.agregar_comedor(comedor_basico)
        esperado = 110 + 209.6 + 1350 + comedor_basico.calcular_precio_total()
        assert tienda_con_inventario.calcular_valor_inventario() == pytest.approx(
            esperado
        )

    def test_ignora_elementos_con_error(self, tienda_con_inventario):
        tienda_con_inventario._inventario.append(mueble_que_falla())
        comedor_roto = Mock()
        comedor_roto.calcular_precio_total.side_effect = RuntimeError
        tienda_con_inventario._comedores.append(comedor_roto)
        assert tienda_con_inventario.calcular_valor_inventario() == pytest.approx(
            1669.6
        )


class TestContarTiposMuebles:
    def test_tienda_vacia(self, tienda_vacia):
        assert tienda_vacia._contar_tipos_muebles() == {}

    def test_conteo(self, tienda_con_inventario):
        tienda_con_inventario.agregar_mueble(Silla("Otra", "Metal", "Negro", 50.0))
        assert tienda_con_inventario._contar_tipos_muebles() == {
            "Silla": 2,
            "Mesa": 1,
            "Sofa": 1,
        }


class TestAplicarDescuentoMaterial:
    def test_aplicar_descuento_por_material(self, tienda_vacia):
        silla = Silla("Silla", "Roble", "Natural", 100.0)
        tienda_vacia.agregar_mueble(silla)
        tienda_vacia.aplicar_descuento_material("Roble", 0.1)  # 10% descuento
        assert silla.precio_base == pytest.approx(90.0)

    def test_solo_afecta_al_material_indicado(
        self, tienda_con_inventario, mesa_basica, silla_basica
    ):
        # Mesa básica es de Roble, silla básica de Madera
        mensaje = tienda_con_inventario.aplicar_descuento_material("roble", 0.5)
        assert mesa_basica.precio_base == pytest.approx(100.0)
        assert silla_basica.precio_base == pytest.approx(100.0)
        assert mensaje == "Descuento del 50% aplicado a 1 mueble(s) de material 'roble'"

    @pytest.mark.parametrize("porcentaje", [0, -0.1, 1, 1.5])
    def test_porcentaje_invalido(self, tienda_con_inventario, silla_basica, porcentaje):
        mensaje = tienda_con_inventario.aplicar_descuento_material("Madera", porcentaje)
        assert mensaje.startswith("Error")
        assert silla_basica.precio_base == 100.0
