import pytest

from models.categorias.superficies import Superficie
from models.mueble import Mueble


class SuperficieConcreta(Superficie):
    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_tamaño()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_superficie()


@pytest.fixture
def superficie():
    return SuperficieConcreta("Tablero", "Madera", "Café", 100.0, 200.0, 100.0, 75.0)


class TestSuperficie:
    def test_es_abstracta(self):
        with pytest.raises(TypeError):
            Superficie("S", "Madera", "Café", 100.0, 1, 1, 1)

    def test_hereda_de_mueble(self, superficie):
        assert isinstance(superficie, Mueble)

    def test_dimensiones(self, superficie):
        assert superficie.largo == 200.0
        assert superficie.ancho == 100.0
        assert superficie.altura == 75.0

    def test_setters_validos(self, superficie):
        superficie.largo = 50
        superficie.ancho = 40
        superficie.altura = 30
        assert (superficie.largo, superficie.ancho, superficie.altura) == (50, 40, 30)

    @pytest.mark.parametrize("atributo", ["largo", "ancho", "altura"])
    @pytest.mark.parametrize("valor", [0, -10])
    def test_setters_invalidos(self, superficie, atributo, valor):
        with pytest.raises(ValueError, match="mayor a 0"):
            setattr(superficie, atributo, valor)

    def test_calcular_area(self, superficie):
        assert superficie.calcular_area() == 20000.0

    def test_factor_tamaño(self, superficie):
        # 20000 cm² -> +10%
        assert superficie.calcular_factor_tamaño() == pytest.approx(1.10)

    def test_info_superficie(self, superficie):
        info = superficie.obtener_info_superficie()
        assert info == "Dimensiones: 200.0x100.0x75.0cm (Área: 20000.0cm²)"
