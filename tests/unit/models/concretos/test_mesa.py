import pytest

from models.categorias.superficies import Superficie
from models.concretos.mesa import Mesa


class TestMesa:
    def test_herencia(self, mesa_basica):
        assert isinstance(mesa_basica, Superficie)

    def test_valores_por_defecto(self, mesa_basica):
        assert mesa_basica.forma == "rectangular"
        assert mesa_basica.largo == 120.0
        assert mesa_basica.ancho == 80.0
        assert mesa_basica.altura == 75.0
        assert mesa_basica.capacidad_personas == 4

    @pytest.mark.parametrize("forma", ["rectangular", "redonda", "cuadrada", "ovalada"])
    def test_forma_valida(self, mesa_basica, forma):
        mesa_basica.forma = forma
        assert mesa_basica.forma == forma

    def test_forma_invalida(self, mesa_basica):
        with pytest.raises(ValueError, match="Forma debe ser"):
            mesa_basica.forma = "triangular"

    def test_capacidad_valida(self, mesa_basica):
        mesa_basica.capacidad_personas = 8
        assert mesa_basica.capacidad_personas == 8

    def test_capacidad_invalida(self, mesa_basica):
        with pytest.raises(ValueError):
            mesa_basica.capacidad_personas = 0

    def test_calcular_precio_basico(self, mesa_basica):
        # 200 * (1 + 9600/10000 * 0.05) = 209.6
        assert mesa_basica.calcular_precio() == pytest.approx(209.6)

    @pytest.mark.parametrize(
        "forma,capacidad,extra",
        [
            ("rectangular", 4, 0),
            ("redonda", 4, 50),
            ("rectangular", 5, 50),
            ("rectangular", 6, 50),
            ("rectangular", 7, 100),
            ("ovalada", 8, 150),
        ],
    )
    def test_ajustes_precio(self, forma, capacidad, extra):
        mesa = Mesa("M", "Roble", "Natural", 200.0, forma, capacidad_personas=capacidad)
        assert mesa.calcular_precio() == pytest.approx(209.6 + extra)

    def test_obtener_descripcion(self, mesa_basica):
        desc = mesa_basica.obtener_descripcion()
        assert desc.startswith("Mesa: Mesa Comedor")
        assert "Forma: rectangular" in desc
        assert "Dimensiones: 120.0x80.0x75.0cm" in desc
        assert "Capacidad: 4 personas" in desc
        assert "Precio final: $209.6" in desc
