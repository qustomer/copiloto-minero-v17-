import pandas as pd

def get_territorial_weights(region):
    """
    Retorna la Matriz de Pesos Territoriales (MPT) según la región.
    Orden Heptágono: [Político, Social, Ambiental, Hídrico, Económico, Técnico, Comunicacional]
    """
    matrices = {
        "NOA":         [0.10, 0.15, 0.15, 0.30, 0.10, 0.10, 0.10], # Alarma Hídrica
        "Cuyo":        [0.10, 0.15, 0.30, 0.20, 0.10, 0.05, 0.10], # Alarma Ambiental extrema
        "Patagonia":   [0.10, 0.25, 0.20, 0.15, 0.10, 0.10, 0.10], # Alarma Social
        "Peru":        [0.25, 0.25, 0.15, 0.15, 0.10, 0.05, 0.05], # Alarma Político-Social
        "Chile_Centro":[0.10, 0.20, 0.20, 0.25, 0.10, 0.10, 0.05]  # Equilibrio
    }
    # Por defecto, matriz equilibrada (100% dividido en 7 ejes)
    return matrices.get(region, [0.142, 0.142, 0.143, 0.143, 0.143, 0.143, 0.144])

def calculate_icg(df_evidencia):
    """
    Índice de Certidumbre Global (ICG): Mide la robustez probatoria.
    Fórmula: ICG = min(100, Σ Qa)
    """
    suma_qa = df_evidencia['Qa'].sum() if 'Qa' in df_evidencia.columns else len(df_evidencia)
    return min(100.0, round(suma_qa, 2))

def calculate_friccion(df_evidencia):
    """
    Cálculo de Fricción Social: (Documentos negativos / total) * 100
    """
    if df_evidencia.empty:
        return 0.0
    
    total_docs = len(df_evidencia)
    docs_negativos = len(df_evidencia[df_evidencia['Sentimiento'] == 'Negativo'])
    
    friccion = (docs_negativos / total_docs) * 100
    return round(friccion, 2)

def calculate_ibh(df_evidencia, region):
    """
    Índice de Brechas Habilitantes (IBH).
    Fórmula por eje: score_eje = Σ(score * Qa) / Σ(Qa)
    Fórmula final: IBH = Σ(score_eje * peso_territorial)
    """
    ejes_oficiales = ["Político", "Social", "Ambiental", "Hídrico", "Económico", "Técnico", "Comunicacional"]
    pesos = get_territorial_weights(region)
    
    ibh_total = 0.0
    scores_por_eje = {}

    for i, eje in enumerate(ejes_oficiales):
        df_eje = df_evidencia[df_evidencia['Eje'] == eje]
        
        if not df_eje.empty and df_eje['Qa'].sum() > 0:
            # Cálculo ponderado por la Calidad de Artefacto (Qa)
            score_eje = (df_eje['Score_Crudo'] * df_eje['Qa']).sum() / df_eje['Qa'].sum()
        else:
            # Si no hay evidencia en ese eje, se asume un score neutro o base de 50
            score_eje = 50.0 
            
        scores_por_eje[eje] = round(score_eje, 2)
        ibh_total += score_eje * pesos[i]

    return round(ibh_total, 2), scores_por_eje

def calculate_survival_index(ibh, friccion, etapa):
    """
    Índice de Supervivencia del Proyecto (ISP) con Divisor Dinámico (Df).
    """
    if etapa == "Exploración":
        df = 250.0  # Menos sensibilidad al ruido
    elif etapa in ["Factibilidad", "Construcción"]:
        df = 120.0  # Alarma social máxima (alto capital en riesgo)
    else: 
        # Operación
        df = 180.0  # Equilibrio normativo (TSM)
        
    isp_decimal = (ibh / 100.0) - (friccion / df)
    isp_porcentaje = isp_decimal * 100
    
    # Asegura un piso de supervivencia del 5% y un techo del 100%
    isp_final = max(5.0, min(100.0, isp_porcentaje))
    return round(isp_final, 2)

def execute_full_scoring(df_evidencia, region, etapa):
    """
    Orquestador principal del motor de scoring pericial.
    Toma el dataframe de ingesta y devuelve todos los KPIs.
    """
    # 1. Calcular robustez documental
    icg = calculate_icg(df_evidencia)
    
    # 2. Calcular Fricción
    friccion = calculate_friccion(df_evidencia)
    
    # 3. Calcular IBH y obtener el detalle por ejes
    ibh, detalle_ejes = calculate_ibh(df_evidencia, region)
    
    # 4. Calcular Supervivencia (ISP)
    isp = calculate_survival_index(ibh, friccion, etapa)
    
    return {
        "ICG": icg,
        "Friccion": friccion,
        "IBH": ibh,
        "ISP": isp,
        "Detalle_Ejes": detalle_ejes
    }
