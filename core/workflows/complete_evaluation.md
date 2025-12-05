# Complete Evaluation Workflow

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
- Guardar resultado en `data/outputs/feedback/`

### 3. Análisis de Mejora (TEF Improvement Advisor)  
- Procesar feedback del validator
- Identificar patrones y prioridades
- Generar plan de estudio personalizado
- Guardar plan en `data/outputs/study_plans/`

### 4. Investigación de Recursos (TEF Resource Researcher)
- Extraer temas de mejora del plan
- Buscar recursos específicos online
- Validar y curar recomendaciones
- Guardar recursos en `data/outputs/resources/`

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
python -m core.tef_system complete-evaluation   --input="data/inputs/student_writings/ensayo_001.txt"   --student-level="B1"   --target-level="B2"   --urgency="normal"
```
