import pytest

from models.concretos.escritorio import Escritorio
from models.mueble import Mueble


class TestEscritorio:
    def test_herencia(self):
        mueble = Escritorio("E", "Pino", "Blanco", 300)
        assert isinstance(mueble, Mueble)
        assert str(mueble).startswith(mueble.nombre)

    def test_valores_por_defecto(self):
        escritorio = Escritorio("Escritorio", "Pino", "Blanco", 300)
        assert escritorio.forma == "rectangular"
        assert escritorio.tiene_cajones is False
        assert escritorio.num_cajones == 0
        assert escritorio.largo == 1.2
        assert escritorio.tiene_iluminacion is False

    def test_precio_base_none(self):
        assert Escritorio("E", "Pino", "Blanco", None).precio_base == 0

    def test_precio_basico(self):
        assert Escritorio("E", "Pino", "Blanco", 300).calcular_precio() == 300

    def test_cajones_solo_cuentan_si_tiene_cajones(self):
        sin = Escritorio("E", "Pino", "Blanco", 300, tiene_cajones=False, num_cajones=3)
        con = Escritorio("E", "Pino", "Blanco", 300, tiene_cajones=True, num_cajones=3)
        assert sin.calcular_precio() == 300
        assert con.calcular_precio() == 375

    @pytest.mark.parametrize("largo,esperado", [(1.5, 300), (1.6, 350)])
    def test_recargo_por_largo(self, largo, esperado):
        assert (
            Escritorio("E", "Pino", "Blanco", 300, largo=largo).calcular_precio()
            == esperado
        )

    def test_precio_completo(self):
        escritorio = Escritorio("E", "Pino", "Blanco", 300, "L", True, 2, 1.8, True)
        # 300 + 50 (cajones) + 50 (largo) + 40 (luz) + 30 (forma)
        assert escritorio.calcular_precio() == 470

    def test_descripcion(self):
        sin = Escritorio(
            "Gamer", "Pino", "Negro", 300, num_cajones=3
        ).obtener_descripcion()
        con = Escritorio(
            "Gamer",
            "Pino",
            "Negro",
            300,
            tiene_cajones=True,
            num_cajones=3,
            tiene_iluminacion=True,
        ).obtener_descripcion()
        assert sin.startswith("Escritorio 'Gamer'")
        assert "Cajones=0" in sin
        assert "Iluminación=No" in sin
        assert "Cajones=3" in con
        assert "Iluminación=Sí" in con
