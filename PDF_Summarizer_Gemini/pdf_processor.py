import PyPDF2
import io
from typing import List, Tuple

def extract_text_from_pdf(pdf_file) -> Tuple[str, int]:
    """
    Extrai texto de um arquivo PDF carregado via Gradio ou caminho de arquivo.
    
    Args:
        pdf_file: Arquivo PDF ou caminho para o arquivo
        
    Returns:
        Tuple contendo o texto extraído e o número de páginas
    """
    text = ""
    num_pages = 0
    
    try:
        if hasattr(pdf_file, 'read'):  # Se é um arquivo carregado
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        else:  # Se é um caminho de arquivo
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
        num_pages = len(pdf_reader.pages)
        
        for page_num in range(min(num_pages, 50)):  # Limite de páginas
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
            
    except Exception as e:
        raise Exception(f"Erro ao processar PDF: {str(e)}")
    
    return text, num_pages

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """
    Divide o texto em chunks menores para processamento.
    
    Args:
        text: Texto completo a ser dividido
        chunk_size: Tamanho máximo de cada chunk
        overlap: Sobreposição entre chunks para manter contexto
        
    Returns:
        Lista de chunks de texto
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        # Garantir que não quebramos no meio de uma palavra
        if end < len(text):
            while end > start and text[end] not in (' ', '\n', '.', ',', ';', ':'):
                end -= 1
            if end == start:  # Fallback se não encontrar caractere de quebra
                end = start + chunk_size
                
        chunks.append(text[start:end])
        start = end - overlap  # Adiciona sobreposição
        
    return chunks