import gradio as gr
from dotenv import load_dotenv
import os
from summarizer import summarize_pdf

# 🔹 Carregar variáveis de ambiente
load_dotenv()

# 🔹 Validar se a chave está correta
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or not api_key.startswith("sk-"):
    raise ValueError(
        "⚠️ ERRO: A chave da OpenAI não foi encontrada ou está inválida.\n"
        "Verifique seu arquivo `.env` e confirme que ele contém:\n"
        "OPENAI_API_KEY=sk-sua_chave_aqui"
    )

# Função para rodar no Gradio
def process_pdf(file):
    try:
        return summarize_pdf(file.name)
    except Exception as e:
        return f"⚠️ Ocorreu um erro ao processar o PDF: {str(e)}"

# Interface Gradio
iface = gr.Interface(
    fn=process_pdf,
    inputs=gr.File(label="Envie seu PDF", type="filepath"),
    outputs="text",
    title="📄 Resumidor de PDF com LangChain + OpenAI",
    description="Envie um PDF em português e obtenha um resumo gerado por IA."
)

if __name__ == "__main__":
    iface.launch()
