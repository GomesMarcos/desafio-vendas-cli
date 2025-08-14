"""
Comandos da ferramenta vendas-cli
"""

import argparse


def configurar_argumentos() -> argparse.ArgumentParser:
    """
    Configura os argumentos da linha de comando.

    Returns:
        argparse.ArgumentParser: O parser configurado.
    """
    parser = argparse.ArgumentParser(
        description="Processa arquivos de vendas e gera relatórios."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Caminho para o arquivo de entrada contendo os dados de vendas.",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Formato do relatório de saída (padrão: text).",
    )
    return parser


parser = configurar_argumentos()
