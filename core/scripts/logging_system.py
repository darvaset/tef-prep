#!/usr/bin/env python3
"""
Sistema de Logging para TEF Preparation System
"""

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
        """Log de ejecución completa de un agente"""
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
