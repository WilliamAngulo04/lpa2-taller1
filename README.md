# LPA2 Taller1: Pruebas Unitarias Tienda de Muebles

![commits](https://badgen.net/github/commits/UR-CC/lpa2-taller1?icon=github) 
![last_commit](https://img.shields.io/github/last-commit/UR-CC/lpa2-taller1)

## Objetivos

- Aplicar **pruebas unitarias** con `pytest`
- Implementar **mocks y fixtures** para aislar dependencias
- Medir y analizar **cobertura de código** con `pytest-cov`
- Aplicar **Test-Driven Development (TDD)** en nuevas funcionalidades
- Diseñar pruebas para **clases abstractas y herencia**
- Crear pruebas para **composición y herencia múltiple**
- Implementar **pruebas de integración** básicas

## Prerrequisitos

- Conocimientos de OOP con Python
- Familiaridad con los conceptos de abstracción, herencia, polimorfismo

## Estructura del Proyecto

```
lpa2-taller1/
├─ src/                   # Código del proyecto
├─ tests/
│  ├─ fixtures/          # Datos de prueba
│  ├─ unit/              # Pruebas unitarias
│  │  ├─ conftest.py     # Configuración compartida
│  │  └─ models/
│  │     ├─ test_mueble.py
│  │     ├─ categorias/
│  │     │  ├─ test_almacenamiento.py
│  │     │  ├─ test_asientos.py
│  │     │  └─ test_superficies.py
│  │     ├─ concretos/
│  │     │  ├─ test_armario.py
│  │     │  ├─ test_cajonera.py
│  │     │  ├─ test_cama.py
│  │     │  ├─ test_comedor.py
│  │     │  ├─ test_escritorio.py
│  │     │  ├─ test_mesa.py
│  │     │  ├─ test_silla.py
│  │     │  ├─ test_sillon.py
│  │     │  ├─ test_sofa.py
│  │     │  └─ test_sofacama.py
│  │     └─ composicion/
│  │        └─ test_comedor.py
│  └─ integration/       # Pruebas de integración
├─ .coveragerc           # Configuración de cobertura
└─ pytest.ini            # Configuración de pytest
```

## Configuración del Entorno

### Preparación del Proyecto

- Crear un **fork** del repo `https://github.com/UR-CC/lpa2-taller1` en la cuenta GitHub del estudiante.

- Abrir una terminal de comandos.

- Crear un directorio para los **proyectos**:

    ```bash
    mkdir proyectos
    cd proyectos
    ```

- Clonar el repo del estudiante:

    ```bash
    git clone https://github.com/usuario/lpa2-taller1.git
    cd lpa2-taller1
    ```

- Crear entorno virtual - en Ubuntu utiliza `python3`:

    ```bash
    python -m venv venv
    source venv/bin/activate # Mac/Linux/WSL
    pip install -r requirements.txt
    ```

### Configurar Pytest

Archivo `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --color=yes
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-branch
pythonpath = . src tests
filterwarnings =
    ignore::DeprecationWarning
```

### Configurar Cobertura

Archivo `.coveragerc`:

```ini
[run]
source = src
omit = 
    */__pycache__/*
    */tests/*
    */venv/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    pass

fail_under = 80
```

## Diseño de Pruebas Unitarias

### Filosofía de las Pruebas

**Principios AAA (Arrange-Act-Assert):**

```python
def test_nombre_del_test():
    # Arrange: Preparar el escenario
    objeto = Clase(parametro=valor)
    
    # Act: Ejecutar la acción a probar
    resultado = objeto.metodo()
    
    # Assert: Verificar el resultado
    assert resultado == valor_esperado
```

**Patrones Comunes:**

- Una prueba por escenario
- Nombres descriptivos para tests
- Tests independientes y aislados
- Mockear dependencias externas

### Pruebas para Clases Abstractas

**tests/unit/models/test_mueble.py:**

```python
import pytest
from abc import ABC
from src.models.mueble import Mueble

class TestMueble:
    def test_es_clase_abstracta(self):
        # Verificar que Mueble es abstracta
        with pytest.raises(TypeError):
            mueble = Mueble("Mesa", "Madera", 100.0)
    
    def test_tiene_metodos_abstractos(self):
        # Verificar que tiene métodos abstractos
        assert hasattr(Mueble, 'calcular_precio')
        assert hasattr(Mueble, 'obtener_descripcion')
        
        # Verificar que son abstractos
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__
```

### Pruebas para Herencia

**tests/unit/models/concretos/test_silla.py:**

```python
import pytest
from src.models.concretos.silla import Silla

class TestSilla:
    @pytest.fixture
    def silla_basica(self):
        return Silla("Silla Básica", "Madera", 50.0, 4, "Madera")
    
    def test_instanciacion_correcta(self, silla_basica):
        # Verificar herencia de atributos
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.precio_base == 50.0
        
        # Verificar atributos específicos
        assert silla_basica.numero_patas == 4
        assert silla_basica.tipo_madera == "Madera"
    
    def test_calcular_precio(self, silla_basica):
        # Probar polimorfismo
        precio = silla_basica.calcular_precio()
        assert precio == 50.0  # Precio base sin modificaciones
    
    def test_obtener_descripcion(self, silla_basica):
        descripcion = silla_basica.obtener_descripcion()
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion
```

### Pruebas para Herencia Múltiple

**tests/unit/models/concretos/test_sofacama.py:**

```python
import pytest
from src.models.concretos.sofacama import SofaCama

class TestSofaCama:
    def test_herencia_multiple(self):
        sofa_cama = SofaCama("Sofá Cama Moderno", "Tela", 500.0, 3, "Queen")
        
        # Verificar atributos de Sofa
        assert sofa_cama.capacidad_personas == 3
        
        # Verificar atributos de Cama
        assert sofa_cama.tamaño_colchon == "Queen"
        
        # Verificar método específico
        assert hasattr(sofa_cama, 'transformar')
    
    def test_resolucion_metodos(self):
        sofa_cama = SofaCama("Sofá Cama", "Cuero", 600.0, 2, "Full")
        
        # Verificar que usa el método correcto (MRO)
        precio = sofa_cama.calcular_precio()
        assert precio > 600.0  # Debe incluir recargos de ambas clases
```

### Pruebas para Composición

**tests/unit/models/composicion/test_comedor.py:**

```python
import pytest
from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla

class TestComedor:
    @pytest.fixture
    def comedor_basico(self):
        mesa = Mesa("Mesa Comedor", "Roble", 200.0, "Rectangular", 6)
        sillas = [Silla("Silla Comedor", "Roble", 50.0, 4, "Roble") for _ in range(6)]
        return Comedor("Comedor Familiar", mesa, sillas)
    
    def test_composicion_correcta(self, comedor_basico):
        assert comedor_basico.mesa is not None
        assert len(comedor_basico.sillas) == 6
        assert isinstance(comedor_basico.mesa, Mesa)
        assert all(isinstance(silla, Silla) for silla in comedor_basico.sillas)
    
    def test_calcular_precio_total(self, comedor_basico):
        precio_total = comedor_basico.calcular_precio()
        precio_esperado = 200.0 + (6 * 50.0)  # Mesa + 6 sillas
        assert precio_total == precio_esperado
```

### Pruebas con Mocks

**tests/unit/services/test_tienda.py:**

```python
import pytest
from unittest.mock import Mock, patch
from src.services.tienda import Tienda
from src.models.concretos.silla import Silla

class TestTienda:
    @pytest.fixture
    def tienda_vacia(self):
        return Tienda()
    
    @pytest.fixture
    def silla_mock(self):
        mock_silla = Mock(spec=Silla)
        mock_silla.nombre = "Silla Mock"
        mock_silla.calcular_precio.return_value = 75.0
        return mock_silla
    
    def test_agregar_producto(self, tienda_vacia, silla_mock):
        tienda_vacia.agregar_producto(silla_mock)
        assert len(tienda_vacia.inventario) == 1
        assert tienda_vacia.inventario[0] == silla_mock
    
    def test_vender_producto_existente(self, tienda_vacia, silla_mock):
        tienda_vacia.agregar_producto(silla_mock)
        
        with patch('builtins.print') as mock_print:
            resultado = tienda_vacia.vender_producto("Silla Mock")
            
            assert resultado is True
            assert len(tienda_vacia.inventario) == 0
            mock_print.assert_called_once()
    
    def test_vender_producto_inexistente(self, tienda_vacia):
        resultado = tienda_vacia.vender_producto("Producto Inexistente")
        assert resultado is False
```

## Ejecución de Pruebas

### Comandos Básicos

- Configurar la variable de entorno `PYTHONPATH`:

    ```bash
    export PYTHONPATH=.
    ```

- Ejecutar todas las pruebas, `-v` en modo *verbose*:

    ```bash
    pytest -v
    ```

- Ejecutar pruebas con cobertura detallada

    ```bash
    pytest --cov=src --cov-report=html
    ```

- Ejecutar pruebas específicas

    ```bash
    pytest tests/unit/models/ -v
    ```

- Ejecutar pruebas y mostrar cobertura en terminal

    ```bash
    pytest --cov=src --cov-report=term-missing
    ```

- Ejecutar pruebas marcadas como rápidas

    ```bash
    pytest -m "not slow"
    ```

### Marcadores de Pruebas

**tests/conftest.py:**

```python
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
```

**Uso en pruebas:**

```python
@pytest.mark.slow
def test_proceso_lento():
    # Esta prueba se puede saltar con pytest -m "not slow"
    pass

@pytest.mark.integration
def test_integracion_completa():
    # Prueba de integración
    pass
```

## Estrategias de Pruebas

### 1. Test-Driven Development (TDD)

**Ciclo Red-Green-Refactor:**

1. **RED**: Escribir prueba que falle
2. **GREEN**: Implementar mínimo código para pasar
3. **REFACTOR**: Mejorar el código manteniendo pruebas

**Ejemplo - Nueva funcionalidad de descuentos:**

```python
# tests/unit/services/test_descuentos.py
def test_aplicar_descuento_por_material():
    # RED: Escribir prueba primero
    tienda = Tienda()
    silla = Silla("Silla", "Roble", 100.0, 4, "Roble")
    
    tienda.agregar_producto(silla)
    tienda.aplicar_descuento_material("Roble", 0.1)  # 10% descuento
    
    assert silla.precio_base == 90.0  # Esta prueba fallará inicialmente
```

### 2. Categorías de Pruebas

| Tipo | Objetivo | Ejemplo |
|------|----------|---------|
| **Unitarias** | Probar unidades individuales | `test_silla_calcular_precio()` |
| **Integración** | Probar interacción entre módulos | `test_tienda_con_catalogo()` |
| **Fixtures** | Datos de prueba reutilizables | `@pytest.fixture def silla_basica()` |
| **Mocks** | Simular dependencias externas | `@patch('services.tienda.print')` |

### 3. Patrones de Diseño para Pruebas

**Fixture para datos complejos:**

```python
@pytest.fixture
def comedor_completo():
    mesa = Mesa("Mesa Roble", "Roble", 300.0, "Rectangular", 8)
    sillas = [Silla("Silla Roble", "Roble", 80.0, 4, "Roble") for _ in range(8)]
    return Comedor("Comedor Grande", mesa, sillas)

def test_comedor_precio(comedor_completo):
    precio = comedor_completo.calcular_precio()
    assert precio == 300.0 + (8 * 80.0)
```

**Parámetros para múltiples escenarios:**

```python
@pytest.mark.parametrize("material,precio_base,esperado", [
    ("Madera", 100.0, 100.0),
    ("Roble", 150.0, 150.0),
    ("Metal", 120.0, 120.0),
])
def test_silla_precios_diferentes_materiales(material, precio_base, esperado):
    silla = Silla(f"Silla {material}", material, precio_base, 4, material)
    assert silla.calcular_precio() == esperado
```

## Análisis de Cobertura

### Interpretar Reportes de Cobertura

```bash
# Generar reporte HTML
pytest --cov=src --cov-report=html

# Abrir reporte
open htmlcov/index.html
```

**Métricas importantes:**

- **Cobertura total**: Porcentaje general de código cubierto
- **Líneas cubiertas**: Líneas ejecutadas durante pruebas
- **Líneas missing**: Líneas que necesitan pruebas
- **Branch coverage**: Cobertura de ramas condicionales

### Mejorar Cobertura

**Identificar gaps:**

```bash
pytest --cov=src --cov-report=term-missing
```

**Ejemplo de salida:**

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/models/mueble.py       15      3    80%   22-24
src/services/tienda.py     45     10    78%   15-18, 33-39
```

## Entregables

El estudiante debe actualizar su repositorio personal con:

1. **Estructura de pruebas completa** organizada por módulos
2. **Cobertura mínima del 80%** en todos los módulos principales
3. **Pruebas para casos edge** y condiciones de error
4. **Fixtures y mocks** para pruebas aisladas
5. **Reporte de cobertura** HTML generado
6. **README actualizado** con instrucciones de ejecución

## Instrucciones de Ejecución (Entrega)

> Nota: el código fuente importa los módulos como `models...`, `services...` y `ui...`
> (sin el prefijo `src.`), por lo que las pruebas usan ese mismo estilo de import.
> `pytest.ini` agrega `src` al `pythonpath`, así que no hace falta exportar `PYTHONPATH`.

1. Crear y activar el entorno virtual e instalar dependencias:

    ```bash
    python -m venv venv
    source venv/bin/activate      # Mac/Linux/WSL
    venv\Scripts\activate         # Windows (PowerShell / cmd)
    pip install -r requirements.txt
    ```

2. Ejecutar toda la suite (incluye cobertura en terminal y HTML en `htmlcov/`):

    ```bash
    pytest
    ```

3. Ejecutar subconjuntos:

    ```bash
    pytest tests/unit                 # solo unitarias
    pytest -m integration             # solo integración
    pytest -m "not slow"              # omitir pruebas lentas
    pytest tests/unit/services -v     # un módulo específico
    ```

4. Ejecutar la aplicación interactiva:

    ```bash
    python src/main.py
    ```

### Organización de las pruebas

| Ubicación | Contenido |
|-----------|-----------|
| `tests/conftest.py` | Registro de marcadores `slow` e `integration` |
| `tests/fixtures/datos_muebles.py` | Datos de prueba reutilizables |
| `tests/unit/conftest.py` | Fixtures compartidas (sillas, mesas, comedores, tiendas, mocks) |
| `tests/unit/models/` | Clase abstracta, categorías, concretos, herencia múltiple y composición |
| `tests/unit/services/test_tienda.py` | Lógica de negocio con mocks + funcionalidades desarrolladas con TDD |
| `tests/unit/ui/test_menu.py` | Menú Rich con entradas simuladas (`Prompt`, `IntPrompt`, `Confirm`, `input`) |
| `tests/unit/test_main.py` | Punto de entrada `main.py` |
| `tests/integration/` | Flujos completos: catálogo de ejemplo, ventas, descuentos y sesión de menú |

### Funcionalidades desarrolladas con TDD

En `TiendaMuebles` se implementaron, escribiendo primero las pruebas (RED → GREEN):

- `obtener_muebles_por_tipo(tipo_clase)`: filtra por clase, incluyendo subclases.
- `calcular_valor_inventario()`: suma muebles y comedores, ignorando elementos con error.
- `_contar_tipos_muebles()`: conteo de muebles por nombre de clase.
- `aplicar_descuento_material(material, porcentaje)`: reduce el `precio_base` de los muebles de un material (`porcentaje` entre 0 y 1, ej. `0.1` = 10%).

## Recursos Adicionales

### Documentación Oficial

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Coverage](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

### Mejores Prácticas

- Escribir pruebas independientes y rápidas
- Usar nombres descriptivos para tests
- Probar tanto el éxito como los casos de error
- Mantener las pruebas actualizadas con el código
- Usar fixtures para datos de prueba complejos

### Comandos Útiles

- Ejecutar pruebas y generar badge de cobertura

    ```bash
    pytest --cov=src --cov-report=term-missing --cov-badge
    ```

- Ejecutar pruebas en paralelo

    ```bash
    pytest -n auto
    ```

- Ver tiempo de ejecución de pruebas

    ```bash
    pytest --durations=10
    ```

**Nota**: repo [solución al proyecto Muebles](https://github.com/axlcraft/lpa1-taller-poo).

