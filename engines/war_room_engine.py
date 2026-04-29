def apply_solutions_and_recalculate(results, selected_solutions, region, mineral, phase):
    """
    Simula la mitigación de riesgos basada en soluciones seleccionadas.
    """
    new_ibh = results["IBH"]
    new_friccion = results["Friccion"]
    
    # Cada solución reduce un 5% la fricción y mejora un 3% el IBH
    for sol in selected_solutions:
        new_friccion = max(0, new_friccion - 5)
        new_ibh = min(100, new_ibh + 3)
        
    # Recalcular ISP proyectado (Supervivencia)
    new_isp = (new_ibh + (100 - new_friccion)) / 2
    
    return {
        "IBH": new_ibh,
        "Friccion": new_friccion,
        "ISP": new_isp,
        "ICG": results["ICG"]
    }
