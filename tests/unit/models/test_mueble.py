import pytest

from models.mueble import Mueble


class MuebleConcreto(Mueble):
    """Implementación mínima para poder probar la lógica concreta de Mueble."""

    def calcular_precio(self) -> float:
        return self.precio_base

    def obtener_descripcion(self) -> str:
        return f"Mueble {self.nombre}"


@pytest.fixture
def mueble():
    return MuebleConcreto("Mesa", "Madera", "Café", 100.0)


class TestMuebleAbstracto:
    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Mueble("Mesa", "Madera", "Café", 100.0)

    def test_tiene_metodos_abstractos(self):
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__
        assert Mueble.__abstractmethods__ == {"calcular_precio", "obtener_descripcion"}

    def test_subclase_incompleta_no_se_puede_instanciar(self):
        class SoloPrecio(Mueble):
            def calcular_precio(self):
                return 0

        with pytest.raises(TypeError):
            SoloPrecio("X", "Y", "Z", 1.0)


class TestMuebleAtributos:
    def test_constructor_asigna_atributos(self, mueble):
        assert mueble.nombre == "Mesa"
        assert mueble.material == "Madera"
        assert mueble.color == "Café"
        assert mueble.precio_base == 100.0

    @pytest.mark.parametrize("atributo", ["nombre", "material", "color"])
    def test_setter_texto_elimina_espacios(self, mueble, atributo):
        setattr(mueble, atributo, "  Valor  ")
        assert getattr(mueble, atributo) == "Valor"

    @pytest.mark.parametrize("atributo", ["nombre", "material", "color"])
    @pytest.mark.parametrize("valor", ["", "   ", None])
    def test_setter_texto_rechaza_vacios(self, mueble, atributo, valor):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            setattr(mueble, atributo, valor)

    def test_precio_base_acepta_cero(self, mueble):
        mueble.precio_base = 0
        assert mueble.precio_base == 0

    def test_precio_base_rechaza_negativo(self, mueble):
        with pytest.raises(ValueError, match="negativo"):
            mueble.precio_base = -1


class TestMuebleRepresentacion:
    def test_str(self, mueble):
        assert str(mueble) == "Mesa de Madera en color Café"

    def test_repr(self, mueble):
        assert repr(mueble) == (
            "Mueble(nombre='Mesa', material='Madera', color='Café', precio_base=100.0)"
        )
