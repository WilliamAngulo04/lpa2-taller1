"""
Pruebas para models.composicion.comedor (composición mesa + sillas).
"""

from unittest.mock import Mock

import pytest

from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def mesa_mock():
    mesa = Mock(spec=Mesa)
    mesa.calcular_precio.return_value = 200.0
    mesa.obtener_descripcion.return_value = "Mesa Mock"
    mesa.material = "Roble"
    mesa.capacidad_personas = 6
    return mesa


def sillas_mock(cantidad, precio=50.0):
    sillas = []
    for i in range(cantidad):
        silla = Mock(spec=Silla)
        silla.nombre = f"Silla {i + 1}"
        silla.material = "Roble"
        silla.material_tapizado = None
        silla.calcular_precio.return_value = precio
        silla.obtener_descripcion.return_value = f"Silla Mock {i + 1}"
        sillas.append(silla)
    return sillas


class TestComposicion:
    def test_composicion_correcta(self, comedor_basico):
        assert comedor_basico.nombre == "Comedor Familiar"
        assert isinstance(comedor_basico.mesa, Mesa)
        assert len(comedor_basico.sillas) == 4
        assert all(isinstance(s, Silla) for s in comedor_basico.sillas)

    def test_sin_sillas_por_defecto(self, mesa_mock):
        assert Comedor("Vacío", mesa_mock).sillas == []

    def test_sillas_devuelve_copia(self, comedor_basico):
        comedor_basico.sillas.clear()
        assert len(comedor_basico.sillas) == 4

    def test_len_y_str(self, comedor_basico):
        assert len(comedor_basico) == 5
        assert str(comedor_basico) == "Comedor Comedor Familiar: Mesa + 4 sillas"


class TestPrecio:
    def test_sin_descuento_menos_de_4_sillas(self, mesa_mock):
        comedor = Comedor("C", mesa_mock, sillas_mock(3))
        assert comedor.calcular_precio_total() == 350.0

    def test_descuento_con_4_o_mas_sillas(self, mesa_mock):
        comedor = Comedor("C", mesa_mock, sillas_mock(6))
        assert comedor.calcular_precio_total() == pytest.approx((200 + 6 * 50) * 0.95)

    def test_precio_con_objetos_reales(
        self, comedor_basico, mesa_basica, sillas_comedor
    ):
        esperado = mesa_basica.calcular_precio() + sum(
            s.calcular_precio() for s in sillas_comedor
        )
        assert comedor_basico.calcular_precio_total() == pytest.approx(esperado * 0.95)


class TestAgregarQuitar:
    def test_agregar_silla_a_comedor_vacio(self, mesa_mock, silla_basica):
        comedor = Comedor("C", mesa_mock)
        mensaje = comedor.agregar_silla(silla_basica)
        assert mensaje == "Silla Silla Básica agregada exitosamente al comedor"
        assert len(comedor.sillas) == 1

    def test_agregar_tipo_incorrecto(self, mesa_basica, silla_basica):
        comedor = Comedor("C", mesa_basica, [silla_basica])
        assert comedor.agregar_silla("no soy silla").startswith("Error")
        assert len(comedor.sillas) == 1

    def test_agregar_supera_capacidad(self, mesa_basica, sillas_comedor, silla_basica):
        # La mesa básica admite 4 personas
        comedor = Comedor("C", mesa_basica, sillas_comedor)
        assert "Capacidad máxima: 4" in comedor.agregar_silla(silla_basica)

    def test_capacidad_por_defecto_si_mesa_no_la_define(self, silla_basica):
        class MesaSinCapacidad:
            pass

        comedor = Comedor("C", MesaSinCapacidad(), [silla_basica] * 6)
        assert "Capacidad máxima: 6" in comedor.agregar_silla(silla_basica)

    def test_quitar_sin_sillas(self, mesa_mock):
        assert Comedor("C", mesa_mock).quitar_silla() == "No hay sillas para quitar"

    def test_quitar_ultima_por_defecto(self, mesa_mock):
        comedor = Comedor("C", mesa_mock, sillas_mock(2))
        assert comedor.quitar_silla() == "Silla Silla 2 removida del comedor"
        assert len(comedor.sillas) == 1

    def test_quitar_por_indice(self, mesa_mock):
        comedor = Comedor("C", mesa_mock, sillas_mock(3))
        assert comedor.quitar_silla(0) == "Silla Silla 1 removida del comedor"

    def test_quitar_indice_invalido(self, mesa_mock):
        comedor = Comedor("C", mesa_mock, sillas_mock(1))
        assert comedor.quitar_silla(5) == "Índice de silla inválido"


class TestDescripcionYResumen:
    def test_descripcion_sin_sillas(self, mesa_mock):
        desc = Comedor("Mini", mesa_mock).obtener_descripcion_completa()
        assert desc.startswith("=== COMEDOR MINI ===")
        assert "Mesa Mock" in desc
        assert "SILLAS: Ninguna incluida" in desc
        assert "PRECIO TOTAL: $200.00" in desc
        assert "descuento" not in desc

    def test_descripcion_con_descuento(self, mesa_mock):
        desc = Comedor(
            "Grande", mesa_mock, sillas_mock(4)
        ).obtener_descripcion_completa()
        assert "SILLAS (4 unidades):" in desc
        assert "1. Silla Mock 1" in desc
        assert "PRECIO TOTAL: $380.00" in desc
        assert "(Incluye 5% de descuento por set completo)" in desc

    def test_resumen(self, mesa_mock):
        sillas = sillas_mock(2)
        sillas[0].material_tapizado = "cuero"
        resumen = Comedor("C", mesa_mock, sillas).obtener_resumen()
        assert resumen["nombre"] == "C"
        assert resumen["total_muebles"] == 3
        assert resumen["precio_mesa"] == 200.0
        assert resumen["precio_sillas"] == 100.0
        assert resumen["precio_total"] == 300.0
        assert resumen["capacidad_personas"] == 2
        assert sorted(resumen["materiales_utilizados"]) == ["Roble", "cuero"]

    def test_materiales_ignora_objetos_sin_material(self):
        class Simple:
            def calcular_precio(self):
                return 10.0

        resumen = Comedor("C", Simple(), [Simple()]).obtener_resumen()
        assert resumen["materiales_utilizados"] == []
