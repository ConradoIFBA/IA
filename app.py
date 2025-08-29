import os
import gradio as gr
from summarizer import summarize_pdf          # resumidor local
from PDF_Downloader import salvar_pdf         # gera o PDF do resumo


def process_pdf(pdf_path: str):
    if not pdf_path:
        return "**⚠️ Por favor, envie um PDF.**", None

    if not isinstance(pdf_path, (str, os.PathLike)):
        return "**❌ Entrada de arquivo inesperada.**", None

    ext = os.path.splitext(str(pdf_path))[1].lower()
    if ext != ".pdf":
        return "**❌ Tipo de arquivo inválido. Envie apenas .pdf**", None

    # Gerar o resumo
    resumo = summarize_pdf(str(pdf_path))
    if not resumo or resumo.startswith(("❌", "⚠️")):
        return f"**{resumo or '⚠️ Não foi possível gerar o resumo.'}**", None

    # 🔹 Nome do arquivo de saída = nome_original_resumo.pdf
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    out_name = f"{base_name}_resumo.pdf"

    pdf_file = salvar_pdf(resumo, nome_arquivo=out_name)
    return resumo, pdf_file


with gr.Blocks(theme=gr.themes.Soft(), title="PDF Summarizer (Local)") as demo:
    gr.Markdown("# 📄 Resumidor de PDF (Local)")

    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(
                file_types=[".pdf"],
                label="📂 Escolha seu arquivo PDF",
                type="filepath"  # retorna o caminho do arquivo como string
            )
            btn = gr.Button("✨ Resumir", variant="primary")

        with gr.Column(scale=2):
            resumo_output = gr.Markdown(label="📝 Resumo")
            pdf_download = gr.File(label="📥 Baixar Resumo em PDF")

    btn.click(
        fn=process_pdf,
        inputs=pdf_input,
        outputs=[resumo_output, pdf_download],
    )

if __name__ == "__main__":
    demo.launch(share=True)

