import argparse

from parser.relatorios import Relatorio


def main():
    parser = argparse.ArgumentParser(
        description="Gera relatório de vendas a partir de um arquivo CSV."
    )
    parser.add_argument(
        "caminho_arquivo", type=str, help="Caminho para o arquivo CSV de vendas."
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default="text",
        choices=["text", "txt", "json"],
        help="Formato do relatório (text/txt/json).",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="",
        help="Data inicial para filtrar vendas (opcional).",
    )
    parser.add_argument(
        "--end", type=str, default="", help="Data final para filtrar vendas (opcional)."
    )
    args = parser.parse_args()

    relatorio = Relatorio(
        caminho_arquivo=args.caminho_arquivo,
        formato=args.format,
        data_inicial=args.start,
        data_final=args.end,
    )
    caminho_relatorio = relatorio.gerar_relatorio()
    print(f"Relatório gerado em: {caminho_relatorio}")


if __name__ == "__main__":
    main()
