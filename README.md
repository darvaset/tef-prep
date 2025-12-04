# 🇫🇷 TEF Preparation System

## 📖 Descripción

Sistema inteligente de preparación para el **Test d'Évaluation de Français (TEF)** basado en agentes AI especializados. Diseñado para proporcionar feedback automatizado, planes de mejora personalizados y recursos de estudio curados para estudiantes que se preparan para el examen TEF.

## 🎯 Propósito

El TEF Preparation System automatiza el proceso de evaluación y mejora en la preparación del examen TEF, proporcionando:

- **Evaluación automatizada** de escritos según criterios oficiales TEF
- **Feedback detallado** con puntuaciones específicas por competencia
- **Planes de estudio personalizados y accionables** basados en áreas de mejora identificadas, **enriquecidos con recursos educativos curados automáticamente.**
- **Investigación automática** de recursos educativos relevantes
- **Knowledge base** con ejemplos y criterios de evaluación

## 🏗️ Arquitectura del Sistema

### 🤖 Agentes Especializados

#### 1. **TEF Writing Validator** (`tef-writing-validator`)
- **Función**: Evaluador certificado TEF especializado en escritura
- **Input**: Texto del estudiante + nivel objetivo (A1-C2)
- **Output**: Feedback estructurado con puntuación y observaciones detalladas
- **Especialización**: Análisis según criterios oficiales TEF, identificación de errores gramaticales y de estructura, aplicando rúbricas detalladas para la precisión.

#### 2. **TEF Knowledge Base** (`tef-knowledge-base`)
- **Función**: Repositorio centralizado de conocimiento TEF
- **Contenido**: Exámenes pasados, guías de evaluación, ejemplos por nivel, criterios específicos
- **Propósito**: Proporcionar contexto autoritativo a otros agentes

#### 3. **TEF Improvement Advisor** (`tef-improvement-advisor`)
- **Función**: Tutor especializado en planes de mejora personalizados
- **Input**: Feedback del validator + perfil del estudiante
- **Output**: Plan de estudio estructurado de 2-4 semanas, **con temas específicos para investigación y enlaces a recursos recomendados.**
- **Especialización**: Identificación de patrones de error, creación de rutas de aprendizaje y **orquestación de búsqueda de recursos.**

#### 4. **TEF Resource Researcher** (`tef-resource-researcher`)
- **Función**: Investigador especializado en recursos TEF de calidad
- **Input**: Tópicos específicos de mejora (tema, nivel, competencia)
- **Output**: Lista curada de recursos online validados (URLs con título)
- **Especialización**: Búsqueda y validación de contenido educativo relevante, **integrándose con el Improvement Advisor para enriquecer los planes de estudio.**

### 🔄 Workflows

El sistema opera mediante workflows que coordinan la interacción entre agentes:

1. **Complete Evaluation Workflow**: (Pendiente de implementación completa)
2. **Evaluación + Plan de Mejora Enriquecido**: El comando `improve` ahora orquesta la evaluación del Validator, la creación del plan del Advisor y la búsqueda de recursos del Researcher, todo en un flujo integrado.

## 🚀 Uso Rápido

```bash
# Inicializar la estructura del proyecto
python init_project.py

# Evaluar un escrito (modo detección automática)
python tef_system.py evaluate --input="inputs/student_writings/mi_ensayo.txt"

# Evaluar un escrito (modo objetivo específico)
python tef_system.py evaluate --input="inputs/student_writings/mi_ensayo.txt" --level="B2"

# Generar plan de mejora enriquecido (modo normal)
python tef_system.py improve --feedback="outputs/feedback/mi_feedback.json"

# Generar plan de mejora enriquecido (modo intensivo)
python tef_system.py improve --feedback="outputs/feedback/mi_feedback.json" --mode="intensive"

# Investigar recursos para un tema específico (uso directo)
python tef_system.py research --topic="subjuntivo" --level="B2"
```

## 📁 Estructura del Proyecto

```
tef-preparation-system/
├── agents/                    # Configuración de agentes especializados
├── workflows/                 # Definición de procesos automatizados
├── inputs/                    # Archivos de entrada (escritos de estudiantes)
├── outputs/                   # Resultados (feedback, planes, recursos)
├── logs/                      # Registro de operaciones del sistema
└── scripts/                   # Herramientas de utilidad y administración
```

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje principal
- **Gemini AI** - Agente principal de evaluación
- **Claude** - Agente de investigación y mejora
- **Web Search APIs** - Investigación de recursos
- **JSON** - Formato de intercambio de datos

## 📋 Requisitos

- Python 3.8 o superior
- API keys para Gemini y Claude (configuración en `.env`)
- Acceso a internet para investigación de recursos

## 🔧 Configuración

1. Clonar el repositorio
2. Ejecutar el script de inicialización: `python init_project.py`
3. Configurar API keys en `.env`
4. Poblar la knowledge base con ejemplos y guías TEF

## 🎓 Casos de Uso

### Para Estudiantes Individuales
- Evaluación automática de escritos de práctica
- Identificación de áreas de mejora específicas
- Obtención de recursos personalizados de estudio

### Para Tutores y Profesores
- Herramienta de evaluación estandarizada
- Generación automática de planes de estudio
- Base de conocimiento centralizada

### Para Centros de Preparación
- Escalabilidad en la evaluación de múltiples estudiantes
- Consistencia en los criterios de evaluación
- Automatización del proceso de feedback

## 📊 Métricas y Seguimiento

El sistema mantiene logs detallados de:
- Evaluaciones realizadas por agente
- Tiempo de procesamiento por tipo de tarea
- Efectividad de recursos recomendados
- Patrones de mejora de estudiantes

## 🔒 Privacidad y Datos

- Los escritos de estudiantes se procesan localmente
- No se almacenan datos personales sensibles
- Los logs pueden configurarse para cumplir GDPR/CCPA

## 🤝 Contribución

Este es un proyecto personal de Diego para automatizar la preparación TEF. Las contribuciones se manejan mediante:
- Issues para bugs o mejoras
- Pull requests con nuevos agentes o workflows
- Documentación de nuevos casos de uso

## 📄 Licencia

Uso personal - Diego's AI Agent Framework

---

**Desarrollado por Diego** | QA Engineering Manager | Bethink Labs
*"Automatizando el aprendizaje, un agente a la vez"*