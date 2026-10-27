import pytest

from models.concretos.armario import Armario
from models.mueble import Mueble


class TestArmario:
    def test_herencia(self):
        mueble = Armario("A", "Pino", "Blanco", 500)
        assert isinstance(mueble, Mueble)
        assert str(mueble).startswith(mueble.nombre)

    def test_valores_por_defecto(self):
        armario = Armario("Armario", "Pino", "Blanco", 500)
        assert armario.num_puertas == 2
        assert armario.num_cajones == 0
        assert armario.tiene_espejos is False

    @pytest.mark.parametrize("precio,esperado", [(None, 0), (99.9, 99), ("150", 150)])
    def test_precio_base_se_convierte_a_entero(self, precio, esperado):
        assert Armario("A", "Pino", "Blanco", precio).precio_base == esperado

    def test_precio_por_defecto(self):
        # 500 + 2 * 50
        assert Armario("A", "Pino", "Blanco", 500).calcular_precio() == 600

    def test_precio_completo(self):
        armario = Armario("A", "Pino", "Blanco", 500, 4, 3, True)
        # 500 + 200 + 90 + 100
        assert armario.calcular_precio() == 890

    @pytest.mark.parametrize(
        "espejos,texto", [(True, "Espejos=Sí"), (False, "Espejos=No")]
    )
    def test_descripcion(self, espejos, texto):
        desc = Armario(
            "Ropero", "Pino", "Blanco", 500, tiene_espejos=espejos
        ).obtener_descripcion()
        assert desc.startswith("Armario 'Ropero'")
        assert "Puertas=2" in desc
        assert texto in desc
        assert "Precio base=$500" in desc
