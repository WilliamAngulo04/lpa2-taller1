from typing import List
from ..concretos.mesa import Mesa
from ..concretos.silla import Silla


class Comedor:
    """
    Clase que representa un conjunto de comedor compuesto por una mesa y varias sillas.
    """

    def __init__(self, mesa: Mesa, sillas: List[Silla] = None):
        self.mesa = mesa
        self.sillas = sillas if sillas is not None else []

    def calcular_precio_total(self) -> float:
        total = self.mesa.calcular_precio()
        total += sum(silla.calcular_precio() for silla in self.sillas)
        return total

    def agregar_silla(self, silla: Silla):
        self.sillas.append(silla)

    def quitar_silla(self, silla: Silla):
        if silla in self.sillas:
            self.sillas.remove(silla)

    def cantidad_sillas(self) -> int:
        return len(self.sillas)

    def descripcion(self) -> str:
        desc = f"Comedor con mesa: {self.mesa.obtener_descripcion()}\n"
        desc += f"y {len(self.sillas)} sillas:\n"
        for idx, silla in enumerate(self.sillas, 1):
            desc += f"  {idx}. {silla.obtener_descripcion()}\n"
        return desc
