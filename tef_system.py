#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEF Preparation System - Main Script

Sistema de agentes AI para preparación del examen TEF.
Coordina la ejecución de workflows entre múltiples agentes especializados.

Autor: Diego | QA Engineering Manager
Fecha: Noviembre 2025
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import re

# Cargar variables de entorno desde config/.env
load_dotenv(dotenv_path=Path('config/.env'))

# Integración del nuevo agente
from agents.tef_writing_validator import TEFWritingValidator
from agents.tef_resource_researcher import TEFResourceResearcher
from agents.tef_improvement_advisor import TEFImprovementAdvisor


class TEFSystem:
    """Controlador principal del sistema TEF"""
    
    def __init__(self):
        self.config = self.load_config()
        self.setup_paths()
        
    def setup_paths(self):
        """Configura las rutas del sistema"""
        self.base_path = Path(".")
        self.agents_path = self.base_path / "agents"
        self.inputs_path = self.base_path / "inputs"
        self.outputs_path = self.base_path / "outputs"
        self.logs_path = self.base_path / "logs"
        
    def load_config(self):
        """Carga la configuración del sistema"""
        config_file = Path("config/system.json")
        
        if not config_file.exists():
            print("❌ Error: Archivo de configuración no encontrado.")
            print("   Ejecuta 'python init_project.py' primero para inicializar el proyecto.")
            sys.exit(1)
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error cargando configuración: {str(e)}")
            sys.exit(1)
    
    def check_system_status(self):
        """Verifica el estado del sistema"""
        status = {
            "system_initialized": False,
            "agents_configured": 0,
            "config_loaded": False,
            "directories_present": 0,
            "ready_for_development": False
        }
        
        # Verificar configuración
        if self.config:
            status["config_loaded"] = True
            status["agents_configured"] = len(self.config.get("agents", {}))
        
        # Verificar directorios
        required_dirs = ["agents", "workflows", "inputs", "outputs", "logs", "config"]
        dirs_present = sum(1 for d in required_dirs if Path(d).exists())
        status["directories_present"] = dirs_present
        
        # Verificar agentes
        agent_dirs = ["tef-writing-validator", "tef-improvement-advisor", "tef-resource-researcher"]
        agents_present = sum(1 for a in agent_dirs if (Path("agents") / a).exists())
        
        # Estado general
        status["system_initialized"] = dirs_present >= 5 and agents_present >= 3
        status["ready_for_development"] = status["system_initialized"] and status["config_loaded"]
        
        return status
    
    def validate_input_file(self, filepath):
        """Valida que el archivo de input existe y es legible"""
        file_path = Path(filepath)
        
        if not file_path.exists():
            print(f"❌ Error: Archivo no encontrado: {filepath}")
            return False
        
        if not file_path.is_file():
            print(f"❌ Error: La ruta no es un archivo: {filepath}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print(f"❌ Error: El archivo está vacío: {filepath}")
                    return False
        except Exception as e:
            print(f"❌ Error leyendo archivo: {str(e)}")
            return False
        
        return True
    
    def evaluate_writing(self, input_file, student_level="B2", target_level=None):
        """Evalúa un escrito usando el TEF Writing Validator"""
        print(f"🔍 Iniciando evaluación de escrito...")
        print(f"   📄 Archivo: {input_file}")
        print(f"   📊 Nivel estudiante: {student_level}")
        print(f"   🎯 Nivel objetivo: {target_level or 'No especificado'}")

        # 1. Validar input
        if not self.validate_input_file(input_file):
            return {"status": "error", "message": "Archivo de input inválido"}

        try:
            # 2. Cargar configuración del agente
            agent_config = self.config["agents"]["tef-writing-validator"]
            if not agent_config.get("enabled", False):
                msg = "El agente TEF Writing Validator está deshabilitado en la configuración."
                print(f"⚠️  {msg}")
                return {"status": "disabled", "message": msg}

            # 3. Leer contenido del archivo
            with open(input_file, 'r', encoding='utf-8') as f:
                student_text = f.read()

            # 4. Instanciar y ejecutar el agente
            print("   🤖 Ejecutando TEF Writing Validator...")
            validator = TEFWritingValidator(config=agent_config)
            evaluation_result = validator.evaluate(
                student_text=student_text,
                student_level=student_level,
                target_level=target_level
            )

            if evaluation_result.get("error"):
                print(f"   ❌ Error durante la evaluación: {evaluation_result.get('message')}")
                return evaluation_result

            # 5. Guardar el resultado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{timestamp}_feedback_{Path(input_file).stem}.json"
            output_file = self.outputs_path / "feedback" / output_filename
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(evaluation_result, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Evaluación completada.")
            print(f"   💾 Resultado guardado en: {output_file}")

            return evaluation_result

        except KeyError:
            msg = "Configuración para 'tef-writing-validator' no encontrada en system.json."
            print(f"❌ Error: {msg}")
            return {"status": "error", "message": msg}
        except Exception as e:
            print(f"❌ Error inesperado en el flujo de evaluación: {str(e)}")
            return {"status": "error", "message": f"Error inesperado: {str(e)}"}
    
    def complete_evaluation(self, input_file, student_level, target_level, urgency="normal"):
        """Ejecuta el workflow completo de evaluación"""
        print(f"🚀 Iniciando evaluación completa (workflow multi-agente)...")
        print(f"   📄 Archivo: {input_file}")
        print(f"   📊 Nivel actual: {student_level}")
        print(f"   🎯 Nivel objetivo: {target_level}")
        print(f"   ⚡ Urgencia: {urgency}")
        print(f"   🔄 Flujo: Validator → Advisor → Researcher")
        
        # Validar input
        if not self.validate_input_file(input_file):
            return {"status": "error", "message": "Archivo de input inválido"}
        
        # Simular workflow (implementación real en Fase 2)
        print("\n⚠️  Workflow completo simulado - Implementación en Fase 2")
        print("   🤖 Agentes involucrados:")
        print("      1️⃣  TEF Writing Validator (evaluación)")
        print("      2️⃣  TEF Improvement Advisor (plan de mejora)")
        print("      3️⃣  TEF Resource Researcher (recursos curados)")
        print("   ⏱️  Tiempo estimado de desarrollo: 4-6 semanas")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = {
            "status": "pending_implementation",
            "phase": "Fase 2 - Inteligencia de Mejora",
            "workflow": "complete_evaluation", 
            "agents_involved": ["tef-writing-validator", "tef-improvement-advisor", "tef-resource-researcher"],
            "input_file": str(input_file),
            "parameters": {
                "student_level": student_level,
                "target_level": target_level, 
                "urgency": urgency
            },
            "timestamp": timestamp,
            "estimated_completion": "4-6 semanas",
            "expected_outputs": [
                "Evaluación detallada con puntuación",
                "Plan de estudio personalizado 2-4 semanas",
                "Lista curada de recursos educativos",
                "Reporte consolidado PDF"
            ]
        }
        
        return result
    
    def research_resources(self, topic, level, competency="writing"):
        """Investiga recursos para un tema específico usando el TEF Resource Researcher"""
        print(f"🔍 Iniciando investigación de recursos...")
        print(f"   🎯 Tema: {topic}")
        print(f"   📊 Nivel: {level}")
        print(f"   📝 Competencia: {competency}")

        try:
            # 1. Cargar configuración del agente
            agent_config = self.config["agents"]["tef-resource-researcher"]
            if not agent_config.get("enabled", False):
                msg = "El agente TEF Resource Researcher está deshabilitado en la configuración."
                print(f"⚠️  {msg}")
                return {"status": "disabled", "message": msg}

            # 2. Instanciar y ejecutar el agente
            print("   🤖 Ejecutando TEF Resource Researcher...")
            researcher = TEFResourceResearcher(config=agent_config)
            research_result = researcher.research(
                topic=topic,
                level=level,
                competency=competency
            )

            if research_result.get("status") == "error":
                print(f"   ❌ Error durante la investigación: {research_result.get('message')}")
                return research_result
            
            print(f"   ✅ Investigación completada. Se encontraron {len(research_result.get('results', []))} resultados.")
            return research_result

        except KeyError:
            msg = "Configuración para 'tef-resource-researcher' no encontrada en system.json."
            print(f"❌ Error: {msg}")
            return {"status": "error", "message": msg}
        except Exception as e:
            print(f"❌ Error inesperado en el flujo de investigación: {str(e)}")
            return {"status": "error", "message": f"Error inesperado: {str(e)}"}

    def improve_plan(self, feedback_file, mode="normal"):
        """Genera un plan de mejora a partir de un archivo de feedback y le añade recursos."""
        print(f"🚀 Iniciando generación de plan de mejora (Modo: {mode})...")
        print(f"   📄 Archivo de feedback: {feedback_file}")

        if not self.validate_input_file(feedback_file):
            return {"status": "error", "message": "Archivo de feedback inválido"}

        try:
            agent_config = self.config["agents"]["tef-improvement-advisor"]
            if not agent_config.get("enabled", False):
                return {"status": "disabled", "message": "El agente TEF Improvement Advisor está deshabilitado."}

            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)

            print("   🤖 Ejecutando TEF Improvement Advisor...")
            advisor = TEFImprovementAdvisor(config=agent_config)
            result = advisor.generate_plan(feedback_data, mode)

            if result.get("status") == "error":
                print(f"   ❌ Error al generar el plan: {result.get('message')}")
                return result

            plan_content = result.get("plan", "")
            
            print("   🤖 Extrayendo temas de investigación del plan...")
            research_topics = self._parse_research_topics(plan_content)

            if research_topics:
                plan_content = re.sub(r"```yaml.*?```", "", plan_content, flags=re.DOTALL).strip()
                
                print("   🔍 Buscando recursos recomendados (esto puede tardar unos segundos)...")
                collected_resources = []
                for topic_data in research_topics:
                    print(f"      - Buscando sobre: '{topic_data['topic']}'...")
                    research_result = self.research_resources(
                        topic=topic_data['topic'],
                        level=topic_data['level'],
                        competency=topic_data['competency']
                    )
                    collected_resources.append({
                        "topic_info": topic_data,
                        "results": research_result.get("results", [])
                    })
                
                resources_markdown = self._format_resources_for_markdown(collected_resources)
                plan_content += resources_markdown

            base_name = Path(feedback_file).stem.replace("feedback_", "")
            output_filename = f"{base_name}_study_plan.md"
            output_file = self.outputs_path / "study_plans" / output_filename
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(plan_content)

            print(f"   ✅ Plan de estudio enriquecido con recursos.")
            print(f"   💾 Guardado en: {output_file}")
            
            return {"status": "success", "plan_file": str(output_file)}

        except KeyError:
            msg = "Configuración para 'tef-improvement-advisor' o 'tef-resource-researcher' no encontrada."
            return {"status": "error", "message": msg}
        except json.JSONDecodeError:
            return {"status": "error", "message": f"Error: El archivo de feedback '{feedback_file}' no es un JSON válido."}
        except Exception as e:
            return {"status": "error", "message": f"Error inesperado en el flujo de mejora: {e}"}

    def _parse_research_topics(self, plan_content: str) -> list:
        """Extrae y parsea el bloque YAML de temas para investigar."""
        topics = []
        match = re.search(r"```yaml\s*\n---\s*\n###\s*TEMAS_PARA_INVESTIGAR\s*\n(.*?)\s*```", plan_content, re.DOTALL)
        
        if not match:
            return []

        yaml_content = match.group(1).strip()
        
        current_topic = {}
        for line in yaml_content.split('\n'):
            line = line.strip()
            if line.startswith('- topic:'):
                if current_topic:
                    topics.append(current_topic)
                current_topic = {'topic': line.split(':', 1)[1].strip().strip('"')}
            elif line.startswith('level:'):
                current_topic['level'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('competency:'):
                current_topic['competency'] = line.split(':', 1)[1].strip().strip('"')
                
        if current_topic:
            topics.append(current_topic)
            
        return topics

    def _format_resources_for_markdown(self, collected_resources: list) -> str:
        """Formatea la lista de recursos encontrados en una sección Markdown."""
        if not collected_resources:
            return ""

        markdown_section = "\n\n---\n\n## 📚 Recursos Recomendados\n"
        
        for resource_group in collected_resources:
            info = resource_group['topic_info']
            results = resource_group['results']
            
            markdown_section += f"\n### {info['competency'].capitalize()}: {info['topic'].capitalize()} (Nivel {info['level']})\n"
            
            if results:
                for res in results[:3]:
                    markdown_section += f"- [{res['title']}]({res['link']})\n"
            else:
                markdown_section += "- No se encontraron recursos específicos para este tema.\n"
                
        return markdown_section
        
    def display_status(self):
        """Muestra el estado completo del sistema"""
        print("📊 TEF PREPARATION SYSTEM - STATUS REPORT")
        print("=" * 50)
        
        # Información del sistema
        system_info = self.config.get("system", {})
        print(f"📋 Sistema: {system_info.get('name', 'TEF Preparation System')}")
        print(f"🔢 Versión: {system_info.get('version', '1.0.0')}")
        print(f"👨‍💻 Autor: {system_info.get('author', 'Diego')}")
        print(f"📅 Creado: {system_info.get('created', 'N/A')}")
        
        # Estado del sistema
        status = self.check_system_status()
        print(f"\n🎯 Estado General:")
        print(f"   ✅ Sistema inicializado: {'Sí' if status['system_initialized'] else 'No'}")
        print(f"   ⚙️  Configuración cargada: {'Sí' if status['config_loaded'] else 'No'}")
        print(f"   📁 Directorios presentes: {status['directories_present']}/6")
        print(f"   🤖 Agentes configurados: {status['agents_configured']}")
        print(f"   🚀 Listo para desarrollo: {'Sí' if status['ready_for_development'] else 'No'}")
        
        # Estado de agentes
        print(f"\n🤖 Estado de Agentes:")
        agents_config = self.config.get("agents", {})
        for agent_name, agent_config in agents_config.items():
            enabled = "✅" if agent_config.get("enabled", False) else "❌"
            model = agent_config.get("model", "N/A")
            print(f"   {enabled} {agent_name}: {model}")
        
        # Próximos pasos
        print(f"\n📋 Próximos Pasos de Desarrollo:")
        if not status["system_initialized"]:
            print("   1️⃣  Ejecutar: python init_project.py")
            print("   2️⃣  Configurar API keys en config/.env")
        else:
            print("   1️⃣  Configurar API keys en config/.env")
            print("   2️⃣  Implementar TEF Writing Validator (Fase 1)")
            print("   3️⃣  Poblar knowledge base con ejemplos TEF")
            print("   4️⃣  Testing con escritos reales")
        
        # Roadmap resumido
        print(f"\n🛣️  Roadmap de Desarrollo:")
        print("   📌 FASE 1 (2-3 sem): Fundación - TEF Writing Validator")
        print("   📌 FASE 2 (2-3 sem): Inteligencia - Improvement Advisor") 
        print("   📌 FASE 3 (2 sem):   Investigación - Resource Researcher")
        print("   📌 FASE 4 (2-3 sem): Optimización y Escalabilidad")
        print("   📌 FASE 5 (4-6 sem): Expansión Multi-competencia")
        
        print("\n" + "=" * 50)


def main():
    """Función principal con CLI"""
    parser = argparse.ArgumentParser(
        description="TEF Preparation System - Agentes AI para preparación del examen TEF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python tef_system.py status
  python tef_system.py evaluate --input inputs/student_writings/example.txt --level B2
  python tef_system.py improve --feedback outputs/feedback/20251202_feedback.json
  python tef_system.py complete-evaluation --input example.txt --student-level B1 --target-level B2
  python tef_system.py research --topic "subjonctif" --level B2
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # Comando: status
    status_parser = subparsers.add_parser("status", help="Mostrar estado del sistema")
    
    # Comando: evaluate
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluar un escrito")
    evaluate_parser.add_argument("--input", required=True, 
                                help="Archivo de texto a evaluar")
    evaluate_parser.add_argument("--level", default=None, 
                                help="Nivel objetivo para la evaluación (ej. B2). Si se omite, se activará la detección automática de nivel.")
    evaluate_parser.add_argument("--target", 
                                help="Nivel objetivo del estudiante")
    
    # Comando: complete-evaluation
    complete_parser = subparsers.add_parser("complete-evaluation", 
                                          help="Evaluación completa con plan de mejora")
    complete_parser.add_argument("--input", required=True,
                                help="Archivo de texto a evaluar")
    complete_parser.add_argument("--student-level", default="B2",
                                help="Nivel actual del estudiante")
    complete_parser.add_argument("--target-level", required=True,
                                help="Nivel objetivo del estudiante")
    complete_parser.add_argument("--urgency", choices=["normal", "intensivo"], default="normal",
                                help="Urgencia del plan de estudio")
    
    # Comando: research
    research_parser = subparsers.add_parser("research", help="Investigar recursos educativos")
    research_parser.add_argument("--topic", required=True,
                                help="Tema específico a investigar")
    research_parser.add_argument("--level", required=True,
                                help="Nivel TEF objetivo (A1-C2)")
    research_parser.add_argument("--competency", default="writing",
                                help="Competencia específica (writing, reading, listening, speaking)")

    # Comando: improve
    improve_parser = subparsers.add_parser("improve", help="Generar plan de mejora desde feedback")
    improve_parser.add_argument("--feedback", required=True,
                                help="Ruta al archivo JSON de feedback")
    improve_parser.add_argument("--mode", default="normal", choices=["normal", "intensive"],
                                help="Modo del plan de estudio: normal (default) o intensive.")
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Si no hay comando, mostrar ayuda
    if not args.command:
        parser.print_help()
        return
    
    # Inicializar sistema
    try:
        tef_system = TEFSystem()
    except SystemExit:
        return  # Error ya manejado en TEFSystem.__init__
    except Exception as e:
        print(f"❌ Error inicializando sistema: {str(e)}")
        return
    
    # Ejecutar comando
    try:
        if args.command == "status":
            tef_system.display_status()
            
        elif args.command == "evaluate":
            result = tef_system.evaluate_writing(args.input, args.level, args.target)
            print("\n📋 Resultado de Evaluación:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.command == "complete-evaluation":
            result = tef_system.complete_evaluation(
                args.input, args.student_level, args.target_level, args.urgency
            )
            print("\n📋 Resultado de Evaluación Completa:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.command == "research":
            result = tef_system.research_resources(args.topic, args.level, args.competency)
            print("\n📋 Resultado de Investigación:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "improve":
            result = tef_system.improve_plan(args.feedback, args.mode)
            print("\n📋 Resultado del Plan de Mejora:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error ejecutando comando '{args.command}': {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()