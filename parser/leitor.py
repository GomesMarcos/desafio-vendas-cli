from csv import DictReader
from pathlib import Path
from typing import Dict, List

from core.logger import logger


def extrair_dados(file_path: Path) -> List[Dict]:
    """Lê um arquivo CSV e retorna seu conteúdo como uma lista de dicionários."""
    if not file_path.exists():
        mensagem = f"Arquivo {file_path} não encontrado."
        logger.error(mensagem)
        raise FileNotFoundError(mensagem)

    with file_path.open("r", encoding="utf-8") as file:
        reader = DictReader(file)
        return list(reader)
