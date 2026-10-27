"""
Clase concreta Cajonera.
Representa una cajonera genérica.
"""

from ..mueble import Mueble


class Cajonera(Mueble):
    """
    Clase concreta que representa una cajonera.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: int,
        num_cajones: int = 3,
        tiene_ruedas: bool = False,
    ):
        super().__init__(
            nombre,
            material,
            color,
            int(precio_base) if precio_base is not None else 0,
        )
        self.num_cajones = num_cajones
        self.tiene_ruedas = tiene_ruedas

    def calcular_precio(self) -> int:
        """Calcula el precio final de la cajonera."""
        precio = self.precio_base
        precio += self.num_cajones * 20
        if self.tiene_ruedas:
            precio += 30
        return int(round(precio))

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada de la cajonera.
        """
        return (
            f"Cajonera '{self.nombre}': Material={self.material}, Color={self.color}, "
            f"Cajones={self.num_cajones}, Ruedas={'Sí' if self.tiene_ruedas else 'No'}, "
            f"Precio base=${self.precio_base}"
        )
