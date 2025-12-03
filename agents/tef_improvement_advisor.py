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

    def generate_plan(self, feedback_data):
        """
        Genera un plan de estudio personalizado a partir de los datos de feedback.

        Args:
            feedback_data (dict): Un diccionario con los resultados de la evaluación.

        Returns:
            str: El plan de estudio generado en formato Markdown.
        """
        if not isinstance(feedback_data, dict):
            return {"status": "error", "message": "El feedback debe ser un diccionario."}

        # Extraer las secciones clave para el prompt
        try:
            nivel_alcanzado = feedback_data.get("nivel_alcanzado", "No especificado")
            areas_mejora = feedback_data.get("areas_mejora", [])
            errores_frecuentes = feedback_data.get("errores_frecuentes", [])
            recomendaciones = feedback_data.get("recomendaciones", [])

            if not any([areas_mejora, errores_frecuentes, recomendaciones]):
                return {"status": "error", "message": "El feedback no contiene información suficiente para generar un plan."}

        except Exception as e:
            return {"status": "error", "message": f"Error al procesar los datos de feedback: {e}"}

        # Construir el contexto para el prompt del usuario
        user_prompt_context = f"""
## CONTEXTO DE LA EVALUACIÓN DEL ESTUDIANTE

Aquí tienes el resumen del feedback recibido por el estudiante. Tu tarea es usar esta información para crear el plan de estudio personalizado como se te indicó en tu rol de sistema.

- **Nivel Alcanzado**: {nivel_alcanzado}

- **Áreas de Mejora Identificadas**:
{self._format_list(areas_mejora)}

- **Errores Frecuentes Detectados**:
{self._format_list(errores_frecuentes)}

- **Recomendaciones Sugeridas**:
{self._format_list(recomendaciones)}
"""

        # Crear la sesión de chat con el modelo
        try:
            chat = self.model.start_chat(history=[
                {'role': 'user', 'parts': [self.system_prompt]},
                {'role': 'model', 'parts': ["Entendido. Estoy listo para recibir el feedback del estudiante y crear su plan de estudio personalizado."]}
            ])
            
            response = chat.send_message(user_prompt_context)
            
            # Limpiar la respuesta para asegurar que solo contenga el plan
            plan_content = response.text.strip()
            
            return {"status": "success", "plan": plan_content}

        except Exception as e:
            return {"status": "error", "message": f"Error al generar el plan con el modelo de IA: {e}"}

    def _format_list(self, items):
        """Formatea una lista en una cadena de viñetas para el prompt."""
        if not items:
            return "- (Ninguno)"
        return "\n".join(f"- {item}" for item in items)
