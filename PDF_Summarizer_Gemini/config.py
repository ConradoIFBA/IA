import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da API Gemini - MODELOS ATUALIZADOS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Modelos disponíveis: gemini-1.0-pro, gemini-1.5-pro, gemini-1.5-flash
MODEL_NAME = "gemini-1.0-pro"  # Modelo mais estável e amplamente disponível
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1000))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))

# Configurações de processamento de PDF
MAX_PDF_PAGES = 50
CHUNK_SIZE = 4000  # Tamanho dos chunks de texto para processamento
CHUNK_OVERLAP = 200  # Sobreposição entre chunks

# Configurações de sumarização
SUMMARY_PROMPT = """
Por favor, produza um resumo conciso e informativo do texto abaixo.
O resumo deve capturar os pontos principais e as ideias mais importantes.
Se o texto for técnico, foque nos conceitos e conclusões fundamentais.

Mantenha o resumo em português e com no máximo {max_length} palavras.

Texto para resumir:
{text}
"""