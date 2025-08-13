import logging


def get_logger(name: str = "desafio-vendas-cli") -> logging.Logger:
    """Obtém um logger configurado.

    Args:
        name (str, optional): O nome do logger. Defaults to None.

    Returns:
        logging.Logger: O logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        __set_loggers_handlers(logger)
    return logger


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",  # Turquesa
        logging.INFO: "\033[32m",  # Verde
        logging.WARNING: "\033[33m",  # Amarelo
        logging.ERROR: "\033[31m",  # Vermelho
        logging.CRITICAL: "\033[41m",  # Fundo vermelho
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def __set_loggers_handlers(logger: logging.Logger) -> None:
    # Console handler com cores
    stream_handler = logging.StreamHandler()
    color_formatter = ColorFormatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler.setFormatter(color_formatter)
    logger.addHandler(stream_handler)

    # File handler (sem cores)
    file_handler = logging.FileHandler("logs", encoding="utf-8")
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


# Instância do logger
logger = get_logger()
