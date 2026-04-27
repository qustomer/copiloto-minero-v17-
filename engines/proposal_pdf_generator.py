import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------------------------------------------------
# Utilidad: generar hash de integridad del proyecto
# ---------------------------------------------------

def generate_project_hash(data: dict) -> str:
    serialized = str(data).encode()
    return hashlib.sha256(serialized).hexdigest()


# ---------------------------------------------------
# PDF 1 — REPORTE COMERCIAL (Bilingüe Cliente)
# ---------------------------------------------------

def generate_commercial_report(results, pricing, solutions, file_path="Executive_Report.pdf"):

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("EXECUTIVE COMMERCIAL REPORT", styles['Title']))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Índice de Bienestar Heptagonal (IBH):</b> %.2f" % results["IBH"], styles['Normal']))
    story.append(Paragraph("<b>Índice de Supervivencia del Proyecto (ISP):</b> %.2f%%" % results["ISP"], styles['Normal']))
    story.append(Paragraph("<b>Índice de Certeza Global (ICG):</b> %.2f%%" % results["ICG"], styles['Normal']))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Investment Overview</b>", styles['Heading2']))
    story.append(Paragraph(f"Total Fee USD: {pricing['total_fee_usd']}", styles['Normal']))
    story.append(Paragraph(f"Total Fee Local Currency: {pricing['total_fee_local']}", styles['Normal']))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Selected Strategic Solutions</b>", styles['Heading2']))
    for sol in solutions:
        story.append(Paragraph(f"• {sol}", styles['Normal']))

    story.append(Spacer(1,24))
    story.append(Paragraph("This proposal is based on forensic data analysis and risk modelling.", styles['Italic']))

    project_hash = generate_project_hash(results)
    story.append(Spacer(1,24))
    story.append(Paragraph(f"Integrity Hash: {project_hash}", styles['Normal']))

    doc.build(story)


# ---------------------------------------------------
# PDF 2 — REPORTE TÉCNICO INTERNO (Director)
# ---------------------------------------------------

def generate_technical_report(results, pricing, evidence_summary, file_path="Technical_Report.pdf"):

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("TECHNICAL AUDIT REPORT", styles['Title']))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Evidence Summary</b>", styles['Heading2']))
    story.append(Paragraph(f"Total Unique Sources: {evidence_summary['total_sources']}", styles['Normal']))
    story.append(Paragraph(f"ICG: {results['ICG']}%", styles['Normal']))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Risk Metrics</b>", styles['Heading2']))
    story.append(Paragraph(f"IBH: {results['IBH']}", styles['Normal']))
    story.append(Paragraph(f"ISP: {results['ISP']}%", styles['Normal']))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Financial Breakdown</b>", styles['Heading2']))
    story.append(Paragraph(f"Consulting Core (70%): {pricing['consulting_core']}", styles['Normal']))
    story.append(Paragraph(f"Local Deployment (30%): {pricing['local_deployment']}", styles['Normal']))

    project_hash = generate_project_hash(results)
    story.append(Spacer(1,24))
    story.append(Paragraph(f"Integrity Hash: {project_hash}", styles['Normal']))

    doc.build(story)


# ---------------------------------------------------
# Orquestador de reportes duales
# ---------------------------------------------------

def generate_dual_reports(results, pricing, solutions, evidence_summary):

    if results["ICG"] < 50:
        # modo FBE — solo reporte técnico
        generate_technical_report(results, pricing, evidence_summary)
        return "FBE_report_generated"

    generate_commercial_report(results, pricing, solutions)
    generate_technical_report(results, pricing, evidence_summary)

    return "dual_reports_generated"
