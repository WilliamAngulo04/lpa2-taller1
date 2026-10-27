import pytest

from models.categorias.asientos import Asiento
from models.concretos.cama import Cama
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama
from models.mueble import Mueble
from tests.fixtures.datos_muebles import SOFACAMA_BASICO


@pytest.fixture
def sofacama():
    return SofaCama(**SOFACAMA_BASICO)


class TestSofaCamaHerencia:
    def test_herencia_multiple(self, sofacama):
        assert isinstance(sofacama, Sofa)
        assert isinstance(sofacama, Cama)
        assert isinstance(sofacama, Mueble)

    def test_mro(self):
        assert SofaCama.__mro__[:5] == (SofaCama, Sofa, Asiento, Cama, Mueble)

    def test_atributos_de_ambos_padres(self, sofacama):
        # De Sofa / Asiento
        assert sofacama.capacidad_personas == 3
        assert sofacama.material_tapizado == "tela"
        assert sofacama.tiene_brazos is True
        # De Cama
        assert sofacama.tamaño == "matrimonial"
        assert sofacama.tamaño_cama == "matrimonial"
        assert sofacama.incluye_colchon is True
        # Propios
        assert sofacama.mecanismo_conversion == "plegable"
        assert sofacama.modo_actual == "sofa"

    def test_tiene_cabecera_heredada_de_cama(self, sofacama):
        assert sofacama.tiene_cabecera is False


class TestSofaCamaPrecio:
    def test_resolucion_metodos(self, sofacama):
        # Sofa: 1000 * 1.3 + 150 = 1450; Cama: +300 (matrimonial) +250 (colchón)
        assert sofacama.calcular_precio() == pytest.approx(2000.0)
        assert sofacama.calcular_precio() > Sofa.calcular_precio(sofacama)

    @pytest.mark.parametrize(
        "tamaño,mecanismo,colchon,esperado",
        [
            ("individual", "plegable", False, 1450.0),
            ("queen", "plegable", False, 1950.0),
            ("king", "hidraulico", False, 2300.0),
            ("matrimonial", "electrico", True, 2300.0),
        ],
    )
    def test_variantes(self, tamaño, mecanismo, colchon, esperado):
        sc = SofaCama(
            "SC",
            "Tela",
            "Gris",
            1000.0,
            tamaño_cama=tamaño,
            incluye_colchon=colchon,
            mecanismo_conversion=mecanismo,
        )
        assert sc.calcular_precio() == pytest.approx(esperado)


class TestSofaCamaConversion:
    def test_convertir_a_cama(self, sofacama):
        mensaje = sofacama.convertir_a_cama()
        assert mensaje == "Sofá convertido a cama usando mecanismo plegable"
        assert sofacama.modo_actual == "cama"

    def test_convertir_a_cama_dos_veces(self, sofacama):
        sofacama.convertir_a_cama()
        assert sofacama.convertir_a_cama() == "El sofá-cama ya está en modo cama"

    def test_convertir_a_sofa_ya_en_sofa(self, sofacama):
        assert sofacama.convertir_a_sofa() == "El sofá-cama ya está en modo sofá"

    def test_ciclo_completo(self, sofacama):
        sofacama.convertir_a_cama()
        mensaje = sofacama.convertir_a_sofa()
        assert mensaje == "Cama convertida a sofá usando mecanismo plegable"
        assert sofacama.modo_actual == "sofa"


class TestSofaCamaInfo:
    def test_obtener_descripcion(self, sofacama):
        desc = sofacama.obtener_descripcion()
        assert desc.startswith("Sofá-Cama: Sofá Cama Moderno")
        assert "Tamaño como cama: matrimonial" in desc
        assert "Mecanismo: plegable" in desc
        assert "Modo actual: sofa" in desc
        assert "Precio final: $2000.0" in desc

    @pytest.mark.parametrize(
        "tamaño,como_cama", [("individual", 1), ("matrimonial", 2), ("king", 2)]
    )
    def test_capacidad_total(self, tamaño, como_cama):
        sc = SofaCama("SC", "Tela", "Gris", 1000.0, 2, tamaño_cama=tamaño)
        assert sc.obtener_capacidad_total() == {"como_sofa": 2, "como_cama": como_cama}

    def test_str(self, sofacama):
        assert str(sofacama) == "Sofá-cama Sofá Cama Moderno (modo: sofa)"
        sofacama.convertir_a_cama()
        assert str(sofacama) == "Sofá-cama Sofá Cama Moderno (modo: cama)"
