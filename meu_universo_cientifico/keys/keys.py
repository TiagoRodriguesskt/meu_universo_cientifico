import os
from pathlib import Path

from dotenv import load_dotenv  # type: ignore

# localiza a raiz a partir de /keys.py
raiz = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=raiz / ".env")

# Exporta a chave como uma constante de módulo
MINHA_CHAVE = os.getenv("MINHA_CHAVE_MESTRA")


def validar_conexao():
    """Verificar se a chave foi carregada corretamente"""
    return MINHA_CHAVE is not None
