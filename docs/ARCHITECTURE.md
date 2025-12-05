# 🏗️ Arquitectura del TEF Preparation System

## Introducción

Este documento describe la arquitectura de alto nivel del TEF Preparation System, un proyecto diseñado con una estructura de monorepo para facilitar la escalabilidad, la separación de conceptos y el desarrollo de múltiples interfaces de usuario (UIs).

## 🎯 Principios de Diseño

- **Modularidad**: El sistema está dividido en módulos independientes con responsabilidades claras.
- **Separación de Conceptos (SoC)**: La lógica de negocio (core), las UIs y los datos están estrictamente separados.
- **Escalabilidad**: La arquitectura permite añadir nuevas aplicaciones (ej. API, otras UIs) sin afectar los componentes existentes.
- **Reusabilidad**: El módulo `core` es un paquete Python que puede ser importado y utilizado por cualquier otra parte del sistema.

## 📂 Estructura del Monorepo

La estructura de directorios está organizada de la siguiente manera:

```
TEF-Prep/
├── core/                    # El "cerebro" - lógica de negocio principal
├── api/                     # Futuro wrapper de API (FastAPI)
├── streamlit/               # UI del MVP (Streamlit)
├── data/                    # Datos de entrada, salida y logs
├── tests/                   # Pruebas para todos los módulos
├── docs/                    # Documentación del proyecto
├── README.md                # README principal
└── ...                      # Otros archivos de configuración (gitignore, requirements)
```

### Módulo `core`

- **Responsabilidad**: Contiene toda la lógica de negocio del sistema. Es el "cerebro" que orquesta a los agentes de IA y ejecuta los workflows de evaluación y mejora.
- **Contenido**:
    - `agents/`: Definiciones y prompts de los agentes especializados.
    - `config/`: Archivos de configuración del sistema y de los agentes.
    - `scripts/`: Utilidades para la administración del sistema.
    - `workflows/`: Lógica de coordinación entre agentes.
    - `tef_system.py`: El controlador principal que expone la funcionalidad del sistema.
    - `__init__.py`: Convierte al directorio `core` en un paquete Python importable.

### Módulo `api`

- **Responsabilidad**: Exponer la funcionalidad del módulo `core` a través de una API RESTful. Esto permitirá que clientes de terceros (ej. aplicaciones web, móviles) interactúen con el sistema.
- **Tecnología**: FastAPI (planeado).
- **Estado Actual**: Placeholder.

### Módulo `streamlit`

- **Responsabilidad**: Proporcionar una interfaz de usuario rápida y sencilla para interactuar con el sistema. Es el MVP (Minimum Viable Product) para la validación de la funcionalidad principal.
- **Tecnología**: Streamlit.
- **Estado Actual**: Placeholder.

### Directorio `data`

- **Responsabilidad**: Almacenar todos los datos persistentes que el sistema utiliza o genera.
- **Contenido**:
    - `inputs/`: Escritos de los estudiantes para ser evaluados.
    - `outputs/`: Resultados generados por el sistema (feedback, planes de estudio).
    - `logs/`: Logs de ejecución para depuración y seguimiento.

### Directorio `tests`

- **Responsabilidad**: Contener todas las pruebas (unitarias, de integración, funcionales) para asegurar la calidad y el correcto funcionamiento de todos los módulos.
- **Estructura**: Refleja la estructura de los otros módulos (`tests/core`, `tests/api`, etc.).

## 🤝 Contratos de API entre Módulos

La comunicación entre los módulos de UI (como `streamlit` o `api`) y el módulo `core` se realiza a través de la importación y el uso de la clase `TEFSystem`.

```python
# Ejemplo de cómo una UI podría usar el módulo core

from core.tef_system import TEFSystem

# 1. Inicializar el sistema
tef_sys = TEFSystem()

# 2. Ejecutar una evaluación
feedback = tef_sys.evaluate_writing("ruta/a/un/escrito.txt")

# 3. Generar un plan de mejora
plan = tef_sys.improve_plan("ruta/a/un/feedback.json", mode="normal")
```

Esta arquitectura asegura que cualquier cambio en la lógica interna de los agentes o workflows dentro de `core` no requerirá cambios en las UIs, siempre que la firma de los métodos públicos de `TEFSystem` se mantenga estable.

## 🚀 Cómo Agregar Nuevas UIs

Para agregar una nueva interfaz (por ejemplo, una aplicación de escritorio con Tkinter o una app web con Flask), los pasos serían:

1.  **Crear un nuevo directorio** en la raíz del proyecto (ej. `desktop_app/`).
2.  **Añadir sus propias dependencias** en un archivo `requirements.txt` dentro de ese directorio.
3.  **Importar y utilizar `TEFSystem`** desde el módulo `core` para acceder a la lógica de negocio.

Esta estructura promueve un desarrollo limpio y desacoplado, permitiendo que el proyecto crezca de manera ordenada.
