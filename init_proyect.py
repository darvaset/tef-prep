#!/usr/bin/env python3
"""
################################################################################
#                                                                              #
#                      ⚠️️   DEPRECATED SCRIPT   ⚠️️                             #
#                                                                              #
#   This script is outdated and does not reflect the new monorepo structure.   #
#   Do not run it. It is kept for historical purposes only.                      #
#                                                                              #
################################################################################

TEF Preparation System - Initialization Script

Este script inicializa toda la estructura de carpetas y archivos base 
del sistema de preparación TEF basado en agentes AI.

Autor: Diego | QA Engineering Manager
Fecha: Noviembre 2025
"""

import os
import json
from pathlib import Path
from datetime import datetime


def create_directory_structure():
    """Crea la estructura completa de directorios del proyecto"""
    
    directories = [
        # Agentes especializados
        "agents/tef-writing-validator",
        "agents/tef-writing-validator/examples",
        "agents/tef-knowledge-base/exams",
        "agents/tef-knowledge-base/guides", 
        "agents/tef-knowledge-base/examples",
        "agents/tef-knowledge-base/criteria",
        "agents/tef-improvement-advisor",
        "agents/tef-improvement-advisor/learning_paths",
        "agents/tef-resource-researcher",
        "agents/tef-resource-researcher/search_templates",
        
        # Workflows de coordinación
        "workflows",
        
        # Inputs y outputs
        "inputs/student_writings",
        "outputs/feedback",
        "outputs/study_plans", 
        "outputs/resources",
        
        # Sistema y utilidades
        "logs/agents",
        "logs/workflows",
        "logs/system",
        "scripts",
        "config",
        
        # Testing y desarrollo
        "tests/unit",
        "tests/integration",
        "tests/fixtures"
    ]
    
    print("🏗️  Creando estructura de directorios...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return len(directories)


def create_base_configuration_files():
    """Crea los archivos de configuración base del sistema"""
    
    # Configuración principal del sistema
    system_config = {
        "system": {
            "name": "TEF Preparation System",
            "version": "1.0.0",
            "author": "Diego - QA Engineering Manager",
            "created": datetime.now().isoformat(),
            "description": "Sistema de agentes AI para preparación del examen TEF"
        },
        "agents": {
            "tef-writing-validator": {
                "enabled": True,
                "model": "gemini-pro",
                "max_tokens": 2000,
                "temperature": 0.1
            },
            "tef-improvement-advisor": {
                "enabled": True,
                "model": "claude-sonnet",
                "max_tokens": 1500,
                "temperature": 0.3
            },
            "tef-resource-researcher": {
                "enabled": True,
                "model": "claude-sonnet",
                "max_tokens": 1000,
                "temperature": 0.2
            }
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/system/tef_system.log"
        }
    }
    
    with open("config/system.json", "w", encoding="utf-8") as f:
        json.dump(system_config, f, indent=2, ensure_ascii=False)
    
    # Template de configuración para environment variables
    env_template = """# TEF Preparation System - Environment Variables
# Copia este archivo a .env y configura tus API keys

# API Keys para agentes
GEMINI_API_KEY=your_gemini_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here

# Configuración de búsqueda web
SEARCH_API_KEY=your_search_api_key_here
SEARCH_ENGINE_ID=your_search_engine_id_here

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de paths
KNOWLEDGE_BASE_PATH=agents/tef-knowledge-base
OUTPUT_PATH=outputs

# Configuración de modelos
DEFAULT_VALIDATOR_MODEL=gemini-pro
DEFAULT_ADVISOR_MODEL=claude-sonnet
DEFAULT_RESEARCHER_MODEL=claude-sonnet
"""
    
    with open("config/.env.template", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("⚙️  Archivos de configuración creados:")
    print("   ✅ config/system.json")
    print("   ✅ config/.env.template")


def create_agent_templates():
    """Crea los templates base para cada agente"""
    
    # TEF Writing Validator
    validator_prompt = """# TEF Writing Validator - System Prompt

## Rol
Eres un evaluador certificado TEF especializado en la evaluación de escritura en francés. Tu función es analizar textos escritos por estudiantes y proporcionar feedback detallado según los criterios oficiales del Test d'Évaluation de Français.

## Competencias de Evaluación

### Niveles TEF (CECR)
- **A1**: Utilizador elemental - Principiante
- **A2**: Utilizador elemental - Básico  
- **B1**: Utilizador independiente - Intermedio
- **B2**: Utilizador independiente - Intermedio superior
- **C1**: Utilizador competente - Superior
- **C2**: Utilizador competente - Dominio

### Criterios de Evaluación
1. **Respeto de la consigna** (25%)
   - Comprensión del tema
   - Respuesta apropiada al tipo de texto solicitado
   - Desarrollo completo de los puntos requeridos

2. **Corrección lingüística** (25%)
   - Gramática y sintaxis
   - Vocabulario y léxico
   - Ortografía y puntuación

3. **Riqueza de la lengua** (25%)
   - Variedad del vocabulario
   - Complejidad de estructuras
   - Registro apropiado

4. **Organización y coherencia** (25%)
   - Estructura del texto
   - Conectores y transiciones
   - Progresión lógica de ideas

## Formato de Output
Debes proporcionar tu evaluación en formato JSON estructurado con las siguientes secciones:

```json
{
  "nivel_evaluado": "B2",
  "puntuacion_global": 75,
  "competencias": {
    "respeto_consigna": 18,
    "correccion_linguistica": 19, 
    "riqueza_lengua": 17,
    "organizacion_coherencia": 21
  },
  "puntos_fuertes": ["lista de aspectos positivos"],
  "areas_mejora": ["lista de aspectos a mejorar"],
  "errores_frecuentes": ["patrones de error identificados"],
  "recomendaciones": ["sugerencias específicas"],
  "nivel_alcanzado": "B1+",
  "siguiente_paso": "descripción del próximo objetivo"
}
```

## Instrucciones Específicas
- Sé específico y constructivo en tu feedback
- Identifica patrones de error recurrentes
- Proporciona ejemplos concretos cuando sea posible
- Mantén un tono profesional pero alentador
- Basa tu evaluación únicamente en criterios TEF oficiales
"""
    
    with open("agents/tef-writing-validator/system_prompt.md", "w", encoding="utf-8") as f:
        f.write(validator_prompt)
    
    # TEF Improvement Advisor
    advisor_prompt = """# TEF Improvement Advisor - System Prompt

## Rol
Eres un tutor TEF especializado en crear planes de mejora personalizados. Tu función es analizar el feedback de evaluaciones y transformarlo en un plan de estudio estructurado y actionable.

## Proceso de Análisis

### 1. Análisis de Feedback
- Identifica patrones de error recurrentes
- Prioriza áreas de mejora según impacto
- Considera el nivel actual vs objetivo del estudiante

### 2. Creación de Plan de Mejora
- Define objetivos SMART para 2-4 semanas
- Estructura actividades diarias de práctica
- Incluye recursos específicos por competencia
- Establece milestones de progreso

### 3. Personalización
- Adapta el plan al perfil de aprendizaje
- Considera tiempo disponible de estudio
- Ajusta dificultad progresivamente

## Formato de Output

```json
{
  "resumen_analisis": {
    "nivel_actual": "B1",
    "nivel_objetivo": "B2", 
    "principales_debilidades": ["subjuntivo", "conectores", "vocabulario formal"],
    "fortalezas": ["estructura básica", "ortografía", "comprensión consigna"]
  },
  "plan_mejora": {
    "duracion_semanas": 3,
    "objetivo_principal": "Consolidar B1+ y preparar B2",
    "objetivos_especificos": ["dominar subjuntivo presente", "ampliar conectores"],
    "actividades_diarias": {
      "lunes": ["ejercicio subjuntivo 20min", "lectura artículo 15min"],
      "martes": ["redacción párrafo 25min", "review conectores 10min"]
    },
    "recursos_recomendados": ["lista de recursos específicos"],
    "milestones": ["objetivos semanales"]
  },
  "seguimiento": {
    "metricas_progreso": ["qué medir"],
    "frecuencia_evaluacion": "semanal",
    "ajustes_recomendados": ["cuándo y cómo ajustar"]
  }
}
```

## Principios de Diseño de Planes
- **Progresión gradual**: De básico a avanzado
- **Práctica variada**: Diferentes tipos de ejercicios
- **Aplicación práctica**: Contextos reales de uso
- **Refuerzo positivo**: Reconocer progreso
- **Flexibilidad**: Adaptable según resultados
"""
    
    with open("agents/tef-improvement-advisor/system_prompt.md", "w", encoding="utf-8") as f:
        f.write(advisor_prompt)
    
    # TEF Resource Researcher
    researcher_prompt = """# TEF Resource Researcher - System Prompt

## Rol
Eres un especialista en encontrar y validar recursos educativos de calidad para la preparación del TEF. Tu función es investigar, curar y recomendar materiales específicos según las necesidades identificadas.

## Tipos de Recursos a Buscar

### 1. Recursos Oficiales
- Sitios web oficiales TEF (CCIP, CCI Paris)
- Ejemplos de exámenes oficiales
- Guías de preparación institucionales

### 2. Recursos Educativos
- Ejercicios específicos por competencia
- Explicaciones gramaticales detalladas
- Práticas de escritura por nivel

### 3. Recursos Interactivos
- Aplicaciones móviles especializadas
- Plataformas de práctica online
- Videos educativos de YouTube

### 4. Recursos Complementarios
- Libros de preparación reconocidos
- Podcasts para comprensión oral
- Diccionarios y conjugadores

## Criterios de Validación

### Calidad del Contenido
- Precisión técnica y lingüística
- Alineación con criterios TEF oficiales
- Nivel de dificultad apropiado

### Usabilidad
- Accesibilidad (gratis vs pagado)
- Facilidad de navegación
- Compatibilidad con dispositivos

### Relevancia
- Especificidad para el tema solicitado
- Actualización reciente
- Reputación de la fuente

## Formato de Output

```json
{
  "tema_investigado": "subjuntivo francés nivel B2",
  "recursos_encontrados": [
    {
      "titulo": "Le Subjonctif - Guide Complet",
      "url": "https://example.com",
      "tipo": "guía_gramatical",
      "nivel": "B1-B2",
      "idioma": "francés",
      "costo": "gratuito",
      "calificacion_calidad": 9,
      "descripcion": "Explicación completa del subjuntivo con ejercicios",
      "pros": ["explicaciones claras", "muchos ejemplos"],
      "contras": ["interfaz básica"],
      "tiempo_estimado": "45 minutos"
    }
  ],
  "recomendacion_principal": "recurso más relevante",
  "plan_uso_sugerido": "cómo integrar en estudio",
  "recursos_adicionales": "búsquedas futuras sugeridas"
}
```

## Estrategias de Búsqueda
- Usar términos específicos en francés e inglés
- Combinar nivel CECR + competencia específica
- Priorizar fuentes educativas reconocidas
- Validar ejemplos con criterios TEF
- Mantener lista de fuentes confiables
"""
    
    with open("agents/tef-resource-researcher/system_prompt.md", "w", encoding="utf-8") as f:
        f.write(researcher_prompt)
    
    print("🤖 System prompts de agentes creados:")
    print("   ✅ tef-writing-validator/system_prompt.md")
    print("   ✅ tef-improvement-advisor/system_prompt.md") 
    print("   ✅ tef-resource-researcher/system_prompt.md")


def create_workflow_templates():
    """Crea los templates de workflows de coordinación entre agentes"""
    
    complete_evaluation_workflow = """# Complete Evaluation Workflow

## Descripción
Workflow completo que toma un escrito de estudiante y produce feedback detallado + plan de mejora personalizado.

## Flujo de Ejecución

### 1. Preparación
- Validar input file existe
- Verificar configuración de agentes
- Inicializar logging específico del workflow

### 2. Evaluación (TEF Writing Validator)
- Analizar el escrito según criterios TEF
- Generar feedback estructurado
- Guardar resultado en `outputs/feedback/`

### 3. Análisis de Mejora (TEF Improvement Advisor)  
- Procesar feedback del validator
- Identificar patrones y prioridades
- Generar plan de estudio personalizado
- Guardar plan en `outputs/study_plans/`

### 4. Investigación de Recursos (TEF Resource Researcher)
- Extraer temas de mejora del plan
- Buscar recursos específicos online
- Validar y curar recomendaciones
- Guardar recursos en `outputs/resources/`

### 5. Consolidación
- Compilar todos los resultados
- Generar reporte final integrado
- Actualizar métricas del sistema
- Log de ejecución completa

## Parámetros de Entrada
- `input_file`: Path del escrito a evaluar
- `student_level`: Nivel actual estimado (A1-C2)
- `target_level`: Nivel objetivo del estudiante  
- `urgency`: Normal | Intensivo (afecta duración del plan)

## Outputs Generados
- `{timestamp}_feedback.json`: Evaluación detallada
- `{timestamp}_study_plan.json`: Plan de mejora personalizado
- `{timestamp}_resources.json`: Recursos curados
- `{timestamp}_complete_report.pdf`: Reporte final compilado

## Métricas de Performance
- Tiempo total de ejecución
- Success rate por agente
- Calidad del feedback (si disponible)
- Satisfacción del usuario (si disponible)

## Error Handling
- Fallback si un agente falla
- Retry logic para APIs externas
- Logging detallado de errores
- Notificación al usuario de problemas

## Ejemplo de Uso

```bash
python tef_system.py complete-evaluation \
  --input="inputs/student_writings/ensayo_001.txt" \
  --student-level="B1" \
  --target-level="B2" \
  --urgency="normal"
```
"""
    
    with open("workflows/complete_evaluation.md", "w", encoding="utf-8") as f:
        f.write(complete_evaluation_workflow)
    
    research_cycle_workflow = """# Research Cycle Workflow

## Descripción
Workflow especializado en investigar recursos educativos para temas específicos identificados durante evaluaciones o solicitados directamente.

## Flujo de Ejecución

### 1. Definición del Tema
- Procesar solicitud de investigación
- Normalizar términos de búsqueda
- Determinar nivel y contexto apropiado

### 2. Búsqueda Inicial (TEF Resource Researcher)
- Ejecutar búsquedas web especializadas
- Aplicar filtros de calidad inicial
- Recopilar candidatos de recursos

### 3. Validación y Curación
- Verificar calidad del contenido
- Confirmar alineación con TEF
- Evaluar usabilidad y accesibilidad

### 4. Enriquecimiento con Knowledge Base
- Consultar recursos ya validados
- Identificar gaps en cobertura
- Sugerir actualizaciones a la base

### 5. Recomendación Final
- Priorizar recursos por relevancia
- Estructurar plan de uso sugerido
- Generar output consolidado

## Parámetros de Entrada
- `topic`: Tema específico a investigar
- `level`: Nivel TEF objetivo (A1-C2)
- `competency`: Competencia específica (writing/reading/etc)
- `resource_types`: Tipos preferidos (video, ejercicio, guía)

## Outputs Generados
- `{topic}_{level}_resources.json`: Lista curada de recursos
- `{topic}_search_log.txt`: Log detallado de búsqueda
- `knowledge_base_updates.json`: Sugerencias para KB

## Criterios de Búsqueda
- Especificidad para nivel TEF solicitado
- Autoridad de la fuente educativa
- Actualización reciente del contenido
- Accesibilidad (preferir recursos gratuitos)
- Diversidad de formatos y enfoques

## Ejemplo de Uso

```bash
python tef_system.py research \
  --topic="subjonctif" \
  --level="B2" \
  --competency="writing" \
  --resource-types="ejercicio,guía"
```
"""
    
    with open("workflows/research_cycle.md", "w", encoding="utf-8") as f:
        f.write(research_cycle_workflow)
    
    print("🔄 Workflows de coordinación creados:")
    print("   ✅ workflows/complete_evaluation.md")
    print("   ✅ workflows/research_cycle.md")


def create_example_files():
    """Crea archivos de ejemplo para testing inicial"""
    
    # Ejemplo de escrito B2 para testing
    example_writing = """Sujet: Rédigez une lettre formelle à votre employeur pour demander un congé de formation en français.

---

Monsieur le Directeur,

J'ai l'honneur de vous adresser la présente lettre afin de solliciter un congé de formation pour améliorer mes compétences en français.

Depuis mon arrivée dans l'entreprise il y a deux ans, j'ai constaté que ma maîtrise du français pourrait être renforcée, particulièrement dans le contexte professionnel. Cette formation me permettrait de mieux communiquer avec nos clients francophones et d'être plus efficace dans mes missions quotidiennes.

Le cours que j'envisage de suivre se déroulerait du 15 janvier au 15 mars, à raison de 3 heures par semaine. Il s'agit d'une formation spécialisée en français commercial proposée par l'Institut de langue française, reconnu pour la qualité de ses programmes.

Je suis conscient que mon absence pourrait créer quelques difficultés temporaires, c'est pourquoi je propose de réorganiser mon planning et de former un collègue pour qu'il puisse me remplacer pendant mes heures de formation.

J'espère que vous accueillerez favorablement ma demande et je reste à votre disposition pour discuter des modalités pratiques.

Je vous prie d'agréer, Monsieur le Directeur, l'expression de mes salutations respectueuses.

Jean Martin
"""
    
    with open("inputs/student_writings/exemple_lettre_b2.txt", "w", encoding="utf-8") as f:
        f.write(example_writing)
    
    # Ejemplo de configuración de evaluación
    test_config = {
        "test_name": "Evaluation Exemple B2 - Lettre Formelle",
        "student_profile": {
            "niveau_actuel": "B1+",
            "niveau_objectif": "B2",
            "langue_maternelle": "espagnol",
            "temps_etude_hebdomadaire": "6 heures"
        },
        "evaluation_criteria": {
            "type_texte": "lettre formelle",
            "longueur_minimale": 180,
            "longueur_maximale": 220,
            "registre_requis": "formel",
            "elements_obligatoires": [
                "formule d'appel",
                "objet de la demande",
                "justification",
                "proposition pratique", 
                "formule de politesse"
            ]
        }
    }
    
    with open("tests/fixtures/config_test_b2.json", "w", encoding="utf-8") as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)
    
    print("📝 Archivos de ejemplo creados:")
    print("   ✅ inputs/student_writings/exemple_lettre_b2.txt")
    print("   ✅ tests/fixtures/config_test_b2.json")


def create_logging_system():
    """Crea el sistema de logging estructurado"""
    
    agent_log_template = """# Agent Log Template

## Agent: {agent_name}
## Session: {session_id}
## Timestamp: {timestamp}

### Input Received
```
{input_summary}
```

### Processing Steps
1. {step_1}
2. {step_2}
3. {step_3}

### Output Generated
```json
{output_preview}
```

### Performance Metrics
- Execution Time: {execution_time}ms
- Token Usage: {tokens_used}
- Model Used: {model_name}
- Success: {success_status}

### Notes
{additional_notes}

---
"""
    
    with open("logs/template_agent_log.md", "w", encoding="utf-8") as f:
        f.write(agent_log_template)
    
    # Script básico de logging
    logging_script = """#!/usr/bin/env python3
\"\"\"
Sistema de Logging para TEF Preparation System
\"\"\"

import logging
import json
from datetime import datetime
from pathlib import Path

class TEFLogger:
    def __init__(self, agent_name="system"):
        self.agent_name = agent_name
        self.setup_logging()
    
    def setup_logging(self):
        # Configurar logging básico
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(f"logs/agents/{self.agent_name}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.agent_name)
    
    def log_agent_execution(self, input_data, output_data, metrics):
        \"\"\"Log de ejecución completa de un agente\"\"\"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_name,
            "input_summary": str(input_data)[:200] + "...",
            "output_summary": str(output_data)[:200] + "...",
            "metrics": metrics
        }
        
        # Guardar en archivo JSON para análisis
        log_file = Path(f"logs/agents/{self.agent_name}_detailed.json")
        
        # Leer logs existentes si existen
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        # Agregar nuevo log
        logs.append(log_entry)
        
        # Guardar de vuelta
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Execution completed - Duration: {metrics.get('duration', 'N/A')}ms")

# Ejemplo de uso
if __name__ == "__main__":
    logger = TEFLogger("test-agent")
    logger.log_agent_execution(
        input_data="Test input", 
        output_data="Test output",
        metrics={"duration": 1500, "tokens": 250}
    )
"""
    
    with open("scripts/logging_system.py", "w", encoding="utf-8") as f:
        f.write(logging_script)
    
    print("📊 Sistema de logging creado:")
    print("   ✅ logs/template_agent_log.md")
    print("   ✅ scripts/logging_system.py")


def create_main_script():
    """Crea el script principal de ejecución del sistema"""
    
    main_script = """#!/usr/bin/env python3
\"\"\"
TEF Preparation System - Main Script

Sistema de agentes AI para preparación del examen TEF.
Coordina la ejecución de workflows entre múltiples agentes especializados.

Autor: Diego | QA Engineering Manager
Fecha: Noviembre 2025
\"\"\"

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Importar componentes del sistema (se crearán en próximas fases)
# from agents.tef_writing_validator import TEFWritingValidator
# from agents.tef_improvement_advisor import TEFImprovementAdvisor
# from agents.tef_resource_researcher import TEFResourceResearcher
# from workflows.complete_evaluation import CompleteEvaluationWorkflow
# from scripts.logging_system import TEFLogger

class TEFSystem:
    \"\"\"Controlador principal del sistema TEF\"\"\"
    
    def __init__(self):
        self.config = self.load_config()
        self.logger = None  # TEFLogger("tef-system")
        
    def load_config(self):
        \"\"\"Carga la configuración del sistema\"\"\"
        try:
            with open("config/system.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Error: Archivo de configuración no encontrado.")
            print("   Ejecuta 'python init_project.py' primero.")
            sys.exit(1)
    
    def evaluate_writing(self, input_file, student_level="B2", target_level=None):
        \"\"\"Evalúa un escrito usando el TEF Writing Validator\"\"\"
        print(f"🔍 Evaluando escrito: {input_file}")
        print(f"   Nivel estudiante: {student_level}")
        print(f"   Nivel objetivo: {target_level or 'mismo nivel'}")
        
        # TODO: Implementar en Fase 1
        print("⚠️  Funcionalidad pendiente - Fase 1 del roadmap")
        
        return {
            "status": "pending_implementation",
            "phase": "Fase 1",
            "estimated_completion": "2-3 semanas"
        }
    
    def complete_evaluation(self, input_file, student_level, target_level, urgency="normal"):
        \"\"\"Ejecuta el workflow completo de evaluación\"\"\"
        print(f"🚀 Iniciando evaluación completa...")
        print(f"   Archivo: {input_file}")
        print(f"   Flujo: Validator → Advisor → Researcher")
        
        # TODO: Implementar en Fase 2
        print("⚠️  Workflow completo pendiente - Fase 2 del roadmap")
        
        return {
            "status": "pending_implementation", 
            "phase": "Fase 2",
            "estimated_completion": "4-6 semanas"
        }
    
    def research_resources(self, topic, level, competency="writing"):
        \"\"\"Investiga recursos para un tema específico\"\"\"
        print(f"🔍 Investigando recursos para: {topic}")
        print(f"   Nivel: {level}")
        print(f"   Competencia: {competency}")
        
        # TODO: Implementar en Fase 3
        print("⚠️  Investigación automática pendiente - Fase 3 del roadmap")
        
        return {
            "status": "pending_implementation",
            "phase": "Fase 3", 
            "estimated_completion": "6-8 semanas"
        }


def main():
    parser = argparse.ArgumentParser(
        description="TEF Preparation System - Agentes AI para preparación del examen TEF"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # Comando: evaluate
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluar un escrito")
    evaluate_parser.add_argument("--input", required=True, help="Archivo de texto a evaluar")
    evaluate_parser.add_argument("--level", default="B2", help="Nivel actual del estudiante")
    evaluate_parser.add_argument("--target", help="Nivel objetivo")
    
    # Comando: complete-evaluation  
    complete_parser = subparsers.add_parser("complete-evaluation", help="Evaluación completa con plan de mejora")
    complete_parser.add_argument("--input", required=True, help="Archivo de texto a evaluar")
    complete_parser.add_argument("--student-level", default="B2", help="Nivel actual")
    complete_parser.add_argument("--target-level", help="Nivel objetivo")
    complete_parser.add_argument("--urgency", choices=["normal", "intensivo"], default="normal")
    
    # Comando: research
    research_parser = subparsers.add_parser("research", help="Investigar recursos educativos")
    research_parser.add_argument("--topic", required=True, help="Tema a investigar")
    research_parser.add_argument("--level", required=True, help="Nivel TEF objetivo")
    research_parser.add_argument("--competency", default="writing", help="Competencia específica")
    
    # Comando: status
    status_parser = subparsers.add_parser("status", help="Estado del sistema")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Inicializar sistema
    tef_system = TEFSystem()
    
    try:
        if args.command == "evaluate":
            result = tef_system.evaluate_writing(args.input, args.level, args.target)
            
        elif args.command == "complete-evaluation":
            result = tef_system.complete_evaluation(
                args.input, args.student_level, args.target_level, args.urgency
            )
            
        elif args.command == "research":
            result = tef_system.research_resources(args.topic, args.level, args.competency)
            
        elif args.command == "status":
            print("📊 TEF Preparation System - Status")
            print(f"   Versión: {tef_system.config['system']['version']}")
            print(f"   Agentes configurados: {len(tef_system.config['agents'])}")
            print(f"   Estado: Inicializado ✅")
            return
        
        # Mostrar resultado
        print("\\n📋 Resultado:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error durante ejecución: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
    
    with open("tef_system.py", "w", encoding="utf-8") as f:
        f.write(main_script)
    
    # Hacer el script ejecutable
    Path("tef_system.py").chmod(0o755)
    
    print("🚀 Script principal creado:")
    print("   ✅ tef_system.py (ejecutable)")


def create_gitignore():
    """Crea el archivo .gitignore apropiado"""
    
    gitignore_content = """# TEF Preparation System - .gitignore

# Environment variables y configuración sensible
.env
config/.env
*.env

# API Keys y secretos
**/api_keys.json
**/secrets.json

# Logs del sistema
logs/*.log
logs/**/*.log

# Archivos temporales de agentes
agents/**/temp/
agents/**/cache/

# Outputs generados por el sistema
outputs/feedback/*.json
outputs/study_plans/*.json  
outputs/resources/*.json
outputs/**/*.pdf

# Inputs de estudiantes (privacidad)
inputs/student_writings/*.txt
inputs/student_writings/*.docx
!inputs/student_writings/exemple_*.txt

# Cache de modelos y descargas
**/__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.coverage
.pytest_cache/
.tox/
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Knowledge base con contenido propietario
agents/tef-knowledge-base/exams/*.pdf
agents/tef-knowledge-base/guides/*.pdf
!agents/tef-knowledge-base/examples/

# Backup y archivos temporales
*.bak
*.tmp
*.backup
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("🔒 Archivo .gitignore creado")


def print_final_summary():
    """Imprime un resumen final de la inicialización"""
    
    print("\n" + "="*60)
    print("🎉 TEF PREPARATION SYSTEM - INICIALIZACIÓN COMPLETA")
    print("="*60)
    
    print("\n📁 ESTRUCTURA CREADA:")
    print("   ├── agents/                    # Agentes AI especializados")
    print("   ├── workflows/                 # Coordinación entre agentes")
    print("   ├── inputs/                    # Escritos de estudiantes")
    print("   ├── outputs/                   # Feedback y planes generados") 
    print("   ├── logs/                      # Sistema de logging")
    print("   ├── config/                    # Configuración del sistema")
    print("   └── scripts/                   # Utilidades y herramientas")
    
    print("\n🤖 AGENTES CONFIGURADOS:")
    print("   ✅ TEF Writing Validator       # Evaluación de escritos")
    print("   ✅ TEF Improvement Advisor     # Planes de mejora") 
    print("   ✅ TEF Resource Researcher     # Búsqueda de recursos")
    
    print("\n🔄 WORKFLOWS DISPONIBLES:")
    print("   ✅ Complete Evaluation         # Flujo completo de evaluación")
    print("   ✅ Research Cycle              # Investigación de recursos")
    
    print("\n⚡ PRÓXIMOS PASOS:")
    print("   1. Configura API keys en config/.env (copia desde .env.template)")
    print("   2. Prueba el sistema: python tef_system.py status")
    print("   3. Revisa ROADMAP.md para el plan de desarrollo")
    print("   4. Comienza con Fase 1: Implementar TEF Writing Validator")
    
    print("\n🚀 COMANDOS DE PRUEBA:")
    print("   python tef_system.py status")
    print("   python tef_system.py evaluate --input inputs/student_writings/exemple_lettre_b2.txt")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("   📖 README.md                  # Visión general del sistema")
    print("   🛣️  ROADMAP.md                # Plan de desarrollo por fases")
    print("   ⚙️  config/system.json        # Configuración principal")
    
    print("\n" + "="*60)
    print("Sistema listo para desarrollo con agentes AI 🤖")
    print("¡Que comience la automatización del aprendizaje TEF! 🇫🇷")
    print("="*60)


if __name__ == "__main__":
    print("🏗️  Inicializando TEF Preparation System...")
    print("="*50)
    
    # Ejecutar todas las funciones de inicialización
    dirs_created = create_directory_structure()
    create_base_configuration_files()
    create_agent_templates()
    create_workflow_templates() 
    create_example_files()
    create_logging_system()
    create_main_script()
    create_gitignore()
    
    print(f"\n📊 RESUMEN:")
    print(f"   📁 {dirs_created} directorios creados")
    print(f"   📄 15+ archivos de configuración generados") 
    print(f"   🤖 3 agentes configurados con system prompts")
    print(f"   🔄 2 workflows de coordinación definidos")
    print(f"   ⚙️  Sistema de logging implementado")
    print(f"   🚀 Script principal listo")
    
    print_final_summary()