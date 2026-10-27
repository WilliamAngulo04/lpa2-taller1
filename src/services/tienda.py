"""
Servicio de la tienda que maneja la lógica de negocio.
Esta clase implementa el patrón de servicio para separar la lógica de negocio de la UI.
"""

from typing import List, Dict, Optional, Union

# Corrección de imports para ejecución directa
from models.mueble import Mueble
from models.composicion.comedor import Comedor
# TODO: Importar las clases necesarias


class TiendaMuebles:
    """
    Clase que maneja toda la lógica de negocio de la tienda de muebles.

    Esta clase implementa:
    - Gestión de inventario
    - Búsquedas y filtros
    - Cálculos de precios y descuentos
    - Operaciones de venta

    Conceptos OOP aplicados:
    - Encapsulación: Agrupa toda la lógica relacionada con la tienda
    - Abstracción: Oculta la complejidad del manejo de inventario
    - Composición: Contiene colecciones de muebles
    """

    def obtener_estadisticas(self) -> dict:
        """
        Retorna estadísticas básicas y acumulativas de la tienda para la UI.
        Returns:
            dict: Diccionario con estadísticas
        """
        try:
            total_muebles = len(self._inventario)
            total_comedores = len(self._comedores)
            valor_inventario = 0
            for mueble in self._inventario:
                try:
                    valor_inventario += mueble.calcular_precio()
                except Exception:
                    pass
            tipos_muebles = {}
            for mueble in self._inventario:
                tipo = type(mueble).__name__
                tipos_muebles[tipo] = tipos_muebles.get(tipo, 0) + 1
            ventas_realizadas = (
                len(self._ventas_realizadas)
                if hasattr(self, "_ventas_realizadas")
                else 0
            )
            # Acumulativos
            total_muebles_vendidos = getattr(self, "_total_muebles_vendidos", 0)
            valor_total_ventas = getattr(self, "_valor_total_ventas", 0.0)
            return {
                "total_muebles": total_muebles,
                "total_comedores": total_comedores,
                "valor_inventario": valor_inventario,
                "tipos_muebles": tipos_muebles,
                "descuentos_activos": self._descuentos_activos.copy(),
                "ventas_realizadas": ventas_realizadas,
                "total_muebles_vendidos": total_muebles_vendidos,
                "valor_total_ventas": valor_total_ventas,
            }
        except Exception:
            return {
                "total_muebles": 0,
                "total_comedores": 0,
                "valor_inventario": 0.0,
                "tipos_muebles": {},
                "descuentos_activos": {},
                "ventas_realizadas": 0,
                "total_muebles_vendidos": 0,
                "valor_total_ventas": 0.0,
            }

    def estadisticas(self) -> dict:
        """Alias de obtener_estadisticas() para compatibilidad."""
        return self.obtener_estadisticas()

    def __init__(self, nombre_tienda: str = "Mueblería OOP"):
        """
        Constructor de la tienda.

        Args:
            nombre_tienda: Nombre de la tienda
        """
        self._nombre = nombre_tienda
        self._inventario: List[Mueble] = []
        self._comedores: List[Comedor] = []
        self._ventas_realizadas: List[Dict] = []
        self._descuentos_activos: Dict[str, float] = {}
        # Campos acumulativos
        self._total_muebles_vendidos: int = 0
        self._valor_total_ventas: float = 0.0

    @property
    def nombre(self) -> str:
        """Getter para el nombre de la tienda."""
        return self._nombre

    # @property
    # def total_muebles(self) -> int:
    #     """Retorna el total de muebles en inventario."""
    #     return len(self._inventario)

    def agregar_mueble(self, mueble: "Mueble") -> str:
        """
        Agrega un mueble al inventario de la tienda.
        Args:
            mueble: Objeto mueble a agregar
        Returns:
            str: Mensaje de confirmación
        """
        if mueble is None:
            return "Error: El mueble no puede ser None"
        try:
            precio = mueble.calcular_precio()
            if precio <= 0:
                return "Error: El mueble debe tener un precio válido mayor a 0"
        except Exception as e:
            return f"Error al calcular precio del mueble: {str(e)}"
        self._inventario.append(mueble)
        return f"Mueble {getattr(mueble, 'nombre', str(mueble))} agregado exitosamente al inventario"

    def agregar_comedor(self, comedor: "Comedor") -> str:
        """
        Agrega un comedor completo a la tienda.
        Args:
            comedor: Objeto Comedor a agregar
        Returns:
            str: Mensaje de confirmación
        """
        if comedor is None:
            return "Error: El comedor no puede ser None"
        self._comedores.append(comedor)
        return (
            f"Comedor {getattr(comedor, 'nombre', str(comedor))} agregado exitosamente"
        )

    def buscar_muebles_por_nombre(self, nombre: str) -> List["Mueble"]:
        """
        Busca muebles por nombre (búsqueda parcial, case-insensitive).
        Args:
            nombre: Nombre o parte del nombre a buscar
        Returns:
            List[Mueble]: Lista de muebles que coinciden con la búsqueda
        """
        if not nombre or not nombre.strip():
            return []
        nombre_lower = nombre.lower().strip()
        resultados = []
        for mueble in self._inventario:
            if nombre_lower in mueble.nombre.lower():
                resultados.append(mueble)
        return resultados

    def filtrar_por_precio(
        self, precio_min: float = 0, precio_max: float = float("inf")
    ) -> List["Mueble"]:
        """
        Filtra muebles por rango de precios.

        Args:
            precio_min: Precio mínimo (inclusivo)
            precio_max: Precio máximo (inclusivo)
        Returns:
            List[Mueble]: Lista de muebles en el rango de precios
        """
        if precio_min < 0:
            precio_min = 0
        resultados = []
        for mueble in self._inventario:
            try:
                precio = mueble.calcular_precio()
                if precio_min <= precio <= precio_max:
                    resultados.append(mueble)
            except Exception:
                continue  # Saltar muebles con errores de precio
        return resultados

    def filtrar_por_material(self, material: str) -> List["Mueble"]:
        """
        Filtra muebles por material.

        Args:
            material: Material a buscar
        Returns:
            List[Mueble]: Lista de muebles del material especificado
        """
        if not material or not material.strip():
            return []
        material_lower = material.lower().strip()
        resultados = []
        for mueble in self._inventario:
            try:
                if (
                    hasattr(mueble, "material")
                    and mueble.material
                    and mueble.material.lower().strip() == material_lower
                ):
                    resultados.append(mueble)
            except Exception:
                continue
        return resultados

    def obtener_muebles_por_tipo(self, tipo_clase: type) -> List["Mueble"]:
        """
        Obtiene todos los muebles de un tipo específico.

        Args:
            tipo_clase: Clase del tipo de mueble (ej: Silla, Mesa, etc.)

        Returns:
            List[Mueble]: Lista de muebles del tipo especificado
        """
        return [mueble for mueble in self._inventario if isinstance(mueble, tipo_clase)]

    def calcular_valor_inventario(self) -> float:
        """
        Calcula el valor total del inventario.

        Returns:
            float: Valor total de todos los muebles en inventario
        """
        valor_total = 0
        for mueble in self._inventario:
            try:
                valor_total += mueble.calcular_precio()
            except Exception:
                continue  # Saltar muebles con errores

        for comedor in self._comedores:
            try:
                valor_total += comedor.calcular_precio_total()
            except Exception:
                continue

        return round(valor_total, 2)

    def aplicar_descuento(self, categoria: str, porcentaje: float) -> str:
        """
        Aplica un descuento a una categoría de muebles.

        Args:
            categoria: Nombre de la categoría (ej: "sillas", "mesas")
            porcentaje: Porcentaje de descuento (0-100)
        Returns:
            str: Mensaje de confirmación
        """
        if not 0 < porcentaje <= 100:
            return "Error: El porcentaje debe estar entre 1 y 100"
        categoria_lower = categoria.lower().strip()
        # Normalizar nombres de clase (Silla, Mesa, etc.)
        # El sistema usa el nombre de la clase, por ejemplo 'Silla', 'Mesa', etc.
        # Si el usuario ingresa 'sillas', 'mesas', etc., quitamos la 's' final si existe
        if categoria_lower.endswith("s"):
            categoria_lower = categoria_lower[:-1]
        # Capitalizar para coincidir con el nombre de clase
        categoria_clase = categoria_lower.capitalize()
        self._descuentos_activos[categoria_clase] = porcentaje / 100
        return (
            f"Descuento del {porcentaje}% aplicado a la categoría '{categoria_clase}'"
        )

    def aplicar_descuento_material(self, material: str, porcentaje: float) -> str:
        """
        Reduce el precio base de los muebles de un material específico.

        Args:
            material: Material de los muebles a rebajar (case-insensitive)
            porcentaje: Fracción de descuento, mayor a 0 y menor a 1 (ej: 0.1 = 10%)
        Returns:
            str: Mensaje de confirmación
        """
        if not 0 < porcentaje < 1:
            return "Error: El porcentaje debe ser mayor a 0 y menor a 1"
        muebles = self.filtrar_por_material(material)
        for mueble in muebles:
            mueble.precio_base = mueble.precio_base * (1 - porcentaje)
        return (
            f"Descuento del {porcentaje * 100:g}% aplicado a {len(muebles)} "
            f"mueble(s) de material '{material}'"
        )

    def realizar_venta(
        self, mueble: "Mueble", cliente: str = "Cliente Anónimo"
    ) -> Dict:
        """
        Procesa la venta de un mueble.
        Args:
            mueble: Mueble a vender
            cliente: Nombre del cliente
        Returns:
            Dict: Información de la venta realizada o error
        """
        if mueble not in self._inventario:
            return {"error": "El mueble no está disponible en inventario"}
        try:
            precio_original = mueble.calcular_precio()
            # Use the class name as key, matching how discounts are registered
            tipo_mueble = type(mueble).__name__
            descuento_aplicado = self._obtener_descuento(tipo_mueble)
            precio_final = precio_original * (1 - descuento_aplicado)
            from datetime import datetime

            # Ensure mueble.nombre is always a string
            nombre_mueble = getattr(mueble, "nombre", None)
            if not nombre_mueble:
                nombre_mueble = tipo_mueble
            venta = {
                "mueble": nombre_mueble,
                "cliente": cliente,
                "precio_original": precio_original,
                "descuento": descuento_aplicado * 100,
                "precio_final": round(precio_final, 2),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self._ventas_realizadas.append(venta)
            self._inventario.remove(mueble)
            # Acumulativos
            self._total_muebles_vendidos += 1
            self._valor_total_ventas += venta["precio_final"]
            return venta
        except Exception as e:
            return {"error": f"Error al procesar la venta: {str(e)}"}

    def _obtener_descuento(self, tipo_mueble: str) -> float:
        """
        Busca el descuento activo para un tipo de mueble.
        La comparación ignora mayúsculas, ya que aplicar_descuento normaliza
        la categoría con capitalize() (ej: 'SofaCama' se registra como 'Sofacama').

        Returns:
            float: Fracción de descuento (0 si no hay descuento para el tipo)
        """
        for categoria, descuento in self._descuentos_activos.items():
            if categoria.lower() == tipo_mueble.lower():
                return descuento
        return 0

    def _contar_tipos_muebles(self) -> Dict[str, int]:
        """
        Cuenta cuántos muebles hay de cada tipo.
        Método privado auxiliar.

        Returns:
            Dict[str, int]: Diccionario con el conteo por tipo
        """
        conteo = {}
        for mueble in self._inventario:
            tipo = type(mueble).__name__
            conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo

    def generar_reporte_inventario(self) -> str:
        """
        Genera un reporte completo del inventario.
        Returns:
            str: Reporte detallado del inventario
        """
        estadisticas = self.obtener_estadisticas() or {}
        nombre_tienda = getattr(self, "_nombre", "Tienda")
        if not isinstance(estadisticas, dict):
            estadisticas = {}
        reporte = f"=== REPORTE DE INVENTARIO - {nombre_tienda} ===\n\n"
        reporte += f"Total de muebles: {estadisticas.get('total_muebles', 0)}\n"
        reporte += f"Total de comedores: {estadisticas.get('total_comedores', 0)}\n"
        reporte += f"Valor total del inventario: ${estadisticas.get('valor_inventario', 0):.2f}\n\n"
        reporte += "DISTRIBUCIÓN POR TIPOS:\n"
        tipos = estadisticas.get("tipos_muebles", {}) or {}
        for tipo, cantidad in tipos.items():
            reporte += f"- {tipo}: {cantidad} unidades\n"
        descuentos = estadisticas.get("descuentos_activos", {}) or {}
        if descuentos:
            reporte += "\nDESCUENTOS ACTIVOS:\n"
            for categoria, descuento in descuentos.items():
                reporte += f"- {categoria}: {descuento * 100:.1f}%\n"
        return reporte
