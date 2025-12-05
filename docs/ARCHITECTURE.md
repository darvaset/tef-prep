# TEF Preparation System - Architecture

## Overview
Sistema de preparación TEF con 3 agentes AI especializados y UI web.

## Components

### Core (`core/`)
- `tef_system.py` - Orquestador principal
- `agents/tef_writing_validator.py` - Evalúa escritos
- `agents/tef_improvement_advisor.py` - Genera planes de mejora
- `agents/tef_resource_researcher.py` - Busca recursos educativos

### UI (`streamlit/`)
- `app.py` - Aplicación Streamlit MVP

### Data Flow
```
User Text → Validator → Feedback → Advisor → Plan → Researcher → Resources
                                                          ↓
                                              Consolidated Response
```

### Key Methods

**CLI (file-based):**
- `evaluate_writing()` - Evalúa y guarda feedback.json
- `improve_plan()` - Genera plan desde feedback.json
- `research_resources()` - Busca recursos por tema

**UI (memory-based):**
- `full_pipeline(text, exercise_type, mode)` - Todo en una llamada, retorna dict

## Configuration
- `core/config/system.json` - Configuración de agentes
- `core/config/.env` - API keys (no commitear)

## Models Used
- Gemini 2.5 Flash para todos los agentes
