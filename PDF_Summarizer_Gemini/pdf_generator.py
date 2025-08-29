import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from config import MODEL_NAME
import re

def sanitize_filename(filename):
    """
    Remove caracteres inválidos para nomes de arquivo.
    
    Args:
        filename: Nome original do arquivo
        
    Returns:
        Nome do arquivo sanitizado
    """
    # Remove a extensão .pdf se existir
    if filename.lower().endswith('.pdf'):
        filename = filename[:-4]
    
    # Remove caracteres inválidos
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove espaços excessivos e trim
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    # Limita o tamanho do nome (evita problemas com paths longos)
    if len(filename) > 100:
        filename = filename[:100] + '...'
    
    return filename

def get_unique_filename(directory, base_filename):
    """
    Gera um nome de arquivo único para evitar sobrescrita.
    
    Args:
        directory: Diretório onde o arquivo será salvo
        base_filename: Nome base do arquivo
        
    Returns:
        Nome de arquivo único
    """
    counter = 1
    filename = base_filename
    full_path = os.path.join(directory, filename)
    
    # Se o arquivo já existe, adiciona um número
    while os.path.exists(full_path):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        full_path = os.path.join(directory, filename)
        counter += 1
    
    return filename

def criar_pdf_resumo(texto_original: str, resumo: str, original_filename: str, titulo: str = None) -> str:
    """
    Cria um arquivo PDF com o resumo usando o nome original do arquivo.
    
    Args:
        texto_original: Texto completo extraído do PDF
        resumo: Texto do resumo gerado
        original_filename: Nome original do arquivo PDF
        titulo: Título personalizado (opcional)
        
    Returns:
        Caminho completo para o PDF gerado
    """
    # Criar diretório de downloads se não existir
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    
    # Sanitizar o nome do arquivo original
    safe_filename = sanitize_filename(original_filename)
    
    # Criar nome do arquivo final (SEM TIMESTAMP)
    base_filename = f"{safe_filename}_resumo.pdf"
    filename = get_unique_filename(downloads_dir, base_filename)
    full_path = os.path.join(downloads_dir, filename)
    
    # Usar título personalizado ou padrão
    if titulo is None:
        titulo = f"Resumo: {safe_filename}"
    
    # Criar documento PDF
    doc = SimpleDocTemplate(full_path, pagesize=A4, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)
    
    # Estilos
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Heading1']
    estilo_subtitulo = styles['Heading2']
    estilo_normal = styles['BodyText']
    estilo_italico = ParagraphStyle(
        'Italico',
        parent=styles['BodyText'],
        fontName='Helvetica-Oblique',
        textColor=colors.grey
    )
    
    # Conteúdo do PDF
    conteudo = []
    
    # Título
    conteudo.append(Paragraph(titulo, estilo_titulo))
    conteudo.append(Spacer(1, 0.2 * inch))
    
    # Informações do processamento
    conteudo.append(Paragraph("Informações do Processamento", estilo_subtitulo))
    conteudo.append(Paragraph(f"<b>Arquivo original:</b> {original_filename}", estilo_normal))
    conteudo.append(Paragraph(f"<b>Data de geração:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilo_normal))
    conteudo.append(Paragraph(f"<b>Modelo utilizado:</b> {MODEL_NAME}", estilo_normal))
    conteudo.append(Paragraph(f"<b>Tamanho do texto original:</b> {len(texto_original):,} caracteres".replace(',', '.'), estilo_normal))
    conteudo.append(Paragraph(f"<b>Tamanho do resumo:</b> {len(resumo):,} caracteres".replace(',', '.'), estilo_normal))
    
    # Calcular taxa de compressão
    if len(texto_original) > 0:
        taxa_compressao = ((len(texto_original) - len(resumo)) / len(texto_original) * 100)
        conteudo.append(Paragraph(f"<b>Taxa de compressão:</b> {taxa_compressao:.1f}%", estilo_normal))
    
    conteudo.append(Spacer(1, 0.3 * inch))
    
    # Resumo
    conteudo.append(Paragraph("Resumo Gerado", estilo_subtitulo))
    conteudo.append(Spacer(1, 0.1 * inch))
    
    # Adicionar o resumo como parágrafos
    for paragrafo in resumo.split('\n'):
        if paragrafo.strip():
            conteudo.append(Paragraph(paragrafo.strip(), estilo_normal))
            conteudo.append(Spacer(1, 0.05 * inch))
    
    conteudo.append(Spacer(1, 0.3 * inch))
    
    # Rodapé
    rodape = Paragraph(
        f"<i>Resumo gerado automaticamente por sistema de IA em {datetime.now().strftime('%d/%m/%Y')}. "
        "Este é um resumo automatizado e deve ser revisado para precisão completa.</i>",
        estilo_italico
    )
    conteudo.append(rodape)
    
    # Construir PDF
    doc.build(conteudo)
    
    return full_path

def criar_pdf_simples(texto: str, original_filename: str, titulo: str = None) -> str:
    """
    Cria um PDF simples com o nome original do arquivo.
    
    Args:
        texto: Texto do resumo
        original_filename: Nome original do arquivo PDF
        titulo: Título personalizado (opcional)
        
    Returns:
        Caminho completo para o PDF gerado
    """
    # Criar diretório de downloads se não existir
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    
    # Sanitizar o nome do arquivo
    safe_filename = sanitize_filename(original_filename)
    
    # Criar nome do arquivo final (SEM TIMESTAMP)
    base_filename = f"{safe_filename}_resumo.pdf"
    filename = get_unique_filename(downloads_dir, base_filename)
    full_path = os.path.join(downloads_dir, filename)
    
    # Usar título personalizado ou padrão
    if titulo is None:
        titulo = f"Resumo: {safe_filename}"
    
    # Criar documento PDF simples
    c = canvas.Canvas(full_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, titulo)
    c.setFont("Helvetica", 12)
    
    y = 730
    lines = texto.split('\n')
    
    for line in lines:
        if line.strip():
            # Quebra de linha se o texto for muito longo
            if len(line) > 80:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) > 80:
                        c.drawString(50, y, current_line)
                        y -= 20
                        current_line = word
                        if y < 50:
                            c.showPage()
                            y = 750
                            c.setFont("Helvetica", 12)
                    else:
                        current_line += " " + word if current_line else word
                if current_line:
                    c.drawString(50, y, current_line)
                    y -= 20
            else:
                c.drawString(50, y, line)
                y -= 20
            
            if y < 50:
                c.showPage()
                y = 750
                c.setFont("Helvetica", 12)
    
    # Rodapé
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 30, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Modelo: {MODEL_NAME} - Arquivo original: {original_filename}")
    
    c.save()
    return full_path

# Função de limpeza mantida
def limpar_downloads_antigos(dias=7):
    """Remove arquivos PDF com mais de X dias"""
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        return
    
    agora = datetime.now()
    for arquivo in os.listdir(downloads_dir):
        if arquivo.endswith('.pdf'):
            caminho_arquivo = os.path.join(downloads_dir, arquivo)
            tempo_criacao = datetime.fromtimestamp(os.path.getctime(caminho_arquivo))
            dias_diferenca = (agora - tempo_criacao).days
            
            if dias_diferenca > dias:
                os.remove(caminho_arquivo)