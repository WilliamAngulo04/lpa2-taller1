import pytest

from models.categorias.almacenamiento import Almacenamiento
from models.mueble import Mueble


class AlmacenamientoConcreto(Almacenamiento):
    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_almacenamiento()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_almacenamiento()


@pytest.fixture
def almacenamiento():
    return AlmacenamientoConcreto("Baúl", "Madera", "Café", 100.0, 3, 200.0)


class TestAlmacenamiento:
    def test_es_abstracta(self):
        with pytest.raises(TypeError):
            Almacenamiento("A", "Madera", "Café", 100.0, 1, 10.0)

    def test_hereda_de_mueble(self, almacenamiento):
        assert isinstance(almacenamiento, Mueble)

    def test_atributos(self, almacenamiento):
        assert almacenamiento.num_compartimentos == 3
        assert almacenamiento.capacidad_litros == 200.0

    def test_setters_validos(self, almacenamiento):
        almacenamiento.num_compartimentos = 5
        almacenamiento.capacidad_litros = 50.0
        assert almacenamiento.num_compartimentos == 5
        assert almacenamiento.capacidad_litros == 50.0

    @pytest.mark.parametrize("valor", [0, -1])
    def test_compartimentos_invalidos(self, almacenamiento, valor):
        with pytest.raises(ValueError, match="compartimentos"):
            almacenamiento.num_compartimentos = valor

    @pytest.mark.parametrize("valor", [0, -5.0])
    def test_capacidad_invalida(self, almacenamiento, valor):
        with pytest.raises(ValueError, match="capacidad"):
            almacenamiento.capacidad_litros = valor

    def test_factor_almacenamiento(self, almacenamiento):
        # 1 + (3-1)*0.05 + (200/100)*0.02 = 1.14
        assert almacenamiento.calcular_factor_almacenamiento() == pytest.approx(1.14)

    def test_info_almacenamiento(self, almacenamiento):
        assert (
            almacenamiento.obtener_info_almacenamiento()
            == "Compartimentos: 3, Capacidad: 200.0L"
        )
