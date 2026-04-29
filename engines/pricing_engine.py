def calculate_price(ibh, friccion, isp):
    """
    Motor de Pricing V17 - Ajustado por Riesgo y Probabilidad de Supervivencia (ISP).
    """
    # 1. Base de Honorarios según complejidad técnica (USD)
    base_fee = 15000 
    
    # 2. Factor de Riesgo (A mayor fricción y menor IBH, mayor el esfuerzo de consultoría)
    # Si el IBH es bajo (ej. 40) y la Fricción es alta (ej. 70), el factor aumenta.
    risk_multiplier = ( (100 - ibh) + friccion + (100 - isp) ) / 100
    
    # 3. Cálculo Final
    # Aseguramos un mínimo del fee base y aplicamos el multiplicador de riesgo
    total_final = base_fee * (1 + risk_multiplier)
    
    return round(total_final, 0)

# Copiloto Minero v17 - Risk Adjusted Pricing Engine
