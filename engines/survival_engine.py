# engines/survival_engine.py
# ----------------------------------------------------
# Mining Survival Engine (MSM)
# Modelo simplificado tipo Cox + Kaplan-Meier simulada
# Calcula ISP = Índice de Supervivencia Proyectada
# ----------------------------------------------------

import math


# ----------------------------------------------------
# Coeficientes de riesgo por fase del proyecto
# (aproximación tipo Cox Proportional Hazards)
# ----------------------------------------------------
PHASE_COEFFICIENTS = {
    "Exploracion": {
        "politico": 0.30,
        "legal": 0.30,
        "social": 0.15,
        "ambiental": 0.10,
        "hidrico": 0.05,
        "economico": 0.05,
        "tecnico": 0.05,
    },
    "Factibilidad": {
        "social": 0.25,
        "hidrico": 0.20,
        "ambiental": 0.20,
        "economico": 0.15,
        "politico": 0.10,
        "legal": 0.05,
        "tecnico": 0.05,
    },
    "Construccion": {
        "economico": 0.25,
        "ambiental": 0.25,
        "hidrico": 0.20,
        "social": 0.15,
        "tecnico": 0.10,
        "politico": 0.03,
        "legal": 0.02,
    },
    "Operacion": {
        "ambiental": 0.30,
        "social": 0.25,
        "hidrico": 0.20,
        "economico": 0.10,
        "politico": 0.05,
        "legal": 0.05,
        "tecnico": 0.05,
    },
    "Cierre": {
        "ambiental": 0.35,
        "social": 0.25,
        "economico": 0.15,
        "politico": 0.10,
        "legal": 0.10,
        "hidrico": 0.03,
        "tecnico": 0.02,
    },
}


# ----------------------------------------------------
# Función principal — calcular ISP
# ----------------------------------------------------
def calculate_survival_index(axis_scores: dict, phase: str):
    """
    axis_scores → scores 0-100 por eje
    phase → fase del proyecto minero
    """

    coeffs = PHASE_COEFFICIENTS.get(phase, PHASE_COEFFICIENTS["Exploracion"])

    # Convertimos scores a riesgo (1 - score)
    hazard_sum = 0
    for axis, coef in coeffs.items():
        score = axis_scores.get(axis, 50) / 100
        risk = 1 - score
        hazard_sum += coef * risk

    # Modelo simplificado tipo Cox
    baseline_hazard = 0.35
    hazard_rate = baseline_hazard + hazard_sum

    # Supervivencia tipo Kaplan-Meier simulada
    survival_probability = math.exp(-hazard_rate)

    ISP = round(survival_probability * 100, 2)

    return ISP


# ----------------------------------------------------
# Curva de supervivencia simulada (para gráfico)
# ----------------------------------------------------
def generate_survival_curve(current_isp, projected_isp):
    """
    Genera puntos para curva simple en Streamlit
    """

    curve = {
        "Etapa": ["Hoy", "12 meses", "24 meses"],
        "Base": [
            current_isp,
            max(current_isp - 10, 5),
            max(current_isp - 20, 3),
        ],
        "Escenario con Soluciones": [
            projected_isp,
            max(projected_isp - 5, 10),
            max(projected_isp - 10, 5),
        ],
    }

    return curve
