import streamlit as st
import pandas as pd

# Importaciones sincronizadas con la estructura de tu carpeta /engines
from engines.ingestion_engine import run_ingestion_pipeline
from engines.scoring_engine import run_scoring_pipeline
from engines.war_room_engine import apply_solutions_and_recalculate
from engines.pricing_engine import calculate_price
from engines.proposal_pdf_generator import generate_dual_reports
from engines.automation_engine import run_harvester_automation

st.set_page_config(layout="wide", page_title="Copiloto Minero v17")

# Encabezado Profesional
st.title("⛏️ Copiloto Minero v17 — Terminal Pericial")
st.markdown("### **Claudio Falasca Consultor Minero**")

# =====================================================
# PANEL DE CONTROL (SIDEBAR)
# =====================================================
with st.sidebar:
    st.header("Configuración de Control")
    modo_auto = st.toggle("Activar Automatización Total (Capa 8)", value=True)
    
    st.divider()
    st.header("Contexto del Proyecto")
    region = st.selectbox("Región", ["NOA", "Cuyo", "Patagonia", "Centro"])
    mineral = st.selectbox("Mineral", ["Litio", "Cobre", "Oro/Plata", "Otros"])
    phase = st.selectbox(
        "Fase del Proyecto",
        ["Exploración", "Prefactibilidad", "Construcción", "Operación", "Cierre"]
    )

# =====================================================
# FASE 1 — INGESTA DE EVIDENCIA
# =====================================================
st.header("Fase 1 — Auditoría de Evidencia")

if modo_auto:
    st.info("🛰️ MODO CAPA 8: Ingesta Autónoma y Clasificación NLP activa.")
    proyecto_nombre = st.text_input("Nombre del Proyecto para Rastreo Web", value="Proyecto Alpha")
    
    if st.button("Ejecutar Captura y Scoring Automático"):
        # El motor genera las 110 fuentes para rigor TGA de forma autónoma
        df_auto = run_harvester_automation(proyecto_nombre, region)
        st.session_state.docs_accepted = df_auto
        
        # Ejecución inmediata del scoring con los datos succionados
        st.session_state.results = run_scoring_pipeline(df_auto, region, mineral, phase)
        st.success(f"Protocolo TGA cumplido: {len(df_auto)} fuentes procesadas automáticamente.")
else:
    # Modo Manual (Preservado por seguridad)
    uploaded_files = st.file_uploader("Subir evidencia manual", accept_multiple_files=True)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        eje = st.selectbox("Eje Heptágono", ["Político", "Social", "Ambiental", "Hídrico", "Económico", "Técnico", "Comunicacional"])
    with col_m2:
        calidad = st.selectbox("Calidad", ["Alta", "Media", "Baja"])
    with col_m3:
        sentimiento = st.selectbox("Sentimiento", ["Favor", "Neutro", "Contra"])

    if st.button("Procesar Ingesta Manual") and uploaded_files:
        from engines.ingestion_engine import init_document_db, add_documents_batch, eddf_filter
        db = init_document_db()
        batch = add_documents_batch(db, uploaded_files, eje, calidad, sentimiento)
        st.session_state.docs_accepted = eddf_filter(batch)

# Mostrar Tabla de Evidencia si existen datos
if "docs_accepted" in st.session_state:
    st.subheader("Base de Evidencia Validada")
    st.dataframe(st.session_state.docs_accepted, use_container_width=True)

# =====================================================
# FASE 2 — DIAGNÓSTICO Y HONORARIOS
# =====================================================
if "results" in st.session_state:
    res = st.session_state.results
    st.divider()
    st.header("Fase 2 — Diagnóstico de Riesgo y Honorarios")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("IBH (Balance)", f"{res['IBH']}%")
    kpi2.metric("Fricción", f"{res['Friccion']}%")
    kpi3.metric("ISP (Supervivencia)", f"{res['ISP']}%")
    kpi4.metric("ICG (Certidumbre)", res["ICG"])

    # Cálculo de Honorarios (Pricing Engine)
    # Pasamos los 3 parámetros que pide tu función física en pricing_engine.py
    honorarios = calculate_price(res["IBH"], res["Friccion"], res["ISP"])
    
    st.subheader("Inversión Estimada en Gestión Socio-Ambiental")
    st.metric("Fee Profesional Sugerido", f"USD {honorarios:,.0f}")

    if st.button("Generar Reporte Pericial PDF"):
        generate_dual_reports(res, honorarios)
        st.success("Reporte generado exitosamente.")
