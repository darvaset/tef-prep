# Próximos Pasos - TEF Preparation System

## Para la próxima sesión

### Arquitectura y API
- [ ] Crear documento de Arquitectura y Contratos de API
- [ ] Definir endpoints REST (POST /evaluate, POST /improve)
- [ ] Definir modelos de datos (User, Evaluation, StudyPlan)

### MVP Streamlit
- [ ] Crear estructura del proyecto `tef-streamlit/`
- [ ] Implementar `app.py` básico con:
  - Input de texto
  - Selector de modo (Normal/Intensivo)
  - Visualización de feedback
  - Visualización de plan de estudio
  - Descarga de PDF

### Backend
- [ ] Crear `tef-api/` con FastAPI
- [ ] Exponer endpoints que consuman `tef-core`
- [ ] Dockerizar el backend

### Mejoras pendientes del core
- [ ] Añadir generación de PDF del plan de estudio
- [ ] Considerar planes premium (A2→C1 completo)

### Bugs conocidos (prioridad baja)
- [ ] Fix filename de study_plan: incluir modo (normal/intensive) y timestamp de generación para evitar sobrescritura

