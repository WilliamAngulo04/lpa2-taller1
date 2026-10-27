import pytest

from models.categorias.asientos import Asiento
from models.concretos.sofa import Sofa


class TestSofa:
    def test_herencia(self, sofa_basico):
        assert isinstance(sofa_basico, Asiento)

    def test_valores_por_defecto(self, sofa_basico):
        assert sofa_basico.capacidad_personas == 3
        assert sofa_basico.tiene_respaldo is True
        assert sofa_basico.tiene_brazos is True
        assert sofa_basico.es_modular is False
        assert sofa_basico.incluye_cojines is False

    def test_calcular_precio_basico(self, sofa_basico):
        # 1000 * 1.2 (respaldo + 2 personas extra) + 150 (brazos)
        assert sofa_basico.calcular_precio() == pytest.approx(1350.0)

    def test_calcular_precio_completo(self):
        sofa = Sofa("S", "Madera", "Gris", 1000.0, 3, True, "cuero", True, True, True)
        # 1000 * 1.4 + 150 + 200 + 50
        assert sofa.calcular_precio() == pytest.approx(1800.0)

    def test_sin_brazos(self):
        sofa = Sofa("S", "Madera", "Gris", 1000.0, tiene_brazos=False)
        assert sofa.calcular_precio() == pytest.approx(1200.0)

    def test_obtener_descripcion(self, sofa_basico):
        desc = sofa_basico.obtener_descripcion()
        assert desc.startswith("Sofá: Sofá Familiar")
        assert "Capacidad: 3 personas" in desc
        assert "Brazos: Sí" in desc
        assert "Modular: No" in desc
        assert "Incluye cojines: No" in desc
        assert "Precio final: $1350.0" in desc
