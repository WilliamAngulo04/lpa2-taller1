"""
Clase concreta Escritorio.
Representa un escritorio genérico.
"""

from ..mueble import Mueble


class Escritorio(Mueble):
    """
    Clase concreta que representa un escritorio.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: int,
        forma: str = "rectangular",
        tiene_cajones: bool = False,
        num_cajones: int = 0,
        largo: float = 1.2,
        tiene_iluminacion: bool = False,
    ):
        super().__init__(
            nombre,
            material,
            color,
            int(precio_base) if precio_base is not None else 0,
        )
        self.forma = forma
        self.tiene_cajones = tiene_cajones
        self.num_cajones = num_cajones
        self.largo = largo
        self.tiene_iluminacion = tiene_iluminacion

    def calcular_precio(self) -> int:
        """Calcula el precio final del escritorio."""
        precio = self.precio_base
        if self.tiene_cajones:
            precio += self.num_cajones * 25
        if self.largo > 1.5:
            precio += 50
        if self.tiene_iluminacion:
            precio += 40
        if self.forma != "rectangular":
            precio += 30
        return int(round(precio))

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada del escritorio.
        """
        return (
            f"Escritorio '{self.nombre}': Material={self.material}, Color={self.color}, "
            f"Forma={self.forma}, Cajones={self.num_cajones if self.tiene_cajones else 0}, "
            f"Largo={self.largo}m, Iluminación={'Sí' if self.tiene_iluminacion else 'No'}, "
            f"Precio base=${self.precio_base}"
        )
