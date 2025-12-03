#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEF Resource Researcher Agent

Este agente investiga recursos educativos en la web utilizando la
Google Custom Search API.

Autor: Diego | QA Engineering Manager
Fecha: Noviembre 2025
"""

import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime

class TEFResourceResearcher:
    """
    Agente para investigar recursos educativos para el TEF.
    """
    def __init__(self, config: dict, logger: logging.Logger = None):
        """
        Inicializa el investigador de recursos.

        Args:
            config (dict): Configuración del agente desde system.json.
            logger (logging.Logger, optional): Logger para el agente.
        """
        self.config = config
        self.agent_name = "tef-resource-researcher"
        
        if logger:
            self.logger = logger
        else:
            self._setup_logging()

        self._setup_search_api()
        
        self.logger.info("TEF Resource Researcher inicializado correctamente.")

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

    def _setup_search_api(self):
        """Configura el cliente de la API de búsqueda personalizada de Google."""
        try:
            load_dotenv(dotenv_path=Path("config/.env"))
            self.api_key = os.getenv("SEARCH_API_KEY")
            self.cse_id = os.getenv("SEARCH_ENGINE_ID")

            if not self.api_key or self.api_key == "your_search_api_key_here":
                self.logger.error("La SEARCH_API_KEY no está configurada en config/.env")
                raise ValueError("SEARCH_API_KEY no encontrada.")
            if not self.cse_id or self.cse_id == "your_search_engine_id_here":
                self.logger.error("El SEARCH_ENGINE_ID no está configurado en config/.env")
                raise ValueError("SEARCH_ENGINE_ID no encontrado.")
            
            self.service = build("customsearch", "v1", developerKey=self.api_key)
            self.logger.info("Cliente de Google Custom Search API configurado.")
        except Exception as e:
            self.logger.error(f"Error configurando la API de búsqueda: {e}")
            raise

    def research(self, topic: str, level: str, competency: str = "writing", num_results: int = 5) -> dict:
        """
        Realiza una investigación de recursos para un tema, nivel y competencia dados.

        Args:
            topic (str): El tema a investigar (ej. "subjonctif").
            level (str): El nivel TEF objetivo (ej. "B2").
            competency (str): La competencia específica (ej. "writing").
            num_results (int): Número máximo de resultados a devolver.

        Returns:
            dict: Un diccionario con los resultados de la búsqueda.
        """
        self.logger.info(f"Iniciando investigación para '{topic}' (Nivel: {level}, Competencia: {competency}).")
        
        # Simplificar la consulta para aumentar las posibilidades de encontrar resultados
        query = f"francés {topic} {level} {competency}"
        
        try:
            self.logger.info(f"Realizando búsqueda con la consulta: '{query}'")
            print(f"DEBUG: Consulta enviada a Google Custom Search: '{query}'") # Debug print
            res = self.service.cse().list(q=query, cx=self.cse_id, num=num_results).execute()
            
            search_results = []
            if 'items' in res:
                for item in res['items']:
                    search_results.append({
                        "title": item.get('title'),
                        "link": item.get('link'),
                        "snippet": item.get('snippet')
                    })
            
            self.logger.info(f"Investigación completada. Se encontraron {len(search_results)} resultados.")
            return {
                "status": "success",
                "query": query,
                "results": search_results,
                "metadata": {
                    "topic": topic,
                    "level": level,
                    "competency": competency,
                    "timestamp": datetime.datetime.now().isoformat()
                }
            }

        except Exception as e:
            self.logger.critical(f"Ha ocurrido un error crítico durante la investigación: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "details": "No se pudo completar la investigación debido a un error con la API de búsqueda o un problema interno."
            }

if __name__ == '__main__':
    # Este bloque es para pruebas directas del agente
    print("🧪  Ejecutando prueba del TEF Resource Researcher...")
    
    # Cargar configuración del sistema
    try:
        with open("config/system.json", "r", encoding="utf-8") as f:
            full_config = json.load(f)
        agent_config = full_config["agents"]["tef-resource-researcher"]
    except (FileNotFoundError, KeyError) as e:
        print(f"❌ Error: No se pudo cargar la configuración del agente. {e}")
        exit(1)

    # Inicializar investigador
    try:
        researcher = TEFResourceResearcher(config=agent_config)
    except ValueError as e:
        print(f"❌ Error de inicialización: {e}")
        print("    Asegúrate de que tus claves SEARCH_API_KEY y SEARCH_ENGINE_ID son correctas en config/.env")
        exit(1)
    
    # Ejecutar investigación de prueba
    print("\n" + "="*50)
    print("🚀 Ejecutando investigación de prueba...")
    test_topic = "subjonctif"
    test_level = "B2"
    test_competency = "grammaire"
    
    result = researcher.research(
        topic=test_topic,
        level=test_level,
        competency=test_competency
    )
    
    # Imprimir resultado
    print("\n" + "="*50)
    if result.get("status") == "error":
        print("❌ Investigación de prueba fallida.")
    else:
        print("✅ Investigación de prueba completada.")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*50)
    
    log_file = Path("logs/agents/tef-resource-researcher.log")
    if log_file.exists():
        print(f"\n📄 Log de la prueba disponible en: {log_file}")
