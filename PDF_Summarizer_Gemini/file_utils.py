import os
from typing import Optional

def ensure_directory_exists(directory_path: str) -> bool:
    """
    Garante que um diretório existe, criando-o se necessário.
    
    Args:
        directory_path: Caminho do diretório
        
    Returns:
        True se o diretório existe ou foi criado, False caso contrário
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório {directory_path}: {e}")
        return False

def get_file_size(file_path: str) -> Optional[int]:
    """
    Obtém o tamanho de um arquivo em bytes.
    
    Args:
        file_path: Caminho para o arquivo
        
    Returns:
        Tamanho do arquivo em bytes ou None se o arquivo não existir
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return None