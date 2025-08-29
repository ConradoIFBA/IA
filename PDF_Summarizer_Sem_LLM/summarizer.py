from pypdf import PdfReader

def extrair_texto_pdf(pdf_path):
    """Extrai texto de um PDF e já normaliza a formatação."""
    texto = ""
    leitor = PdfReader(pdf_path)
    for pagina in leitor.pages:
        texto += pagina.extract_text() + "\n"

    # Normaliza: remove múltiplos espaços e quebras de linha desnecessárias
    texto = " ".join(texto.split())
    return texto

def resumir_texto(texto, max_sentencas=5):
    """Resumo simples: pega as primeiras frases do texto normalizado."""
    frases = texto.split(". ")
    resumo = ". ".join(frases[:max_sentencas])
    return resumo + "."

def summarize_pdf(pdf_path):
    """Pipeline completo: extrai e resume o PDF."""
    texto = extrair_texto_pdf(pdf_path)
    if not texto.strip():
        return "⚠️ Não foi possível extrair texto do PDF."
    resumo = resumir_texto(texto)
    return resumo
