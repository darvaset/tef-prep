import json
# -*- coding: utf-8 -*-
"""
TEF Improvement Advisor Agent

Este agente se especializa en crear planes de mejora personalizados
basados en el feedback de una evaluación de escritura TEF.
"""

import google.generativeai as genai
from pathlib import Path
import os

class TEFImprovementAdvisor:
    """
    Agente que analiza el feedback de una evaluación y genera un plan de estudio.
    """
    def __init__(self, config):
        """
        Inicializa el agente con su configuración y el modelo de IA.
        """
        self.config = config
        self.model_name = config.get("model", "gemini-pro")
        self.agent_path = Path(os.path.dirname(__file__))
        self.system_prompt = self._load_system_prompt()
        
        # Configurar la API de Google
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise ValueError(f"Error al configurar el modelo de IA: {e}")

    def _load_system_prompt(self):
        """
        Carga el prompt del sistema desde el archivo correspondiente.
        """
        prompt_path = self.agent_path / "tef-improvement-advisor" / "system_prompt.md"
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo de system prompt en: {prompt_path}")

    def generate_plan(self, feedback_data: dict, mode: str = "normal") -> dict:
        """
        Genera un plan de estudio personalizado a partir de los datos de feedback.

        Args:
            feedback_data (dict): Un diccionario con los resultados de la evaluación.
            mode (str): El modo del plan de estudio ('normal' o 'intensive').

        Returns:
            str: El plan de estudio generado en formato Markdown.
        """
        if not isinstance(feedback_data, dict):
            return {"status": "error", "message": "El feedback debe ser un diccionario."}

        try:
            # Extraer la nueva estructura de datos del feedback
            context_data = {
                "nivel_detectado": feedback_data.get("nivel_detectado", "N/A"),
                "nivel_objetivo": feedback_data.get("nivel_objetivo", "N/A"),
                "brecha_nivel": feedback_data.get("brecha_nivel", {}),
                "areas_mejora": feedback_data.get("areas_mejora", []),
                "errores_frecuentes": feedback_data.get("errores_frecuentes", [])
            }

            if context_data["nivel_detectado"] == "N/A":
                return {"status": "error", "message": "El feedback no contiene el campo requerido 'nivel_detectado'."}

        except Exception as e:
            return {"status": "error", "message": f"Error al procesar los datos de feedback: {e}"}

        # Construir el contexto para el prompt del usuario
        user_prompt = f"""
## CONTEXTO PARA EL PLAN DE ESTUDIO

**Feedback del Estudiante:**
```json
{{
  "nivel_detectado": "{context_data['nivel_detectado']}",
  "nivel_objetivo": "{context_data['nivel_objetivo']}",
  "brecha_nivel": {json.dumps(context_data['brecha_nivel'])},
  "areas_mejora": {json.dumps(context_data['areas_mejora'])},
  "errores_frecuentes": {json.dumps(context_data['errores_frecuentes'])}
}}
```

**Modo de Plan Solicitado:**
- **modo_plan**: "{mode}"

**Tu Tarea:**
Genera el plan de estudio personalizado en formato Markdown siguiendo TODAS las instrucciones de tu rol (Contexto, Modos, Formato de Output).
"""

        # Crear la sesión de chat con el modelo
        try:
            chat = self.model.start_chat(history=[
                {'role': 'user', 'parts': [self.system_prompt]},
                {'role': 'model', 'parts': ["Entendido. Estoy listo para recibir el contexto y el modo del plan para generar la hoja de ruta del estudiante."]}
            ])
            
            response = chat.send_message(user_prompt)
            
            plan_content = response.text.strip()
            
            return {"status": "success", "plan": plan_content}

        except Exception as e:
            return {"status": "error", "message": f"Error al generar el plan con el modelo de IA: {e}"}

    def _format_list(self, items):
        """Formatea una lista en una cadena de viñetas para el prompt."""
        if not items:
            return "- (Ninguno)"
        return "\n".join(f"- {item}" for item in items)
