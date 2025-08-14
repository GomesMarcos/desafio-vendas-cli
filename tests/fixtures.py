from pathlib import Path
from unittest.mock import MagicMock

import pytest

happy_path_params = [
    ([MagicMock()], "text", "relatorio_text"),
    ([MagicMock(), MagicMock()], "json", "relatorio_json"),
]
happy_path_ids = [
    "text-format-single-venda",
    "json-format-multiple-vendas",
]

# Parâmetros e ids para test_gerar_relatorio_no_vendas_raises_value_error
no_vendas_params: list[tuple[list | None, str]] = [
    ([], "Nenhuma venda encontrada."),
    (None, "Nenhuma venda encontrada."),
]
no_vendas_ids = [
    "no-vendas-empty-list",
    "no-vendas-none",
]

# Parâmetros e ids para test_gerar_relatorio_extrair_dados_raises_exception
exception_params = [
    (
        Exception("Arquivo dummy.csv não encontrado."),
        Exception,
        "Arquivo dummy.csv não encontrado.",
    ),
]
exception_ids = [
    "extrair-dados-raises-exception",
]


@pytest.fixture(scope="function", autouse=True)
def dummy_csv_file(request):
    # Arrange
    dummy_path = Path("dummy.csv")
    node_name = request.node.name.lower()
    if "extrair_dados_raises_exception" in node_name:
        # Forçando que o arquivo não exista para este teste
        if dummy_path.exists():
            dummy_path.unlink()
        yield
    elif "no_vendas_raises_value_error" in node_name:
        # Forçando que o arquivo exista mas não possua vendas para este teste
        dummy_path.write_text(
            "produto,quantidade,preco_unitario,data\n",
            encoding="utf-8",
        )
        yield
        if dummy_path.exists():
            dummy_path.unlink()
    else:
        # Para outros testes, criar o arquivo com dados de vendas
        dummy_path.write_text(
            "produto,quantidade,preco_unitario,data\nCamiseta,3,49.9,01/01/2025\n",
            encoding="utf-8",
        )
        yield
        if dummy_path.exists():
            dummy_path.unlink()
