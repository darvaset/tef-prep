### Sección 1: Estructura del Proyecto
```
TEF-Prep/
├── core/           # Lógica de agentes y orquestación
├── streamlit/      # UI web (MVP)
├── data/           # inputs, outputs, logs
├── docs/           # Documentación
└── tests/          # Tests
```

### Sección 2: Instalación
```bash
# Clonar repo
git clone [repo-url]
cd TEF-Prep

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp core/config/.env.example core/config/.env
# Editar .env y agregar GEMINI_API_KEY
```

### Sección 3: Uso - CLI

**Comando: status**
```bash
python -m core.tef_system status
```

**Comando: evaluate** (detección automática de nivel)
```bash
python -m core.tef_system evaluate --input="data/inputs/student_writings/texto.txt"
```

**Comando: evaluate** (nivel objetivo específico)
```bash
python -m core.tef_system evaluate --input="data/inputs/student_writings/texto.txt" --level="B2"
```

**Comando: improve** (generar plan desde feedback)
```bash
python -m core.tef_system improve --feedback="data/outputs/feedback/[archivo].json"
python -m core.tef_system improve --feedback="data/outputs/feedback/[archivo].json" --mode="intensive"
```

**Comando: research** (buscar recursos)
```bash
python -m core.tef_system research --topic="subjonctif" --level="B2" --competency="grammaire"
```

### Sección 4: Uso - Streamlit UI
```bash
streamlit run streamlit/app.py
```
Abrir http://localhost:8501 en el navegador.

### Sección 5: Outputs

Los archivos generados se guardan en:
- `data/outputs/feedback/` - Evaluaciones JSON
- `data/outputs/study_plans/` - Planes de estudio Markdown
- `data/logs/` - Logs del sistema