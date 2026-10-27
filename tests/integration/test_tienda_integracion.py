"""
Pruebas de integración: modelos reales + servicio TiendaMuebles + datos de main.py.
"""

import io
from unittest.mock import patch

import pytest
from rich.console import Console

import main
from models.categorias.asientos import Asiento
from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sofacama import SofaCama
from services.tienda import TiendaMuebles
from ui.menu import MenuTienda

pytestmark = pytest.mark.integration


@pytest.fixture
def tienda_demo(capsys):
    """Tienda cargada con el catálogo de ejemplo de main.py."""
    tienda = TiendaMuebles("Demo")
    main.crear_catalogo_inicial(tienda)
    main.crear_comedores_ejemplo(tienda)
    main.aplicar_descuentos_ejemplo(tienda)
    capsys.readouterr()  # descartar los prints de arranque
    return tienda


class TestCatalogoDeEjemplo:
    def test_carga_completa(self, tienda_demo):
        stats = tienda_demo.obtener_estadisticas()
        assert stats["total_muebles"] == 17
        assert stats["total_comedores"] == 2
        assert stats["tipos_muebles"]["Silla"] == 3
        assert stats["tipos_muebles"]["SofaCama"] == 1

    def test_valor_inventario_incluye_comedores(self, tienda_demo):
        valor_muebles = tienda_demo.obtener_estadisticas()["valor_inventario"]
        valor_comedores = sum(c.calcular_precio_total() for c in tienda_demo._comedores)
        assert tienda_demo.calcular_valor_inventario() == pytest.approx(
            valor_muebles + valor_comedores
        )

    def test_polimorfismo_todos_calculan_precio_y_descripcion(self, tienda_demo):
        for mueble in tienda_demo._inventario:
            assert mueble.calcular_precio() > 0
            assert mueble.nombre in mueble.obtener_descripcion()

    def test_busqueda_por_tipo_respeta_herencia(self, tienda_demo):
        asientos = tienda_demo.obtener_muebles_por_tipo(Asiento)
        # 3 sillas + 1 sillón + 2 sofás + 1 sofá-cama
        assert len(asientos) == 7


class TestFlujoDeVenta:
    def test_venta_con_descuento_de_categoria(self, tienda_demo):
        silla = tienda_demo.buscar_muebles_por_nombre("Silla Clásica")[0]
        precio = silla.calcular_precio()

        venta = tienda_demo.realizar_venta(silla, "Laura")

        assert venta["precio_final"] == pytest.approx(precio * 0.9)
        assert silla not in tienda_demo._inventario
        stats = tienda_demo.obtener_estadisticas()
        assert stats["total_muebles"] == 16
        assert stats["ventas_realizadas"] == 1
        assert stats["valor_total_ventas"] == pytest.approx(venta["precio_final"])

    def test_no_se_puede_vender_dos_veces(self, tienda_demo):
        silla = tienda_demo.buscar_muebles_por_nombre("Silla Clásica")[0]
        tienda_demo.realizar_venta(silla)
        assert "error" in tienda_demo.realizar_venta(silla)

    def test_descuento_por_material_afecta_precio_de_venta(self, tienda_vacia_real):
        silla = Silla("Silla Roble", "Roble", "Natural", 100.0, tiene_respaldo=False)
        tienda_vacia_real.agregar_mueble(silla)
        tienda_vacia_real.aplicar_descuento_material("Roble", 0.2)
        assert tienda_vacia_real.realizar_venta(silla)["precio_final"] == pytest.approx(
            80.0
        )


class TestComedorYSofaCama:
    def test_comedor_en_tienda(self, tienda_vacia_real):
        mesa = Mesa("Mesa", "Roble", "Natural", 200.0, capacidad_personas=6)
        comedor = Comedor("Set", mesa)
        for i in range(6):
            comedor.agregar_silla(Silla(f"S{i}", "Roble", "Natural", 50.0))
        assert comedor.agregar_silla(
            Silla("Extra", "Roble", "Natural", 50.0)
        ).startswith("No se pueden")
        tienda_vacia_real.agregar_comedor(comedor)
        esperado = (mesa.calcular_precio() + 6 * 55.0) * 0.95
        assert tienda_vacia_real.calcular_valor_inventario() == pytest.approx(
            esperado, abs=0.01
        )

    def test_sofacama_venta_y_conversion(self, tienda_vacia_real):
        sc = SofaCama("SC", "Tela", "Gris", 1000.0)
        tienda_vacia_real.agregar_mueble(sc)
        sc.convertir_a_cama()
        assert "modo: cama" in str(sc)
        tienda_vacia_real.aplicar_descuento("sofacama", 10)
        venta = tienda_vacia_real.realizar_venta(sc)
        assert venta["descuento"] == pytest.approx(10.0)
        assert venta["precio_final"] == pytest.approx(2000.0 * 0.9)


@pytest.mark.slow
class TestSesionDeMenu:
    def test_sesion_completa(self, tienda_demo, tmp_path):
        """Simula una sesión de usuario: catálogo, venta, reporte guardado y salida."""
        menu = MenuTienda(tienda_demo)
        menu.console = Console(file=io.StringIO(), width=200, color_system=None)
        archivo = tmp_path / "reporte.txt"

        with (
            patch("ui.menu.time.sleep"),
            patch("builtins.input", return_value=""),
            patch("ui.menu.IntPrompt.ask", side_effect=[1, 6, 1, 8, 0]),
            patch("ui.menu.Confirm.ask", side_effect=[True, True]),
            patch("ui.menu.Prompt.ask", side_effect=["Carlos", str(archivo)]),
        ):
            menu.ejecutar()

        texto = menu.console.file.getvalue()
        assert "Catálogo de Muebles" in texto
        assert "Cliente: Carlos" in texto
        assert "Total de muebles: 16" in archivo.read_text(encoding="utf-8")
        assert tienda_demo.obtener_estadisticas()["ventas_realizadas"] == 1


@pytest.fixture
def tienda_vacia_real():
    return TiendaMuebles("Integración")
