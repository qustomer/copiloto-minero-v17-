import hashlib
from datetime import datetime
import pandas as pd

# ==============================
# HASHING PARA DETECTAR DUPLICADOS
# ==============================

def generate_file_hash(file_bytes):
    """Genera huella digital del archivo"""
    return hashlib.sha256(file_bytes).hexdigest()


# ==============================
# CALIDAD DEL ARTEFACTO (Qa)
# ==============================

def calculate_artifact_quality(source_type, date, doc_type):
    """
    Qa = Wf * Fr * Dt
    """

    # Peso por tipo de fuente (Wf)
    wf_map = {
        "Oficial": 1.0,
        "Terceros": 0.8,
        "Corporativo": 0.6,
        "Prensa": 0.3,
    }

    # Densidad técnica (Dt)
    dt_map = {
        "Estudio Técnico": 1.0,
        "Resumen Ejecutivo": 0.6,
        "Nota periodística": 0.2,
    }

    wf = wf_map.get(source_type, 0.3)
    dt = dt_map.get(doc_type, 0.2)

    # Recencia (Fr)
    months_old = (datetime.now() - date).days / 30

    if months_old < 18:
        fr = 1.0
    elif months_old < 36:
        fr = 0.7
    else:
        fr = 0.3

    return wf * fr * dt


# ==============================
# INGESTA PRINCIPAL
# ==============================

def run_ingestion_pipeline(files_metadata):
    """
    Procesa documentos cargados y devuelve dataset limpio
    """

    if len(files_metadata) == 0:
        return pd.DataFrame(), []

    unique_hashes = set()
    cleaned_docs = []
    duplicates = []

    for doc in files_metadata:
        file_hash = doc["hash"]

        # Filtro Anti-Eco Nivel 1
        if file_hash in unique_hashes:
            duplicates.append(doc["name"])
            continue

        unique_hashes.add(file_hash)

        qa = calculate_artifact_quality(
            doc["source_type"],
            doc["date"],
            doc["doc_type"]
        )

        cleaned_docs.append({
            "name": doc["name"],
            "axis": doc["axis"],
            "sentiment": doc["sentiment"],
            "Qa": qa,
            "source_type": doc["source_type"]
        })

    df = pd.DataFrame(cleaned_docs)

    return df, duplicates
