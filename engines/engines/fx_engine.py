# engines/fx_engine.py
# FX Engine v1 — Baseline Abril 2026

BASE_RATES = {
    "USD": 1.0,
    "ARS": 1400.0,   # Baseline oficial fijado
    "CLP": 950.0,
    "PEN": 3.8,
    "MXN": 17.5,
    "COP": 4200.0
}

def get_fx_rate(currency: str) -> float:
    """
    Devuelve tasa FX contra USD.
    3 capas:
    1) Base (hardcoded baseline)
    2) Futuro: API externa
    3) Emergencia fallback USD
    """
    currency = currency.upper()

    if currency in BASE_RATES:
        return BASE_RATES[currency]

    # Fallback de emergencia
    return 1.0


def convert_from_usd(amount_usd: float, target_currency: str) -> float:
    rate = get_fx_rate(target_currency)
    return round(amount_usd * rate, 2)
