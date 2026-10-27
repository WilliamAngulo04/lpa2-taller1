import pytest

from models.concretos.cama import Cama
from models.mueble import Mueble


class TestCama:
    def test_herencia(self, cama_basica):
        assert isinstance(cama_basica, Mueble)

    def test_valores_por_defecto(self, cama_basica):
        assert cama_basica.tamaño == "individual"
        assert cama_basica.incluye_colchon is False
        assert cama_basica.tiene_cabecera is False

    @pytest.mark.parametrize("tamaño", ["individual", "matrimonial", "queen", "king"])
    def test_tamaño_valido(self, cama_basica, tamaño):
        cama_basica.tamaño = tamaño
        assert cama_basica.tamaño == tamaño

    def test_tamaño_invalido(self, cama_basica):
        with pytest.raises(ValueError, match="Tamaño debe ser"):
            cama_basica.tamaño = "gigante"

    @pytest.mark.parametrize(
        "tamaño,esperado",
        [("individual", 500), ("matrimonial", 700), ("queen", 900), ("king", 1100)],
    )
    def test_precio_por_tamaño(self, tamaño, esperado):
        cama = Cama("C", "Madera", "Blanco", 500.0, tamaño)
        assert cama.calcular_precio() == esperado

    def test_precio_con_extras(self):
        cama = Cama("C", "Madera", "Blanco", 500.0, "king", True, True)
        # 500 + 600 + 300 (colchón) + 100 (cabecera)
        assert cama.calcular_precio() == 1500

    def test_obtener_descripcion(self):
        cama = Cama("Cama Lujo", "Madera", "Nogal", 500.0, "queen", True, False)
        desc = cama.obtener_descripcion()
        assert desc.startswith("Cama: Cama Lujo")
        assert "Tamaño: queen" in desc
        assert "Incluye colchón: Sí" in desc
        assert "Cabecera: No" in desc
        assert "Precio final: $1200" in desc
