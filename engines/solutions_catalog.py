# engines/solutions_catalog.py

# Catálogo base de soluciones del Copiloto Minero
# Cada solución impacta ejes del Heptágono y activa servicios

SOLUTIONS_CATALOG = {
    "Monitoreo Hídrico Participativo": {
        "axes_impact": {"Hidrico": 8, "Social": 4},
        "services": ["Hydro Monitoring Program"],
        "survival_boost": 0.05,
        "price_factor": 1.15
    },
    "Mesa de Diálogo Territorial": {
        "axes_impact": {"Social": 10, "Territorial": 6},
        "services": ["Stakeholder Engagement Program"],
        "survival_boost": 0.08,
        "price_factor": 1.20
    },
    "Auditoría Ambiental Independiente": {
        "axes_impact": {"Ambiental": 9},
        "services": ["Environmental Audit"],
        "survival_boost": 0.06,
        "price_factor": 1.18
    },
    "Plan de Relacionamiento Indígena": {
        "axes_impact": {"Social": 12, "Territorial": 5},
        "services": ["Indigenous Engagement Protocol"],
        "survival_boost": 0.10,
        "price_factor": 1.22
    },
    "Programa de Transparencia y Comunicación": {
        "axes_impact": {"Social": 6, "Politico": 4},
        "services": ["Strategic Communications"],
        "survival_boost": 0.04,
        "price_factor": 1.12
    }
}


def apply_solutions(base_scores, selected_solutions):
    """
    Aplica mejoras de score al seleccionar soluciones en el War Room
    """
    new_scores = base_scores.copy()
    activated_services = []
    survival_multiplier = 1
    pricing_multiplier = 1

    for sol in selected_solutions:
        if sol not in SOLUTIONS_CATALOG:
            continue

        data = SOLUTIONS_CATALOG[sol]

        # Impacto en ejes
        for axis, impact in data["axes_impact"].items():
            new_scores[axis] = min(100, new_scores.get(axis, 0) + impact)

        # Servicios activados
        activated_services.extend(data["services"])

        # Impacto supervivencia
        survival_multiplier += data["survival_boost"]

        # Impacto pricing
        pricing_multiplier *= data["price_factor"]

    return new_scores, list(set(activated_services)), survival_multiplier, pricing_multiplier
