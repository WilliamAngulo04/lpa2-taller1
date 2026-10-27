"""
Clase concreta Armario.
Representa un armario genérico.
"""

from ..mueble import Mueble


class Armario(Mueble):
    """
    Clase concreta que representa un armario.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: int,
        num_puertas: int = 2,
        num_cajones: int = 0,
        tiene_espejos: bool = False,
    ):
        super().__init__(
            nombre,
            material,
            color,
            int(precio_base) if precio_base is not None else 0,
        )
        self.num_puertas = num_puertas
        self.num_cajones = num_cajones
        self.tiene_espejos = tiene_espejos

    def calcular_precio(self) -> int:
        """Calcula el precio final del armario."""
        precio = self.precio_base
        precio += self.num_puertas * 50
        precio += self.num_cajones * 30
        if self.tiene_espejos:
            precio += 100
        return int(round(precio))

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada del armario.
        """
        return (
            f"Armario '{self.nombre}': Material={self.material}, Color={self.color}, "
            f"Puertas={self.num_puertas}, Cajones={self.num_cajones}, Espejos={'Sí' if self.tiene_espejos else 'No'}, "
            f"Precio base=${self.precio_base}"
        )
