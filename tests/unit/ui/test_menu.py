"""
Pruebas de la interfaz MenuTienda.
Las entradas del usuario (Prompt, IntPrompt, Confirm, input) se simulan con mocks
y la salida de Rich se captura en memoria para poder verificarla.
"""

import io
from unittest.mock import Mock, patch

import pytest
from rich.console import Console

from ui.menu import MenuTienda


@pytest.fixture(autouse=True)
def sin_esperas():
    with patch("ui.menu.time.sleep"):
        yield


@pytest.fixture
def menu(tienda_con_inventario):
    menu = MenuTienda(tienda_con_inventario)
    menu.console = Console(file=io.StringIO(), width=200, color_system=None)
    return menu


@pytest.fixture
def menu_vacio(tienda_vacia):
    menu = MenuTienda(tienda_vacia)
    menu.console = Console(file=io.StringIO(), width=200, color_system=None)
    return menu


def salida(menu):
    return menu.console.file.getvalue()


class TestInicializacion:
    def test_atributos(self, tienda_vacia):
        menu = MenuTienda(tienda_vacia)
        assert menu.tienda is tienda_vacia
        assert isinstance(menu.console, Console)
        assert menu.running is True

    def test_banner(self, menu):
        menu.mostrar_banner()
        assert "Tienda Test" in salida(menu)


class TestCatalogo:
    def test_catalogo_vacio(self, menu_vacio):
        menu_vacio.mostrar_catalogo_completo()
        assert "No hay muebles en el inventario" in salida(menu_vacio)

    def test_catalogo_con_muebles(self, menu):
        menu.mostrar_catalogo_completo()
        texto = salida(menu)
        assert "Silla Básica" in texto
        assert "$209.60" in texto
        assert "Sofa" in texto

    def test_catalogo_mueble_con_error(self, menu, mueble_mock):
        mueble_mock.calcular_precio.side_effect = RuntimeError
        menu.tienda._inventario.append(mueble_mock)
        menu.mostrar_catalogo_completo()
        assert "Error" in salida(menu)


class TestBusqueda:
    @patch("ui.menu.Prompt.ask", return_value="silla")
    def test_busqueda_con_resultados(self, _ask, menu):
        menu.buscar_muebles_interactivo()
        assert "Se encontraron 1 resultado(s)" in salida(menu)

    @patch("ui.menu.Prompt.ask", return_value="lampara")
    def test_busqueda_sin_resultados(self, _ask, menu):
        menu.buscar_muebles_interactivo()
        assert "No se encontraron muebles que contengan 'lampara'" in salida(menu)

    @patch("ui.menu.Prompt.ask", return_value="   ")
    def test_busqueda_vacia(self, _ask, menu):
        with patch.object(menu.tienda, "buscar_muebles_por_nombre") as buscar:
            menu.buscar_muebles_interactivo()
        buscar.assert_not_called()
        assert "Término de búsqueda vacío" in salida(menu)


class TestFiltroPrecio:
    @patch("ui.menu.IntPrompt.ask", side_effect=[100, 300])
    def test_con_resultados(self, _ask, menu):
        menu.filtrar_por_precio_interactivo()
        assert "Se encontraron 2 mueble(s) en el rango" in salida(menu)

    @patch("ui.menu.IntPrompt.ask", side_effect=[0, 0])
    def test_maximo_cero_es_sin_limite(self, _ask, menu):
        with patch.object(
            menu.tienda, "filtrar_por_precio", return_value=[]
        ) as filtrar:
            menu.filtrar_por_precio_interactivo()
        filtrar.assert_called_once_with(0, float("inf"))

    @patch("ui.menu.IntPrompt.ask", side_effect=[5000, 6000])
    def test_sin_resultados(self, _ask, menu):
        menu.filtrar_por_precio_interactivo()
        assert "No hay muebles en el rango" in salida(menu)

    @patch("ui.menu.IntPrompt.ask", side_effect=[500, 100])
    def test_minimo_mayor_que_maximo(self, _ask, menu):
        menu.filtrar_por_precio_interactivo()
        assert "El precio mínimo no puede ser mayor al máximo" in salida(menu)


class TestFiltroMaterial:
    @patch("ui.menu.Prompt.ask", return_value="madera")
    def test_con_resultados(self, _ask, menu):
        menu.filtrar_por_material_interactivo()
        assert "Muebles de madera encontrados" in salida(menu)

    @patch("ui.menu.Prompt.ask", return_value="oro")
    def test_sin_resultados(self, _ask, menu):
        menu.filtrar_por_material_interactivo()
        assert "No hay muebles de material 'oro'" in salida(menu)

    @patch("ui.menu.Prompt.ask", return_value="")
    def test_vacio(self, _ask, menu):
        menu.filtrar_por_material_interactivo()
        assert "Material no puede estar vacío" in salida(menu)


class TestComedores:
    def test_sin_comedores(self, menu):
        menu.mostrar_comedores()
        assert "No hay comedores disponibles" in salida(menu)

    def test_con_comedores(self, menu, comedor_basico):
        menu.tienda.agregar_comedor(comedor_basico)
        menu.mostrar_comedores()
        assert "Comedor #1" in salida(menu)
        assert "COMEDOR FAMILIAR" in salida(menu)


class TestVenta:
    def test_sin_inventario(self, menu_vacio):
        menu_vacio.realizar_venta_interactiva()
        assert "No hay muebles disponibles para venta" in salida(menu_vacio)

    @patch("ui.menu.Prompt.ask", return_value="Ana")
    @patch("ui.menu.Confirm.ask", return_value=True)
    @patch("ui.menu.IntPrompt.ask", return_value=1)
    def test_venta_exitosa(self, _int, _confirm, _prompt, menu):
        menu.realizar_venta_interactiva()
        texto = salida(menu)
        assert "COMPROBANTE DE VENTA" in texto
        assert "Cliente: Ana" in texto
        assert "PRECIO FINAL: $110.00" in texto
        assert len(menu.tienda._inventario) == 2

    @patch("ui.menu.Confirm.ask", return_value=False)
    @patch("ui.menu.IntPrompt.ask", return_value=1)
    def test_venta_cancelada(self, _int, _confirm, menu):
        menu.realizar_venta_interactiva()
        assert "Venta cancelada" in salida(menu)
        assert len(menu.tienda._inventario) == 3

    @patch("ui.menu.Prompt.ask", return_value="Ana")
    @patch("ui.menu.Confirm.ask", return_value=True)
    @patch("ui.menu.IntPrompt.ask", return_value=1)
    def test_venta_con_error(self, _int, _confirm, _prompt, menu):
        with patch.object(
            menu.tienda, "realizar_venta", return_value={"error": "sin stock"}
        ):
            menu.realizar_venta_interactiva()
        assert "Error: sin stock" in salida(menu)

    @pytest.mark.parametrize("error", [ValueError, IndexError])
    def test_seleccion_invalida(self, menu, error):
        with patch("ui.menu.IntPrompt.ask", side_effect=error):
            menu.realizar_venta_interactiva()
        assert "Selección inválida" in salida(menu)


class TestEstadisticasYReporte:
    def test_mostrar_estadisticas(self, menu):
        menu.mostrar_estadisticas()
        texto = salida(menu)
        assert "Total de muebles" in texto
        assert "$1669.60" in texto
        assert "Silla: 1 unidades" in texto

    def test_estadisticas_invalidas(self, menu):
        with patch.object(menu.tienda, "obtener_estadisticas", return_value=None):
            menu.mostrar_estadisticas()
        texto = salida(menu)
        assert "$0.00" in texto
        assert "Distribución por tipos" not in texto

    @patch("ui.menu.Confirm.ask", return_value=False)
    def test_reporte_sin_guardar(self, _confirm, menu):
        menu.generar_reporte_interactivo()
        assert "REPORTE DE INVENTARIO" in salida(menu)

    @patch("ui.menu.Confirm.ask", return_value=True)
    def test_reporte_guardado(self, _confirm, menu, tmp_path):
        archivo = tmp_path / "reporte.txt"
        with patch("ui.menu.Prompt.ask", return_value=str(archivo)):
            menu.generar_reporte_interactivo()
        assert "Reporte guardado en" in salida(menu)
        assert "Total de muebles: 3" in archivo.read_text(encoding="utf-8")

    @patch("ui.menu.Confirm.ask", return_value=True)
    def test_reporte_error_al_guardar(self, _confirm, menu, tmp_path):
        # Un directorio no se puede abrir como archivo
        with patch("ui.menu.Prompt.ask", return_value=str(tmp_path)):
            menu.generar_reporte_interactivo()
        assert "Error al guardar" in salida(menu)


class TestDescuentos:
    @patch("ui.menu.IntPrompt.ask", side_effect=[1, 10])
    def test_aplicar_descuento(self, _ask, menu):
        menu.aplicar_descuentos_interactivo()
        assert menu.tienda._descuentos_activos == {"Silla": 0.1}
        assert "Descuento del 10% aplicado" in salida(menu)

    @patch("ui.menu.IntPrompt.ask", side_effect=ValueError)
    def test_seleccion_invalida(self, _ask, menu):
        menu.aplicar_descuentos_interactivo()
        assert "Selección inválida" in salida(menu)


class TestListaMuebles:
    @pytest.mark.parametrize("numerada", [True, False])
    def test_mueble_con_error_de_precio(self, menu, mueble_mock, numerada):
        mueble_mock.calcular_precio.side_effect = RuntimeError
        menu._mostrar_lista_muebles([mueble_mock], numerada=numerada)
        texto = salida(menu)
        assert "Mueble Mock" in texto
        assert "Error" in texto


class TestMenuPrincipal:
    @patch("ui.menu.IntPrompt.ask", return_value=3)
    def test_devuelve_opcion(self, _ask, menu):
        assert menu.mostrar_menu_principal() == 3
        assert "MENÚ PRINCIPAL" in salida(menu)

    @patch("ui.menu.IntPrompt.ask", side_effect=[ValueError, 5])
    def test_reintenta_si_opcion_invalida(self, _ask, menu):
        assert menu.mostrar_menu_principal() == 5
        assert "Opción inválida" in salida(menu)


class TestEjecutar:
    ACCIONES = {
        1: "mostrar_catalogo_completo",
        2: "buscar_muebles_interactivo",
        3: "filtrar_por_precio_interactivo",
        4: "filtrar_por_material_interactivo",
        5: "mostrar_comedores",
        6: "realizar_venta_interactiva",
        7: "mostrar_estadisticas",
        8: "generar_reporte_interactivo",
        9: "aplicar_descuentos_interactivo",
    }

    @patch("builtins.input", return_value="")
    def test_despacha_cada_opcion_y_sale(self, mock_input, menu):
        acciones = {nombre: Mock() for nombre in self.ACCIONES.values()}
        for nombre, mock in acciones.items():
            setattr(menu, nombre, mock)
        menu.mostrar_menu_principal = Mock(side_effect=[*self.ACCIONES, 0])

        menu.ejecutar()

        for mock in acciones.values():
            mock.assert_called_once_with()
        assert menu.running is False
        assert mock_input.call_count == 9  # una pausa por opción, ninguna al salir
        assert "Hasta luego" in salida(menu)

    @patch("builtins.input", return_value="")
    def test_opcion_desconocida_no_hace_nada(self, mock_input, menu):
        menu.mostrar_menu_principal = Mock(side_effect=[42, 0])
        menu.ejecutar()
        mock_input.assert_called_once()

    def test_keyboard_interrupt(self, menu):
        menu.mostrar_menu_principal = Mock(side_effect=KeyboardInterrupt)
        menu.ejecutar()
        assert menu.running is False
        assert "Operación cancelada por el usuario" in salida(menu)

    @patch("builtins.input", return_value="")
    def test_error_inesperado_continua(self, mock_input, menu):
        menu.mostrar_menu_principal = Mock(side_effect=[RuntimeError("boom"), 0])
        menu.ejecutar()
        assert "Error inesperado: boom" in salida(menu)
        mock_input.assert_called_once()
