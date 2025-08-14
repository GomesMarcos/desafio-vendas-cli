from contextlib import suppress
from datetime import datetime

from core.logger import logger


class DateHandler:
    """
    Classe para manipulação de datas, incluindo conversão entre string e datetime.date.
    Esta classe oferece métodos para converter strings de data em objetos datetime.date
    e vice-versa, suportando vários formatos comuns de data.
    """

    @staticmethod
    def str_to_date(date_str: str) -> datetime.date:
        """
        Tenta converter uma string para datetime.date usando vários formatos comuns.
        """
        formatos = [
            "%Y-%m-%d",
            "%y-%m-%d",
            "%d/%m/%Y",
            "%d/%m/%y",
            "%d-%m-%Y",
            "%d-%m-%y",
            "%Y/%m/%d",
            "%y/%m/%d",
            "%d.%m.%Y",
            "%d.%m.%y",
            "%Y.%m.%d",
            "%y.%m.%d",
        ]
        # Percorre os formatos e tenta converter, ignorando ValueError
        for formato in formatos:
            with suppress(ValueError):
                return datetime.strptime(date_str, formato).date()

        # Se nenhum formato funcionar, levanta ValueError
        mensagem = f"Formato de data desconhecido: {date_str}"
        logger.error(mensagem)
        raise ValueError(mensagem)

    @staticmethod
    def date_to_str(date: datetime) -> str:
        """Converte um objeto datetime.date para string no formato 'YYYY-MM-DD'."""
        return date.strftime("%Y-%m-%d")
