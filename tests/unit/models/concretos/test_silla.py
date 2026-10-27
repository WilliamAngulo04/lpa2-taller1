import pytest

from models.categorias.asientos import Asiento
from models.concretos.silla import Silla
from models.mueble import Mueble


class TestSilla:
    def test_herencia(self, silla_basica):
        assert isinstance(silla_basica, Asiento)
        assert isinstance(silla_basica, Mueble)

    def test_instanciacion_correcta(self, silla_basica):
        # Atributos heredados
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.precio_base == 100.0
        # Valores por defecto
        assert silla_basica.capacidad_personas == 1
        assert silla_basica.tiene_respaldo is True
        assert silla_basica.material_tapizado is None
        assert silla_basica.altura_regulable is False
        assert silla_basica.tiene_ruedas is False

    def test_setters_propios(self, silla_basica):
        silla_basica.altura_regulable = True
        silla_basica.tiene_ruedas = True
        assert silla_basica.altura_regulable is True
        assert silla_basica.tiene_ruedas is True

    def test_calcular_precio_basico(self, silla_basica):
        # 100 * 1.1 (respaldo)
        assert silla_basica.calcular_precio() == pytest.approx(110.0)

    def test_calcular_precio_oficina(self, silla_oficina):
        # 200 * 1.3 (respaldo + cuero) + 30 (altura) + 20 (ruedas)
        assert silla_oficina.calcular_precio() == pytest.approx(310.0)

    @pytest.mark.parametrize(
        "respaldo,tapizado,esperado",
        [(False, None, 100.0), (True, "tela", 120.0), (True, "cuero", 130.0)],
    )
    def test_precio_segun_comodidad(self, respaldo, tapizado, esperado):
        silla = Silla("S", "Madera", "Café", 100.0, respaldo, tapizado)
        assert silla.calcular_precio() == pytest.approx(esperado)

    def test_obtener_descripcion(self, silla_oficina):
        desc = silla_oficina.obtener_descripcion()
        assert desc.startswith("Silla: Silla Oficina")
        assert "Tapizado: cuero" in desc
        assert "Altura regulable: Sí" in desc
        assert "Ruedas: Sí" in desc
        assert "Precio final: $310.0" in desc

    def test_descripcion_sin_extras(self, silla_basica):
        desc = silla_basica.obtener_descripcion()
        assert "Altura regulable: No" in desc
        assert "Ruedas: No" in desc

    def test_regular_altura_no_regulable(self, silla_basica):
        assert silla_basica.regular_altura(50) == "Esta silla no tiene altura regulable"

    @pytest.mark.parametrize("altura", [39, 101])
    def test_regular_altura_fuera_de_rango(self, silla_oficina, altura):
        assert "entre 40 y 100" in silla_oficina.regular_altura(altura)

    @pytest.mark.parametrize("altura", [40, 70, 100])
    def test_regular_altura_valida(self, silla_oficina, altura):
        assert silla_oficina.regular_altura(altura) == f"Altura ajustada a {altura} cm"

    def test_es_silla_oficina(self, silla_basica, silla_oficina):
        assert silla_oficina.es_silla_oficina() is True
        assert silla_basica.es_silla_oficina() is False
