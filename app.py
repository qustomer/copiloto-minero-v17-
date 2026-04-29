import streamlit as st
import pandas as pd

from engines.ingestion_engine import run_ingestion_pipeline
from engines.scoring_engine import run_scoring_pipeline
from engines.survival_engine import calculate_survival_probability
from engines.solutions_catalog import apply_solutions_and_recalculate
from engines.pricing_engine import calculate_price # Nota el cambio de nombre a 'calculate_price'
from engines.automation_engine import run_harvester_automation
from engines.roi_engine import calculate_roi
from engines.proposal_pdf_generator import generate_dual_reports

st.set_page_config(layout="wide")
st.title("⛏️ Copiloto Minero v17 — Terminal Pericial")
with st.sidebar:
    st.header("Configuración de Control")
    modo_auto = st.toggle("Activar Automatización Total (Capa 8)", value=True)
# =====================================================
# SESSION STATE
# =====================================================

if "documents" not in st.session_state:
    st.session_state.documents = []

if "discarded_docs" not in st.session_state:
    st.session_state.discarded_docs = []

if "scoring_results" not in st.session_state:
    st.session_state.scoring_results = None

if "scenario_results" not in st.session_state:
    st.session_state.scenario_results = None

# =====================================================
# SIDEBAR — CONTEXTO PROYECTO
# =====================================================

st.sidebar.header("Contexto del Proyecto")

region = st.sidebar.selectbox("Región", ["NOA", "Cuyo", "Patagonia", "Centro"])
mineral = st.sidebar.selectbox("Mineral", ["Litio", "Cobre", "Oro/Plata", "Otros"])
phase = st.sidebar.selectbox(
    "Fase del Proyecto",
    ["Exploración", "Prefactibilidad", "Construcción", "Operación", "Cierre"]
)
tier = st.sidebar.selectbox("Tipo de Cliente", ["Major", "Mid", "Pyme"])

# =====================================================
# FASE 1 — INGESTA
# =====================================================

st.header("Fase 1 — Auditoría de Evidencia")

# =====================================================
# FASE 1 — INGESTA (AUTOMATIZADA O MANUAL)
# =====================================================
st.header("Fase 1 — Auditoría de Evidencia")

if modo_auto:
    st.info("SISTEMA EN MODO CAPA 8: Ingesta Web y Clasificación Automática activada.")
    col1, col2 = st.columns(2)
    with col1:
        # Usamos los datos de la sidebar para la búsqueda
        proyecto_nombre = st.text_input("Confirmar Nombre del Proyecto", value="Proyecto Alpha")
    with col2:
        st.write(f"**Región de rastreo:** {region}")
        st.write(f"**Mineral foco:** {mineral}")

    if st.button("Ejecutar Captura Automática y Scoring"):
        # Llamada al nuevo motor que creaste en el Paso 1
        new_docs = run_harvester_automation(proyecto_nombre, region)
        st.session_state.documents = new_docs.to_dict('records')
        
        # Ejecuta el scoring automáticamente tras la ingesta
        st.session_state.scoring_results = run_scoring_pipeline(
            st.session_state.documents, region, mineral, phase
        )
        st.success(f"Protocolo TGA cumplido: {len(new_docs)} fuentes procesadas de forma autónoma.")
else:
    # MANTIENE TU CÓDIGO ORIGINAL PARA CARGA MANUAL SI APAGAS EL MODO AUTO
    uploaded_files = st.file_uploader("Subir documentos", accept_multiple_files=True)
    axis = st.selectbox("Eje Heptágono", ["Político","Social","Ambiental","Hídrico","Económico","Técnico","Comunicacional"])
    source_type = st.selectbox("Tipo Fuente", ["Oficial","Terceros","Corporativo","Prensa"])
    recency = st.selectbox("Recencia", ["<18m","18-36m",">36m"])
    density = st.selectbox("Densidad Técnica", ["Alta","Media","Baja"])
    sentiment = st.selectbox("Sentimiento", ["Favor","Neutro","Contra"])

    if st.button("Agregar documentos manualmente"):
        if uploaded_files:
            new_docs, discarded = run_ingestion_pipeline(
                uploaded_files, axis, source_type, recency, density, sentiment
            )
            st.session_state.documents.extend(new_docs)
            st.session_state.discarded_docs.extend(discarded)

if st.session_state.discarded_docs:
    st.warning(f"{len(st.session_state.discarded_docs)} documentos descartados por duplicación")

# =====================================================
# EJECUTAR AUDITORÍA
# =====================================================

if st.button("Ejecutar Auditoría Forense"):
    st.session_state.scoring_results = run_scoring_pipeline(
        st.session_state.documents, region, mineral, phase
    )

# =====================================================
# RESULTADOS FORENSES
# =====================================================

if st.session_state.scoring_results:

    res = st.session_state.scoring_results

    st.header("Resultados Forenses")

    col1, col2, col3 = st.columns(3)
    col1.metric("IBH", round(res["IBH"],2))
    col2.metric("ICG", round(res["ICG"],2))
    col3.metric("Fricción", f"{res['friction']}%")

    # Curva supervivencia base
    isp_base = calculate_survival_probability(res["IBH"], res["friction"], phase)
    st.metric("ISP Base", f"{isp_base}%")

    # Curva simple supervivencia
    chart_data = pd.DataFrame({
        "Fase":["Actual","Siguiente"],
        "Supervivencia":[isp_base, isp_base*0.95]
    })
    st.line_chart(chart_data.set_index("Fase"))

    # =====================================================
    # WAR ROOM
    # =====================================================

    st.header("War Room — Simulación")

    selected_solutions = st.multiselect(
        "Seleccionar soluciones",
        [
            "Monitoreo Hídrico Participativo",
            "Programa Relacionamiento Indígena",
            "Sistema Alertas Ambientales",
            "Plan Comunicación Estratégica"
        ]
    )

    if st.button("Simular Escenario"):
        scenario = apply_solutions_and_recalculate(
            res, selected_solutions, region, mineral, phase
        )

        # recalcular ISP proyectado
        scenario["ISP"] = calculate_survival_probability(
            scenario["IBH"], scenario["friction"], phase
        )

        st.session_state.scenario_results = scenario

# =====================================================
# ESCENARIO + PRICING
# =====================================================

if st.session_state.scenario_results:

    scenario = st.session_state.scenario_results

    st.header("Escenario Proyectado")

    col1, col2, col3 = st.columns(3)
    col1.metric("IBH Proyectado", round(scenario["IBH"],2))
    col2.metric("Fricción", f"{scenario['friction']}%")
    col3.metric("ISP", f"{scenario['ISP']}%")

    pricing = calculate_project_pricing(
        ibh=scenario["IBH"],
        friction=scenario["friction"],
        isp=scenario["ISP"],
        tier=tier,
    )

    st.header("Inversión Estimada")
    col1, col2 = st.columns(2)
    col1.metric("Fee USD", f"${pricing['total_usd']}")
    col2.metric("Fee ARS", f"${pricing['total_ars']}")

    roi = calculate_roi(pricing["total_usd"])
    st.metric("Margen", f"{roi['margin']}%")

    # =====================================================
    # GENERAR REPORTES (JUEZ FINAL)
    # =====================================================

    st.header("Generación de Reportes")

    if st.button("Generar Reportes PDF"):

        icg = st.session_state.scoring_results["ICG"]

        if icg < 50:
            st.warning("ICG < 50 → Se generará propuesta FBE obligatoria")
        else:
            st.success("Certidumbre validada → Generando Reportes Dual")

        generate_dual_reports(
            scoring=st.session_state.scoring_results,
            scenario=scenario,
            pricing=pricing,
            roi=roi
        )

        st.success("Reportes generados ✔")
