import google.generativeai as genai
from typing import List, Optional
from config import GEMINI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE, SUMMARY_PROMPT
import time

# Configurar a API
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Erro ao configurar API Gemini: {e}")

def get_available_models() -> List[str]:
    """Lista todos os modelos disponíveis na API"""
    try:
        models = genai.list_models()
        return [model.name for model in models]
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
        return []

def check_model_availability(model_name: str) -> bool:
    """Verifica se um modelo específico está disponível"""
    available_models = get_available_models()
    return any(model_name in model for model in available_models)

def generate_summary(text: str, max_length: int = 300) -> str:
    """
    Gera um resumo para o texto fornecido usando a API do Gemini.
    
    Args:
        text: Texto a ser resumido
        max_length: Comprimento máximo aproximado do resumo em palavras
        
    Returns:
        Texto resumido
    """
    if not text or not text.strip():
        return "Nenhum texto válido para resumir."
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "sua_chave_api_aqui":
        return "Erro: API key não configurada. Por favor, defina GEMINI_API_KEY no arquivo .env"
    
    try:
        # Verificar se o modelo está disponível
        if not check_model_availability(MODEL_NAME):
            # Tentar modelos alternativos se o principal não estiver disponível
            alternative_models = ["gemini-1.0-pro", "gemini-1.5-flash", "gemini-pro"]
            for alt_model in alternative_models:
                if check_model_availability(alt_model):
                    actual_model = alt_model
                    break
            else:
                return "Erro: Nenhum modelo Gemini disponível. Verifique sua API key e acesso."
        else:
            actual_model = MODEL_NAME
        
        # Configurar o modelo
        generation_config = {
            "temperature": TEMPERATURE,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": MAX_TOKENS,
        }
        
        # Inicializar o modelo
        model = genai.GenerativeModel(
            model_name=actual_model,
            generation_config=generation_config
        )
        
        # Preparar o prompt
        prompt = SUMMARY_PROMPT.format(max_length=max_length, text=text[:10000])
        
        # Gerar o resumo
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"

def summarize_large_text(text: str, max_length: int = 300) -> str:
    """
    Resume textos longos dividindo-os em partes e resumindo cada parte.
    
    Args:
        text: Texto longo a ser resumido
        max_length: Comprimento máximo do resumo final em palavras
        
    Returns:
        Texto resumido
    """
    from pdf_processor import chunk_text
    
    # Se o texto for curto, resume diretamente
    if len(text) < 5000:
        return generate_summary(text, max_length)
    
    # Divide o texto em chunks
    chunks = chunk_text(text)
    summaries = []
    
    # Gera resumo para cada chunk
    for i, chunk in enumerate(chunks):
        print(f"Processando chunk {i+1}/{len(chunks)}")
        chunk_summary = generate_summary(chunk, max_length // len(chunks))
        if not chunk_summary.startswith("Erro"):
            summaries.append(chunk_summary)
        time.sleep(0.5)  # Pequena pausa para evitar rate limiting
    
    # Combina os resumos parciais
    combined_summary = " ".join(summaries)
    
    # Se ainda for muito longo, faz um resumo do resumo
    if len(combined_summary.split()) > max_length * 1.2:
        return generate_summary(combined_summary, max_length)
    
    return combined_summary

# Função para debug: listar modelos disponíveis
def debug_models():
    """Função para debug - lista modelos disponíveis"""
    print("Verificando modelos disponíveis...")
    models = get_available_models()
    print("Modelos disponíveis:")
    for model in models:
        print(f"  - {model}")
    
    # Testar o modelo configurado
    print(f"\nVerificando modelo configurado: {MODEL_NAME}")
    is_available = check_model_availability(MODEL_NAME)
    print(f"Modelo {MODEL_NAME} disponível: {is_available}")

if __name__ == "__main__":
    debug_models()