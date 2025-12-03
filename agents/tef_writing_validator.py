#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEF Writing Validator Agent

Este agente evalúa un texto en francés según los criterios del TEF,
utilizando la API de Google Gemini para el análisis.

Autor: Diego | QA Engineering Manager
Fecha: Noviembre 2025
"""

import json
import logging
import os
from pathlib import Path
import datetime
from dotenv import load_dotenv
import google.generativeai as genai

class TEFWritingValidator:
    """
    Agente para evaluar escritos en francés para el TEF.
    """
    def __init__(self, config: dict, logger: logging.Logger = None):
        """
        Inicializa el validador.

        Args:
            config (dict): Configuración del agente desde system.json.
            logger (logging.Logger, optional): Logger para el agente.
        """
        self.config = config
        self.agent_name = "tef-writing-validator"
        
        if logger:
            self.logger = logger
        else:
            self._setup_logging()

        self.system_prompt = self._load_system_prompt()
        self._setup_gemini()
        
        self.logger.info("TEF Writing Validator inicializado correctamente.")

    def _setup_logging(self):
        """Configura el sistema de logging para este agente."""
        self.logger = logging.getLogger(self.agent_name)
        self.logger.setLevel(logging.INFO)
        
        log_dir = Path("logs/agents")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(log_dir / f"{self.agent_name}.log", mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def _setup_gemini(self):
        """Configura el cliente de la API de Gemini."""
        try:
            load_dotenv(dotenv_path=Path("config/.env"))
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or api_key == "your_gemini_api_key_here":
                self.logger.error("La API Key de Gemini no está configurada en config/.env")
                raise ValueError("API Key de Gemini no encontrada.")
            
            genai.configure(api_key=api_key)
            self.logger.info("Cliente de Gemini API configurado.")
        except Exception as e:
            self.logger.error(f"Error configurando Gemini: {e}")
            raise

    def _load_system_prompt(self) -> str:
        """Carga el system prompt desde el archivo .md."""
        prompt_path = Path("agents") / self.agent_name / "system_prompt.md"
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"System prompt no encontrado en: {prompt_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error cargando system prompt: {e}")
            raise

    def _build_prompt(self, student_text: str, student_level: str, target_level: str) -> str:
        """Construye el prompt final para enviar a la API de Gemini."""
        
        user_prompt = f"""
## Tarea de Evaluación

**Texto del estudiante:**
---
{student_text}
---

**Información del estudiante:**
- **Nivel actual declarado:** {student_level}
- **Nivel objetivo:** {target_level or 'No especificado'}

**Instrucciones:**
1.  Evalúa el texto proporcionado basándote estrictamente en los criterios TEF descritos en tu rol.
2.  Determina el nivel CECR alcanzado en este escrito.
3.  Asigna una puntuación para cada una de las 4 competencias (sobre 25 puntos cada una).
4.  Calcula la puntuación global (sobre 100).
5.  Proporciona un análisis detallado de puntos fuertes, áreas de mejora y errores.
6.  Ofrece recomendaciones concretas y accionables.
7.  Devuelve la evaluación completa en el formato JSON especificado, sin añadir ningún texto o explicación fuera del JSON.
"""
        return self.system_prompt + user_prompt

    def _parse_response(self, response_text: str) -> dict:
        """Parsea la respuesta JSON del modelo, con manejo de errores."""
        try:
            # Limpiar el string de respuesta para asegurar que solo contenga JSON
            json_str = response_text.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            return json.loads(json_str.strip())
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decodificando JSON de la respuesta: {e}")
            self.logger.debug(f"Respuesta recibida: {response_text}")
            raise ValueError("La respuesta del modelo no es un JSON válido.")
        except Exception as e:
            self.logger.error(f"Error inesperado al parsear la respuesta: {e}")
            raise

    def evaluate(self, student_text: str, student_level: str, target_level: str = None) -> dict:
        """
        Evalúa el texto de un estudiante.

        Args:
            student_text (str): El texto a evaluar.
            student_level (str): El nivel actual declarado por el estudiante.
            target_level (str, optional): El nivel que el estudiante aspira a alcanzar.

        Returns:
            dict: Un diccionario con la evaluación estructurada.
        """
        self.logger.info(f"Iniciando evaluación para estudiante de nivel {student_level}.")
        
        final_prompt = self._build_prompt(student_text, student_level, target_level)
        
        try:
            self.logger.info("Enviando petición a la API de Gemini.")
            
            model = genai.GenerativeModel(self.config.get("model", "gemini-pro"))
            response = model.generate_content(final_prompt)
            
            response_text = response.text
            self.logger.info("Respuesta recibida de la API.")
            
            evaluation = self._parse_response(response_text)
            
            self.logger.info(f"Evaluación completada. Nivel alcanzado: {evaluation.get('evaluation_results', {}).get('nivel_evaluado', 'N/A')}")
            return evaluation

        except Exception as e:
            self.logger.critical(f"Ha ocurrido un error crítico durante la evaluación: {e}", exc_info=True)
            return {
                "error": True,
                "message": str(e),
                "details": "No se pudo completar la evaluación debido a un error con la API de Gemini o un problema interno."
            }

if __name__ == '__main__':
    # Este bloque es para pruebas directas del agente
    print("🧪  Ejecutando prueba del TEF Writing Validator...")
    
    # Cargar configuración del sistema
    try:
        with open("config/system.json", "r", encoding="utf-8") as f:
            full_config = json.load(f)
        agent_config = full_config["agents"]["tef-writing-validator"]
    except (FileNotFoundError, KeyError) as e:
        print(f"❌ Error: No se pudo cargar la configuración del agente. {e}")
        exit(1)

    # Inicializar validador
    try:
        validator = TEFWritingValidator(config=agent_config)
    except ValueError as e:
        print(f"❌ Error de inicialización: {e}")
        print("    Asegúrate de que tu GEMINI_API_KEY es correcta en config/.env")
        exit(1)
    
    # Cargar texto de ejemplo
    try:
        with open("inputs/student_writings/exemple_lettre_b2.txt", "r", encoding="utf-8") as f:
            sample_text = f.read()
    except FileNotFoundError:
        print("❌ Error: Archivo de texto de ejemplo no encontrado.")
        exit(1)
        
    # Ejecutar evaluación
    print("\n" + "="*50)
    print("🚀 Ejecutando evaluación con el modelo configurado...")
    result = validator.evaluate(
        student_text=sample_text,
        student_level="B1",
        target_level="B2"
    )
    
    # Imprimir resultado
    print("\n" + "="*50)
    if result.get("error"):
        print("❌ Evaluación de prueba fallida.")
    else:
        print("✅ Evaluación de prueba completada.")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*50)
    
    log_file = Path("logs/agents/tef-writing-validator.log")
    if log_file.exists():
        print(f"\n📄 Log de la prueba disponible en: {log_file}")
