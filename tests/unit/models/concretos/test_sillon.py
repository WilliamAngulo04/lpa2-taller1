import pytest

from models.categorias.asientos import Asiento
from models.concretos.sillon import Sillon


class TestSillon:
    def test_herencia(self):
        mueble = Sillon("S", "Madera", "Rojo", 400)
        assert isinstance(mueble, Asiento)
        assert str(mueble).startswith(mueble.nombre)

    def test_valores_por_defecto(self):
        sillon = Sillon("Sillón", "Madera", "Rojo", 400)
        assert sillon.capacidad_personas == 2
        assert sillon.tiene_respaldo is True
        assert sillon.material_tapizado is None
        assert sillon.tiene_brazos is True
        assert sillon.es_reclinable is False
        assert sillon.tiene_reposapiés is False

    @pytest.mark.parametrize("precio,esperado", [(None, 0), (399.9, 399)])
    def test_precio_base_se_convierte_a_entero(self, precio, esperado):
        assert Sillon("S", "Madera", "Rojo", precio).precio_base == esperado

    def test_hereda_validaciones_de_asiento(self):
        sillon = Sillon("S", "Madera", "Rojo", 400)
        with pytest.raises(ValueError):
            sillon.capacidad_personas = 0
        assert "Capacidad: 2 personas" in sillon.obtener_info_asiento()

    def test_precio_por_defecto(self):
        # 400 + 100 (brazos)
        assert Sillon("S", "Madera", "Rojo", 400).calcular_precio() == 500

    def test_precio_completo(self):
        sillon = Sillon("S", "Madera", "Rojo", 400, 1, True, "cuero", True, True, True)
        # 400 + 200 + 100 + 250 + 80
        assert sillon.calcular_precio() == 1030

    def test_precio_sin_extras(self):
        sillon = Sillon("S", "Madera", "Rojo", 400, tiene_brazos=False)
        assert sillon.calcular_precio() == 400

    def test_descripcion(self):
        desc = Sillon(
            "Relax", "Madera", "Rojo", 400, es_reclinable=True
        ).obtener_descripcion()
        assert desc.startswith("Sillón 'Relax'")
        assert "Tapizado=N/A" in desc
        assert "Reclinable=Sí" in desc
        assert "Reposapiés=No" in desc
        assert "Precio base=$400" in desc
