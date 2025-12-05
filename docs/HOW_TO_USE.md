# Cómo Usar el TEF Preparation System

Esta guía explica cómo utilizar los comandos disponibles en el sistema de preparación para el TEF.

## Comandos Disponibles

A continuación se detallan los comandos que están implementados y listos para usar.

---

### 1. `evaluate`

**Propósito:** Evalúa un texto escrito por un estudiante. Opera en dos modos:
1.  **Detección Automática:** Si no se especifica un nivel, el sistema detecta el nivel del estudiante y lo evalúa contra el siguiente nivel de la escala CEFR.
2.  **Evaluación contra Objetivo:** Si se especifica un nivel, el sistema evalúa el texto directamente contra ese estándar.

**Uso:**
```bash
# Modo Detección Automática
python -m core.tef_system evaluate --input RUTA_AL_ARCHIVO

# Modo Evaluación contra Objetivo
python -m core.tef_system evaluate --input RUTA_AL_ARCHIVO --level NIVEL_OBJETIVO
```

**Argumentos:**
- `--input` (obligatorio): La ruta al archivo de texto (`.txt`) que contiene el escrito del estudiante.
- `--level` (opcional): El nivel TEF objetivo para la evaluación (ej. B2). Si se omite, se activa la detección automática.

**Ejemplo (Detección Automática):**
```bash
python -m core.tef_system evaluate --input="data/inputs/student_writings/texto1_a2.txt"
```

**Ejemplo (Evaluación contra Objetivo):**
```bash
python -m core.tef_system evaluate --input="data/inputs/student_writings/texto1_a2.txt" --level="B1"
```

**Resultado:**
Genera un archivo JSON en la carpeta `data/outputs/feedback/` con una evaluación detallada, que incluye el modo de evaluación, el nivel detectado, el nivel objetivo y un análisis de la brecha de competencias.

---

### 2. `research`

**Propósito:** Busca recursos de estudio online sobre un tema, nivel y competencia específicos.

**Uso:**
```bash
python -m core.tef_system research --topic TEMA --level NIVEL --competency COMPETENCIA
```

**Argumentos:**
- `--topic`: El tema de gramática, vocabulario o habilidad que se desea investigar (ej. "subjonctif", "connecteurs logiques").
- `--level`: El nivel de dificultad para el cual se buscan los recursos (ej. A1, A2, B1, B2).
- `--competency`: El área de habilidad específica (ej. "grammaire", "vocabulaire", "expression écrite").

**Ejemplo:**
```bash
python -m core.tef_system research --topic="subjonctif" --level="B2" --competency="grammaire"
```

**Resultado:**
El comando imprime en la consola una lista de hasta 10 URLs de recursos de alta calidad (artículos, ejercicios, videos) relacionados con el tema solicitado.

---

### 3. `improve`

**Propósito:** Genera un plan de estudio personalizado y enriquecido con recursos, basándose en un archivo de feedback. El plan puede ser `normal` o `intensive`.

**Uso:**
```bash
python -m core.tef_system improve --feedback RUTA_AL_FEEDBACK.json [--mode MODO]
```

**Argumentos:**
- `--feedback` (obligatorio): La ruta al archivo JSON de feedback generado por el comando `evaluate`.
- `--mode` (opcional): El modo del plan de estudio. Opciones: `normal` (default) o `intensive`.

**Ejemplo (Modo Normal):**
```bash
python -m core.tef_system improve --feedback="data/outputs/feedback/mi_feedback.json"
```

**Ejemplo (Modo Intensivo):**
```bash
python -m core.tef_system improve --feedback="data/outputs/feedback/mi_feedback.json" --mode="intensive"
```

**Resultado:**
Genera un archivo Markdown (`.md`) con un plan de estudio detallado de 3 semanas en `data/outputs/study_plans/`. La cantidad de actividades y la intensidad del plan variarán según el modo seleccionado. El archivo final también incluirá una sección `## 📚 Recursos Recomendados` con enlaces relevantes.
