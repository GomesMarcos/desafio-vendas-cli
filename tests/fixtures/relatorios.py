from pathlib import Path
from unittest.mock import MagicMock

import pytest

happy_path_params = [
    (
        [MagicMock()],
        "text",
        "Relatório de Vendas\nTotal em Vendas: R$998.90\nProduto Mais Vendido: Camiseta (R$49.90)\nQuantidade Vendida: 6\nData da venda: 01/01/2025\n",  # noqa: E501
    ),
    (
        [MagicMock(), MagicMock()],
        "json",
        '{\n    "total_vendas": "998.90",\n    "produto_mais_vendido": {\n        "nome": "Camiseta",\n        "preco": "R$49.9",\n        "quantidade": 6,\n        "data": "01/01/2025"\n    }\n}',  # noqa: E501
    ),
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
    """
    Fixture para criar um arquivo CSV temporário com dados de vendas.
    O arquivo é criado antes de cada teste e removido após o teste ser concluído.
    """
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
        # Para outros testes, criar o arquivo com
        # Dados de vendas (vários itens repetidos)
        dummy_path.write_text(
            "produto,quantidade,preco_unitario,data\n"
            "Camiseta,3,49.9,01/01/2025\n"
            "Calça,2,99.9,13/08/2025\n"
            "Camiseta,1,49.9,10/01/2025\n"
            "Tênis,1,199.9,01/08/2025\n"
            "Camiseta,2,49.9,15/01/2025\n"
            "Calça,1,99.9,20/08/2025\n"
            "Tênis,1,199.9,25/08/2025\n",
            encoding="utf-8",
        )
        yield
        if dummy_path.exists():
            dummy_path.unlink()
