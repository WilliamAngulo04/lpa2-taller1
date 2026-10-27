import pytest

from models.concretos.cajonera import Cajonera
from models.mueble import Mueble


class TestCajonera:
    def test_herencia(self):
        mueble = Cajonera("C", "Pino", "Blanco", 200)
        assert isinstance(mueble, Mueble)
        assert str(mueble).startswith(mueble.nombre)

    def test_valores_por_defecto(self):
        cajonera = Cajonera("Cajonera", "Pino", "Blanco", 200)
        assert cajonera.num_cajones == 3
        assert cajonera.tiene_ruedas is False

    def test_precio_base_none(self):
        assert Cajonera("C", "Pino", "Blanco", None).precio_base == 0

    @pytest.mark.parametrize(
        "cajones,ruedas,esperado", [(3, False, 260), (5, True, 330), (0, False, 200)]
    )
    def test_calcular_precio(self, cajones, ruedas, esperado):
        cajonera = Cajonera("C", "Pino", "Blanco", 200, cajones, ruedas)
        assert cajonera.calcular_precio() == esperado

    @pytest.mark.parametrize(
        "ruedas,texto", [(True, "Ruedas=Sí"), (False, "Ruedas=No")]
    )
    def test_descripcion(self, ruedas, texto):
        desc = Cajonera(
            "Cómoda", "Pino", "Blanco", 200, tiene_ruedas=ruedas
        ).obtener_descripcion()
        assert desc.startswith("Cajonera 'Cómoda'")
        assert "Cajones=3" in desc
        assert texto in desc
