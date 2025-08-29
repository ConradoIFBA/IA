import gradio as gr
from summarizer import generate_summary, summarize_large_text
from pdf_processor import extract_text_from_pdf
from pdf_generator import criar_pdf_resumo, criar_pdf_simples, limpar_downloads_antigos
import time
import os

def process_pdf_summary(pdf_file, summary_length, detailed_summary, pdf_type):
    """
    Processa um arquivo PDF e gera um resumo com nome personalizado.
    """
    if pdf_file is None:
        return "Por favor, faça upload de um arquivo PDF.", "", None
    
    try:
        # Obter nome original do arquivo
        original_filename = os.path.basename(pdf_file.name)
        
        # Converter comprimento da escala 1-5 para palavras aproximadas
        length_map = {1: 150, 2: 250, 3: 350, 4: 500, 5: 700}
        max_length = length_map.get(summary_length, 300)
        
        # Extrair texto do PDF
        with open(pdf_file.name, "rb") as f:
            text, num_pages = extract_text_from_pdf(f)
        
        if not text.strip():
            return "Não foi possível extrair texto do PDF. O arquivo pode ser digitalizado (imagem).", "", None
        
        # Gerar resumo
        start_time = time.time()
        
        if detailed_summary and len(text) > 5000:
            summary = summarize_large_text(text, max_length)
        else:
            summary = generate_summary(text, max_length)
        
        processing_time = time.time() - start_time
        
        # Estatísticas
        stats = f"""
        **Estatísticas do processamento:**
        - Arquivo original: {original_filename}
        - Páginas processadas: {num_pages}
        - Caracteres extraídos: {len(text):,}
        - Caracteres no resumo: {len(summary):,}
        - Tempo de processamento: {processing_time:.2f} segundos
        """
        
        # Criar PDF do resumo com nome personalizado
        if pdf_type == "completo":
            pdf_path = criar_pdf_resumo(text, summary, original_filename, f"Resumo do Documento: {original_filename}")
        else:
            pdf_path = criar_pdf_simples(summary, original_filename, f"Resumo: {original_filename}")
        
        # Nome amigável para download (sem o caminho completo)
        download_filename = os.path.basename(pdf_path)
        
        return summary, stats, pdf_path
        
    except Exception as e:
        return f"Erro ao processar o PDF: {str(e)}", "", None

# Limpar downloads antigos ao iniciar
limpar_downloads_antigos()

# Interface Gradio
with gr.Blocks(title="Resumidor de PDF com Gemini API", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 Resumidor de PDF com Gemini API")
    gr.Markdown("Faça upload de um arquivo PDF para gerar um resumo usando IA e baixe o resultado em PDF.")
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="Upload do PDF", file_types=[".pdf"])
            length_slider = gr.Slider(1, 5, value=3, step=1, 
                                     label="Comprimento do Resumo", 
                                     info="1 (mais curto) - 5 (mais longo)")
            detailed = gr.Checkbox(label="Resumo detalhado (para documentos longos)", value=False)
            pdf_type = gr.Radio(
                choices=["completo", "simples"],
                value="completo",
                label="Tipo de PDF",
                info="Completo: inclui metadados e estatísticas. Simples: apenas o resumo."
            )
            process_btn = gr.Button("Gerar Resumo e PDF", variant="primary")
        
        with gr.Column():
            summary_output = gr.Textbox(label="Resumo", lines=12, interactive=False)
            stats_output = gr.Markdown()
            pdf_output = gr.File(label="Download do PDF", interactive=False)
    
    # Event handlers
    process_btn.click(
        fn=process_pdf_summary,
        inputs=[pdf_input, length_slider, detailed, pdf_type],
        outputs=[summary_output, stats_output, pdf_output]
    )

if __name__ == "__main__":
    demo.launch(share=True)