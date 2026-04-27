import streamlit as st
import pandas as pd

from engines.ingestion_engine import run_ingestion_pipeline
from engines.scoring_engine import run_scoring_pipeline
from engines.survival_engine import calculate_survival_probability
from engines.solutions_engine import apply_solutions_and_recalculate
from engines.pricing_engine import calculate_project_pricing
from engines.roi_engine import calculate_roi
from engines.proposal_pdf_generator import generate_dual_reports


st.set_page_config(layout="wide")
st.title("⛏️ Copiloto Minero v17 — Terminal Pericial")

# =========================================================
# SESSION STATE INIT
# =========================================================

if "documents" not in st.session_state:
    st.session_state.documents = []

if "scoring_results" not in st.session_state:
    st.session_state.scoring_results = None

if "scenario_results" not in st.session_state:
    st.session_state.scenario_results = None

# =========================================================
# SIDEBAR CONTEXTO PROYECTO
# =========================================================

st.sidebar.header("Contexto del Proyecto")

region = st.sidebar.selectbox(
    "Región", ["NOA", "Cuyo", "Patagonia", "Centro"]
)

mineral = st.sidebar.selectbox(
    "Mineral", ["Litio", "Cobre", "Oro/Plata", "Otros"]
)

phase = st.sidebar.selectbox(
    "Fase del Proyecto",
    ["Exploración", "Prefactibilidad", "Construcción", "Operación", "Cierre"]
)

tier = st.sidebar.selectbox(
    "Tipo de Cliente",
    ["Major", "Mid", "Pyme"]
)

# =========================================================
# FASE 1 — INGESTA DOCUMENTAL
# =========================================================

st.header("Fase 1 — Auditoría de Evidencia")

uploaded_files = st.file_uploader(
    "Subir documentos", accept_multiple_files=True
)

axis = st.selectbox(
    "Eje Heptágono del documento",
    ["Político","Social","Ambiental","Hídrico","Económico","Técnico","Comunicacional"]
)

source_type = st.selectbox(
    "Tipo de Fuente",
    ["Oficial","Terceros","Corporativo","Prensa"]
)

recency = st.selectbox(
    "Recencia",
    ["<18m","18-36m",">36m"]
)

density = st.selectbox(
    "Densidad técnica",
    ["Alta","Media","Baja"]
)

sentiment = st.selectbox(
    "Sentimiento",
    ["Favor","Neutro","Contra"]
)

if st.button("Agregar documentos"):
    if uploaded_files:
        new_docs = run_ingestion_pipeline(
            uploaded_files,
            axis,
            source_type,
            recency,
            density,
            sentiment,
        )
        st.session_state.documents.extend(new_docs)
        st.success(f"{len(new_docs)} documentos agregados")

st.write("Documentos cargados:", len(st.session_state.documents))

# =========================================================
# RUN SCORING PIPELINE
# =========================================================

if st.button("Ejecutar Auditoría"):
    st.session_state.scoring_results = run_scoring_pipeline(
        st.session_state.documents,
        region,
        mineral,
        phase
    )

# =========================================================
# RESULTADOS FORENSES
# =========================================================

if st.session_state.scoring_results:

    res = st.session_state.scoring_results

    st.header("Resultados Forenses")

    col1, col2, col3 = st.columns(3)
    col1.metric("IBH Forense", round(res["IBH"], 2))
    col2.metric("ICG", round(res["ICG"], 2))
    col3.metric("Fricción Crítica", str(res["friction"]) + "%")

    # =====================================================
    # SURVIVAL ENGINE
    # =====================================================

    isp = calculate_survival_probability(res["IBH"], res["friction"], phase)
    st.metric("Probabilidad de Supervivencia (ISP)", str(isp) + "%")

    # =====================================================
    # WAR ROOM — SOLUCIONES
    # =====================================================

    st.header("War Room — Simulación de Soluciones")

    selected_solutions = st.multiselect(
        "Seleccionar soluciones",
        [
            "Monitoreo Hídrico Participativo",
            "Programa de Relacionamiento Indígena",
            "Sistema de Alertas Ambientales",
            "Plan de Comunicación Estratégica",
        ],
    )

    if st.button("Simular escenario"):
        scenario = apply_solutions_and_recalculate(
            res,
            selected_solutions,
            region,
            mineral,
            phase
        )
        st.session_state.scenario_results = scenario

# =========================================================
# RESULTADOS SIMULADOS + PRICING
# =========================================================

if st.session_state.scenario_results:

    scenario = st.session_state.scenario_results

    st.header("Escenario Proyectado")

    col1, col2 = st.columns(2)
    col1.metric("IBH Proyectado", round(scenario["IBH"], 2))
    col2.metric("Fricción Proyectada", str(scenario["friction"]) + "%")

    # =============================
    # PRICING ENGINE
    # =============================

    pricing = calculate_project_pricing(
        ibh=scenario["IBH"],
        friction=scenario["friction"],
        isp=scenario["ISP"],
        tier=tier,
    )

    st.header("Inversión Estimada")
    st.metric("Fee Total USD", "$ " + str(pricing["total_usd"]))
    st.metric("Fee Total ARS", "$ " + str(pricing["total_ars"]))

    # =============================
    # ROI ENGINE
    # =============================

    roi = calculate_roi(pricing["total_usd"])
    st.metric("Margen estimado", str(roi["margin"]) + "%")

    # =============================
    # GENERADOR DE REPORTES
    # =============================

    st.header("Generación de Reportes")

    if st.button("Generar Reportes PDF"):

        icg = st.session_state.scoring_results["ICG"]

        if icg < 50:
            st.warning("ICG insuficiente → se generará propuesta FBE")

        generate_dual_reports(
            scoring=st.session_state.scoring_results,
            scenario=scenario,
            pricing=pricing,
            roi=roi
        )

        st.success("Reportes generados ✔")
