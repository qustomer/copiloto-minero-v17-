def calculate_survival_probability(ibh, friction, phase):
    """
    Modelo simplificado de supervivencia del proyecto minero.
    Devuelve ISP (%) = probabilidad de que el proyecto avance sin interrupciones críticas.
    """

    # Base survival por fase
    phase_factor = {
        "Exploración": 0.55,
        "Prefactibilidad": 0.65,
        "Construcción": 0.75,
        "Operación": 0.85,
        "Cierre": 0.90
    }

    base = phase_factor.get(phase, 0.65)

    # Penalización por fricción social/ambiental
    friction_penalty = friction / 100 * 0.5

    # Impacto del IBH (legitimidad social)
    ibh_boost = (ibh / 100) * 0.4

    survival_score = base - friction_penalty + ibh_boost

    # Limitar entre 5% y 95%
    survival_score = max(0.05, min(0.95, survival_score))

    return round(survival_score * 100, 1)
