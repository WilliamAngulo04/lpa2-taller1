"""
Pruebas para models.concretos.comedor (versión simple del comedor).
"""

from unittest.mock import Mock

import pytest

from models.concretos.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def mesa_mock():
    mesa = Mock(spec=Mesa)
    mesa.calcular_precio.return_value = 200.0
    mesa.obtener_descripcion.return_value = "Mesa Mock"
    return mesa


@pytest.fixture
def silla_mock():
    silla = Mock(spec=Silla)
    silla.calcular_precio.return_value = 50.0
    silla.obtener_descripcion.return_value = "Silla Mock"
    return silla


class TestComedorConcreto:
    def test_sin_sillas_por_defecto(self, mesa_mock):
        comedor = Comedor(mesa_mock)
        assert comedor.sillas == []
        assert comedor.cantidad_sillas() == 0

    def test_agregar_y_quitar_silla(self, mesa_mock, silla_mock):
        comedor = Comedor(mesa_mock)
        comedor.agregar_silla(silla_mock)
        assert comedor.cantidad_sillas() == 1
        comedor.quitar_silla(silla_mock)
        assert comedor.cantidad_sillas() == 0

    def test_quitar_silla_inexistente_no_falla(self, mesa_mock, silla_mock):
        comedor = Comedor(mesa_mock)
        comedor.quitar_silla(silla_mock)
        assert comedor.cantidad_sillas() == 0

    def test_calcular_precio_total(self, mesa_mock, silla_mock):
        comedor = Comedor(mesa_mock, [silla_mock] * 4)
        assert comedor.calcular_precio_total() == 400.0
        mesa_mock.calcular_precio.assert_called_once()
        assert silla_mock.calcular_precio.call_count == 4

    def test_descripcion(self, mesa_mock, silla_mock):
        desc = Comedor(mesa_mock, [silla_mock, silla_mock]).descripcion()
        assert desc.startswith("Comedor con mesa: Mesa Mock")
        assert "y 2 sillas:" in desc
        assert "  1. Silla Mock" in desc
        assert "  2. Silla Mock" in desc
