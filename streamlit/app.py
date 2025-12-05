"""
TEF Writing Evaluator - Streamlit MVP
=====================================
UI para evaluar textos en francés y generar planes de mejora.
"""
import streamlit as st
import sys
from pathlib import Path

# Agregar core al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.tef_system import TEFSystem

st.set_page_config(
    page_title="TEF Writing Evaluator",
    page_icon="🇫🇷",
    layout="wide"
)

st.title("🇫🇷 TEF Writing Evaluator")
st.markdown("*Evaluate your French writing and get personalized improvement plans*")

# Input section
st.subheader("Your Text")
texto = st.text_area(
    "Paste your French text here:",
    height=250,
    placeholder="Écrivez votre texte en français ici..."
)

col1, col2 = st.columns(2)
with col1:
    exercise_type = st.selectbox(
        "Exercise Type:",
        ["Formal Letter", "Informal Letter", "Article", "Essay"]
    )
with col2:
    mode = st.selectbox(
        "Study Plan Mode:",
        ["normal", "intensive"]
    )

# Evaluation button
if st.button("✨ Evaluate My Text", type="primary", use_container_width=True):
    if not texto.strip():
        st.error("Please enter some text to evaluate.")
    else:
        with st.spinner("Analyzing your text... This may take 30-60 seconds."):
            try:
                system = TEFSystem()
                results = system.full_pipeline(texto, exercise_type, mode)
                
                if results["status"] == "error":
                    st.error(f"Error: {results['message']}")
                else:
                    # Success - show results in tabs
                    st.success("Evaluation complete!")
                    
                    # Metrics row
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Detected Level", results["nivel_detectado"])
                    col2.metric("Target Level", results["nivel_objetivo"])
                    col3.metric("Global Score", f"{results['score_global']}/100")
                    
                    # Tabs for detailed results
                    tab1, tab2 = st.tabs(["📊 Feedback", "📚 Study Plan"])
                    
                    with tab1:
                        st.json(results["feedback"])
                    
                    with tab2:
                        st.markdown(results["study_plan"])
                        
            except Exception as e:
                st.error(f"System error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Built with Claude & Gemini for TEF exam preparation*")