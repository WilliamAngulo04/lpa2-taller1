"""
Clase concreta Sillón.
Implementa un mueble de asiento para más de una persona, con brazos y respaldo.
"""

from ..categorias.asientos import Asiento


class Sillon(Asiento):
    """
    Clase concreta que representa un sillón.
    Hereda de Asiento y añade características específicas.
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: int,
        capacidad_personas: int = 2,
        tiene_respaldo: bool = True,
        material_tapizado: str = None,
        tiene_brazos: bool = True,
        es_reclinable: bool = False,
        tiene_reposapiés: bool = False,
    ):
        super().__init__(
            nombre,
            material,
            color,
            int(precio_base) if precio_base is not None else 0,
            capacidad_personas,
            tiene_respaldo,
            material_tapizado,
        )
        self.tiene_brazos = tiene_brazos
        self.es_reclinable = es_reclinable
        self.tiene_reposapiés = tiene_reposapiés

    def calcular_precio(self) -> int:
        """Calcula el precio final del sillón."""
        precio = self.precio_base
        if self.material_tapizado:
            precio += 200
        if self.tiene_brazos:
            precio += 100
        if self.es_reclinable:
            precio += 250
        if self.tiene_reposapiés:
            precio += 80
        return int(round(precio))

    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada del sillón.
        """
        return (
            f"Sillón '{self.nombre}': Material={self.material}, Color={self.color}, "
            f"Capacidad={self.capacidad_personas} personas, Tapizado={self.material_tapizado or 'N/A'}, "
            f"Brazos={'Sí' if self.tiene_brazos else 'No'}, Reclinable={'Sí' if self.es_reclinable else 'No'}, "
            f"Reposapiés={'Sí' if self.tiene_reposapiés else 'No'}, Precio base=${self.precio_base}"
        )
