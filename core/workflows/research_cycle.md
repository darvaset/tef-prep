# Research Cycle Workflow

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
python tef_system.py research   --topic="subjonctif"   --level="B2"   --competency="writing"   --resource-types="ejercicio,guía"
```
