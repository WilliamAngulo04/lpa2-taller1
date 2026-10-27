import pytest

from models.categorias.asientos import Asiento
from models.mueble import Mueble


class AsientoConcreto(Asiento):
    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_comodidad()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_asiento()


def crear_asiento(capacidad=1, respaldo=False, tapizado=None):
    return AsientoConcreto(
        "Asiento", "Madera", "Café", 100.0, capacidad, respaldo, tapizado
    )


class TestAsiento:
    def test_es_abstracta(self):
        with pytest.raises(TypeError):
            Asiento("A", "Madera", "Café", 100.0, 1, True)

    def test_hereda_de_mueble(self):
        assert issubclass(Asiento, Mueble)
        assert isinstance(crear_asiento(), Mueble)

    def test_atributos(self):
        asiento = crear_asiento(capacidad=2, respaldo=True, tapizado="tela")
        assert asiento.capacidad_personas == 2
        assert asiento.tiene_respaldo is True
        assert asiento.material_tapizado == "tela"

    def test_setters(self):
        asiento = crear_asiento()
        asiento.capacidad_personas = 4
        asiento.tiene_respaldo = True
        asiento.material_tapizado = "cuero"
        assert asiento.capacidad_personas == 4
        assert asiento.tiene_respaldo is True
        assert asiento.material_tapizado == "cuero"

    @pytest.mark.parametrize("valor", [0, -1])
    def test_capacidad_invalida(self, valor):
        with pytest.raises(ValueError, match="mayor a 0"):
            crear_asiento().capacidad_personas = valor

    @pytest.mark.parametrize(
        "capacidad,respaldo,tapizado,esperado",
        [
            (1, False, None, 1.0),
            (1, True, None, 1.1),
            (1, False, "Cuero", 1.2),
            (1, False, "tela", 1.1),
            (1, False, "lino", 1.0),  # tapizado no reconocido no suma
            (3, True, "cuero", 1.4),
        ],
    )
    def test_factor_comodidad(self, capacidad, respaldo, tapizado, esperado):
        asiento = crear_asiento(capacidad, respaldo, tapizado)
        assert asiento.calcular_factor_comodidad() == pytest.approx(esperado)

    def test_info_asiento_sin_tapizado(self):
        info = crear_asiento().obtener_info_asiento()
        assert info == "Capacidad: 1 personas, Respaldo: No"

    def test_info_asiento_con_tapizado(self):
        info = crear_asiento(2, True, "tela").obtener_info_asiento()
        assert info == "Capacidad: 2 personas, Respaldo: Sí, Tapizado: tela"
