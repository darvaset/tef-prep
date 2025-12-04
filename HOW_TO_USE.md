# Cómo Usar el TEF Preparation System

Esta guía explica cómo utilizar los comandos disponibles en el sistema de preparación para el TEF.

## Comandos Disponibles

A continuación se detallan los comandos que están implementados y listos para usar.

---

### 1. `evaluate`

**Propósito:** Evalúa un texto escrito por un estudiante para un nivel específico del TEF.

**Uso:**
```bash
python tef_system.py evaluate --input RUTA_AL_ARCHIVO --level NIVEL_OBJETIVO
```

**Argumentos:**
- `--input`: La ruta al archivo de texto (`.txt`) que contiene el escrito del estudiante.
- `--level`: El nivel TEF que el estudiante intenta alcanzar (ej. A1, A2, B1, B2, C1, C2).

**Ejemplo:**
```bash
python tef_system.py evaluate --input="inputs/student_writings/example_carta_a2.txt" --level="A2"
```

**Resultado:**
El comando genera un archivo JSON con una marca de tiempo en la carpeta `outputs/feedback/`. Este archivo contiene una evaluación detallada, puntuaciones por competencia, áreas de mejora y recomendaciones.

---

### 2. `research`

**Propósito:** Busca recursos de estudio online sobre un tema, nivel y competencia específicos.

**Uso:**
```bash
python tef_system.py research --topic TEMA --level NIVEL --competency COMPETENCIA
```

**Argumentos:**
- `--topic`: El tema de gramática, vocabulario o habilidad que se desea investigar (ej. "subjonctif", "connecteurs logiques").
- `--level`: El nivel de dificultad para el cual se buscan los recursos (ej. A1, A2, B1, B2).
- `--competency`: El área de habilidad específica (ej. "grammaire", "vocabulaire", "expression écrite").

**Ejemplo:**
```bash
python tef_system.py research --topic="subjonctif" --level="B2" --competency="grammaire"
```

**Resultado:**
El comando imprime en la consola una lista de hasta 10 URLs de recursos de alta calidad (artículos, ejercicios, videos) relacionados con el tema solicitado.

---

### 3. `improve`

**Propósito:** Genera un plan de estudio personalizado y **enriquecido con recursos educativos recomendados** a partir de un archivo de feedback JSON. Este comando orquesta la inteligencia del `Improvement Advisor` con la capacidad de búsqueda del `Resource Researcher`.

**Uso:**
```bash
python tef_system.py improve --feedback RUTA_AL_FEEDBACK.json
```

**Argumentos:**
- `--feedback`: La ruta al archivo JSON de feedback generado por el comando `evaluate`.

**Ejemplo:**
```bash
python tef_system.py improve --feedback="outputs/feedback/20251203_204559_feedback_texto1_a2.json"
```

**Resultado:**
Genera un archivo Markdown (`.md`) con un plan de estudio detallado de 3 semanas en la carpeta `outputs/study_plans/`. El plan se enfoca en las áreas de mejora y errores identificados en el feedback, y **al final del archivo incluirá una sección `## 📚 Recursos Recomendados` con enlaces a recursos online relevantes.**

```markdown
...
---

## 📚 Recursos Recomendados

### Grammaire: Accord adjectif nom genre nombre (Nivel A2)
- [Título del recurso 1](URL1)
- [Título del recurso 2](URL2)

### Grammaire: Accord sujet verbe passé composé (Nivel A2)
- [Título del recurso 1](URL1)
- ...
```
