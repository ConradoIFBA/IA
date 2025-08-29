from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def salvar_pdf(texto: str, nome_arquivo: str = "resumo.pdf") -> str:
    """Gera um PDF com quebras automáticas e margens decentes."""
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    styles = getSampleStyleSheet()
    normal = styles["BodyText"]
    normal.fontName = "Helvetica"
    normal.fontSize = 11
    normal.leading = 15

    # Preserva parágrafos (duas quebras = novo parágrafo)
    story = []
    texto = (texto or "").strip()
    for para in texto.split("\n\n"):
        para = para.strip().replace("\n", "<br/>")
        if not para:
            continue
        story.append(Paragraph(para, normal))
        story.append(Spacer(1, 8))

    doc.build(story)
    return nome_arquivo
