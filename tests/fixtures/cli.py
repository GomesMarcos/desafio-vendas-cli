# Remova o decorator pytest.mark.parametrize e apenas defina os dados como variáveis para serem importados nos testes.

happy_cli_params = [
    (
        ["main.py", "dummy.csv", "--format", "text"],
        "output/relatorio_20240601.txt",
        "Relatório gerado em: output/relatorio_20240601.txt",
    ),
    (
        [
            "main.py",
            "dummy.csv",
            "--format",
            "json",
            "--start",
            "2024-01-01",
            "--end",
            "2024-12-31",
        ],
        "output/relatorio_20240601.json",
        "Relatório gerado em: output/relatorio_20240601.json",
    ),
    (
        ["main.py", "dummy.csv", "--format", "txt", "--start", "2024-01-01"],
        "output/relatorio_20240601.txt",
        "Relatório gerado em: output/relatorio_20240601.txt",
    ),
    (
        ["main.py", "dummy.csv", "--format", "txt", "--end", "2024-12-31"],
        "output/relatorio_20240601.txt",
        "Relatório gerado em: output/relatorio_20240601.txt",
    ),
]

happy_cli_ids = [
    "caminho-feliz-text-sem-datas",
    "caminho-feliz-json-com-datas",
    "borda-txt-apenas-inicio",
    "borda-txt-apenas-fim",
]
