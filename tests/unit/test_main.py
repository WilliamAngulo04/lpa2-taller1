"""
Pruebas del punto de entrada main.py.
"""

from unittest.mock import patch

import pytest

import main
from services.tienda import TiendaMuebles


@pytest.fixture
def tienda():
    return TiendaMuebles("Tienda Main")


class TestFuncionesDeArranque:
    def test_crear_catalogo_inicial(self, tienda, capsys):
        main.crear_catalogo_inicial(tienda)
        assert len(tienda._inventario) > 0
        assert "Catálogo inicial creado con éxito" in capsys.readouterr().out

    def test_crear_comedores_ejemplo(self, tienda):
        main.crear_comedores_ejemplo(tienda)
        assert [c.nombre for c in tienda._comedores] == [
            "Comedor Familiar Completo",
            "Comedor Moderno Premium",
        ]

    def test_aplicar_descuentos_ejemplo(self, tienda):
        main.aplicar_descuentos_ejemplo(tienda)
        assert tienda._descuentos_activos == {"Silla": 0.10, "Mesa": 0.15, "Sofa": 0.20}

    def test_mostrar_estadisticas_iniciales(self, tienda, capsys):
        main.crear_catalogo_inicial(tienda)
        main.mostrar_estadisticas_iniciales(tienda)
        out = capsys.readouterr().out
        assert "Total de muebles" in out
        assert "Silla: 3 unidades" in out


class TestMain:
    @patch("main.MenuTienda")
    @patch("builtins.input", return_value="")
    def test_flujo_normal(self, _input, mock_menu, capsys):
        main.main()
        mock_menu.assert_called_once()
        tienda = mock_menu.call_args.args[0]
        assert isinstance(tienda, TiendaMuebles)
        assert tienda.nombre == "Mueblería Moderna OOP"
        mock_menu.return_value.ejecutar.assert_called_once()
        assert "Programa finalizado" in capsys.readouterr().out

    @patch("main.MenuTienda")
    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_interrupcion_usuario(self, _input, mock_menu, capsys):
        main.main()
        mock_menu.return_value.ejecutar.assert_not_called()
        out = capsys.readouterr().out
        assert "Programa interrumpido por el usuario" in out
        assert "Programa finalizado" in out

    @patch("main.TiendaMuebles", side_effect=RuntimeError("fallo"))
    def test_error_inesperado(self, _tienda, capsys):
        main.main()
        captured = capsys.readouterr()
        assert "Error inesperado: fallo" in captured.out
        assert "RuntimeError" in captured.err  # traceback impreso
        assert "Programa finalizado" in captured.out
