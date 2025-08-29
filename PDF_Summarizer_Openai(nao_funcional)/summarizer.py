from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

def summarize_pdf(file_path: str) -> str:
    try:
        # Ler o PDF
        pdf = PdfReader(file_path)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

        if not text.strip():
            return "⚠️ O PDF está vazio ou não pôde ser lido."

        # Dividir o texto em partes menores
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        texts = splitter.split_text(text)
        docs = [Document(page_content=t) for t in texts]

        # Criar LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # Carregar chain de sumarização
        chain = load_summarize_chain(llm, chain_type="map_reduce")

        # Gerar resumo
        summary = chain.run(docs)

        return summary.strip()

    except Exception as e:
        return f"⚠️ Erro ao processar o PDF: {str(e)}"
