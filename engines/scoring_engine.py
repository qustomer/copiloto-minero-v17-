import numpy as np

AXES = [
    "Político",
    "Social",
    "Ambiental",
    "Hídrico",
    "Económico",
    "Técnico",
    "Comunicacional"
]

# ---------------------------------------------------
# PESOS TERRITORIALES (MPT)
# ---------------------------------------------------

WEIGHT_MATRIX = {
    "NOA_Litio":       [0.10,0.20,0.10,0.25,0.10,0.15,0.10],
    "Cuyo_Cobre":      [0.20,0.15,0.10,0.25,0.10,0.10,0.10],
    "Patagonia_Oro":   [0.15,0.20,0.20,0.10,0.10,0.10,0.15],
    "Centro_Otros":    [0.15,0.15,0.15,0.15,0.15,0.15,0.10],
}

# ---------------------------------------------------
# CALIDAD DE ARTEFACTOS (Qa)
# ---------------------------------------------------

WF = {"Oficial":1.0,"Auditor":0.8,"Corporativo":0.6,"Prensa":0.3}
DT = {"Tecnico":1.0,"Ejecutivo":0.6,"Nota":0.2}

def recency_factor(months):
    if months < 18: return 1.0
    if months < 36: return 0.7
    return 0.3

def artifact_quality(doc):
    return WF[doc["source"]] * recency_factor(doc["age"]) * DT[doc["density"]]

# ---------------------------------------------------
# FRICCIÓN
# ---------------------------------------------------

def calc_friction(axis_docs):
    total = len(axis_docs)
    if total == 0:
        return 0
    negatives = sum(1 for d in axis_docs if d["sentiment"] == "Contra")
    return (negatives/total) * 100

# ---------------------------------------------------
# SUPERVIVENCIA (ISP simplificado deploy)
# ---------------------------------------------------

def calc_survival(ibh, friction):
    base = ibh / 100
    penalty = friction / 200
    isp = max(0.05, base - penalty)
    return round(isp*100,2)

# ---------------------------------------------------
# PIPELINE PRINCIPAL
# ---------------------------------------------------

def run_scoring_pipeline(docs, region, mineral):

    key = f"{region}_{mineral}"
    weights = WEIGHT_MATRIX.get(key, WEIGHT_MATRIX["Centro_Otros"])

    axis_scores = {}
    frictions = {}
    total_quality = 0

    for axis in AXES:
        axis_docs = [d for d in docs if d["axis"] == axis]
        frictions[axis] = calc_friction(axis_docs)

        if not axis_docs:
            axis_scores[axis] = 0
            continue

        weighted = []
        qualities = []

        for d in axis_docs:
            qa = artifact_quality(d)
            score = np.random.uniform(40,80)
            weighted.append(score * qa)
            qualities.append(qa)

        axis_scores[axis] = sum(weighted) / sum(qualities)
        total_quality += sum(qualities)

    IBH = sum(axis_scores[a] * weights[i] for i,a in enumerate(AXES))
    ICG = min(100, total_quality)

    avg_friction = np.mean(list(frictions.values()))
    ISP = calc_survival(IBH, avg_friction)

    return {
        "axis_scores": axis_scores,
        "IBH": round(IBH,2),
        "ICG": round(ICG,2),
        "friction": round(avg_friction,2),
        "ISP": ISP
    }
