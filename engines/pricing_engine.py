def calculate_price(ibh, friccion, isp):
    # Tu lógica de cálculo aquí...
    base_fee = 15000 
    # (El resto de tu código de pricing)
    return total_final
# Copiloto Minero v17 — Risk Adjusted Pricing Engine

from engines.fx_engine import get_fx_rate


# ---------------------------------------------------
# 1. Tiers base de servicios (USD)
# ---------------------------------------------------

BASE_TIERS = {
    "Starter": 25000,
    "Growth": 45000,
    "Advanced": 75000,
    "Crisis": 110000
}


def select_tier(ibh: float) -> str:
    """
    Selecciona tier base según IBH.
    """
    if ibh >= 75:
        return "Starter"
    elif ibh >= 60:
        return "Growth"
    elif ibh >= 45:
        return "Advanced"
    else:
        return "Crisis"


# ---------------------------------------------------
# 2. Multiplicador por Fricción
# ---------------------------------------------------

def friction_multiplier(friction_dict: dict) -> float:
    """
    Aplica multiplicador si hay fricción en ejes críticos.
    """
    critical_axes = ["Social", "Hídrico", "Territorial"]

    max_friction = max([friction_dict.get(ax, 0) for ax in critical_axes])

    if max_friction > 60:
        return 1.35
    elif max_friction > 40:
        return 1.20
    elif max_friction > 20:
        return 1.10
    else:
        return 1.0


# ---------------------------------------------------
# 3. Multiplicador por supervivencia (ISP)
# ---------------------------------------------------

def survival_multiplier(isp: float) -> float:
    """
    A menor supervivencia → mayor fee de mitigación.
    ISP = probabilidad de sobrevivir a siguiente fase.
    """
    if isp >= 80:
        return 1.0
    elif isp >= 60:
        return 1.10
    elif isp >= 40:
        return 1.25
    else:
        return 1.45


# ---------------------------------------------------
# 4. Fee Fortalecimiento Base Evidencial (FBE)
# ---------------------------------------------------

def fbe_fee(icg: float) -> float:
    """
    Si la certeza es baja → se vende relevamiento.
    """
    if icg >= 50:
        return 0
    else:
        return 15000  # USD


# ---------------------------------------------------
# 5. Pricing principal
# ---------------------------------------------------

def calculate_project_pricing(
    ibh: float,
    isp: float,
    icg: float,
    friction: dict,
    currency: str = "USD"
) -> dict:

    tier = select_tier(ibh)
    base_price = BASE_TIERS[tier]

    mult_friction = friction_multiplier(friction)
    mult_survival = survival_multiplier(isp)
    fee_fbe = fbe_fee(icg)

    risk_adjusted_price_usd = base_price * mult_friction * mult_survival
    final_price_usd = risk_adjusted_price_usd + fee_fbe

    fx_rate = get_fx_rate(currency)
    final_price_local = final_price_usd * fx_rate

    return {
        "tier": tier,
        "base_price_usd": base_price,
        "mult_friction": mult_friction,
        "mult_survival": mult_survival,
        "fbe_fee_usd": fee_fbe,
        "final_price_usd": round(final_price_usd, 2),
        "final_price_local": round(final_price_local, 2),
        "currency": currency
    }
