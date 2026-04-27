# engines/roi_engine.py
"""
ROI Engine
Calcula costo interno y margen esperado de la propuesta
"""

from typing import Dict, List

# Costos base internos por tipo de solución (USD)
INTERNAL_COSTS = {
    "Relacionamiento Comunitario": 12000,
    "Gestión Hídrica": 18000,
    "Monitoreo Ambiental": 15000,
    "Compliance Legal": 14000,
    "Comunicación Estratégica": 10000,
    "Gestión de Crisis": 20000,
    "Cierre de Mina": 22000,
}

def calculate_internal_cost(selected_solutions: List[str]) -> float:
    """Suma el costo interno estimado"""
    total_cost = 0
    for sol in selected_solutions:
        total_cost += INTERNAL_COSTS.get(sol, 12000)
    return total_cost


def calculate_roi(sale_price: float, internal_cost: float) -> Dict:
    """Calcula margen y ROI"""
    profit = sale_price - internal_cost
    margin = (profit / sale_price) * 100 if sale_price > 0 else 0

    return {
        "internal_cost_usd": round(internal_cost, 2),
        "profit_usd": round(profit, 2),
        "margin_percent": round(margin, 2),
    }
