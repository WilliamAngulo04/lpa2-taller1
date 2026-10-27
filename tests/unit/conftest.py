"""
Fixtures compartidas por las pruebas unitarias.
"""

from unittest.mock import Mock

import pytest

from models.composicion.comedor import Comedor
from models.concretos.cama import Cama
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sofa import Sofa
from services.tienda import TiendaMuebles
from tests.fixtures.datos_muebles import (
    CAMA_BASICA,
    MESA_BASICA,
    SILLA_BASICA,
    SILLA_OFICINA,
    SOFA_BASICO,
)


@pytest.fixture
def silla_basica():
    return Silla(**SILLA_BASICA)


@pytest.fixture
def silla_oficina():
    return Silla(**SILLA_OFICINA)


@pytest.fixture
def mesa_basica():
    return Mesa(**MESA_BASICA)


@pytest.fixture
def sofa_basico():
    return Sofa(**SOFA_BASICO)


@pytest.fixture
def cama_basica():
    return Cama(**CAMA_BASICA)


@pytest.fixture
def sillas_comedor():
    return [Silla(f"Silla {i}", "Roble", "Natural", 100.0) for i in range(1, 5)]


@pytest.fixture
def comedor_basico(mesa_basica, sillas_comedor):
    return Comedor("Comedor Familiar", mesa_basica, sillas_comedor)


@pytest.fixture
def tienda_vacia():
    return TiendaMuebles("Tienda Test")


@pytest.fixture
def tienda_con_inventario(tienda_vacia, silla_basica, mesa_basica, sofa_basico):
    for mueble in (silla_basica, mesa_basica, sofa_basico):
        tienda_vacia.agregar_mueble(mueble)
    return tienda_vacia


@pytest.fixture
def mueble_mock():
    """Mueble simulado con precio fijo, aislado de cualquier implementación real."""
    mock = Mock(spec=Silla)
    mock.nombre = "Mueble Mock"
    mock.material = "Madera"
    mock.color = "Rojo"
    mock.calcular_precio.return_value = 75.0
    return mock
