from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from parser.modelos import Produto, Venda
from parser.relatorios import Relatorio
from tests.fixtures.relatorios import (
    dummy_csv_file,  # noqa: F401
    exception_ids,
    exception_params,
    happy_path_ids,
    happy_path_params,
    no_vendas_ids,
    no_vendas_params,
)


@pytest.mark.parametrize(
    "vendas, formato, expected_output",
    happy_path_params,
    ids=happy_path_ids,
)
def test_gerar_relatorio_happy_path(vendas, formato, expected_output, dummy_csv_file):
    # Arrange

    relatorio = Relatorio("dummy.csv", formato)

    # Act
    result = relatorio.gerar_relatorio()

    # Assert
    match formato:
        case "text" | "txt":
            assert str(result).endswith(".txt")
        case "json":
            assert str(result).endswith(".json")

    assert str(result).startswith("output/relatorio_")
    # Verifica que o arquivo de saída foi criado
    assert result.exists()

    with open(result, "r", encoding="utf-8") as file:
        content = file.read()
        assert expected_output == content

    result.unlink()  # Remove o arquivo após o teste


@pytest.mark.parametrize(
    "vendas, expected_message",
    no_vendas_params,
    ids=no_vendas_ids,
)
def test_gerar_relatorio_no_vendas_raises_value_error(
    vendas, expected_message, dummy_csv_file
):
    # Arrange

    relatorio = Relatorio("dummy.csv", "text")

    # Act / Assert
    with patch("core.logger.logger") as mock_logger:
        with pytest.raises(ValueError) as excinfo:
            relatorio.gerar_relatorio()
        assert str(excinfo.value) == expected_message


@pytest.mark.parametrize(
    "side_effect, expected_exception, expected_message",
    exception_params,
    ids=exception_ids,
)
def test_gerar_relatorio_extrair_dados_raises_exception(
    side_effect, expected_exception, expected_message, dummy_csv_file
):
    # Arrange

    relatorio = Relatorio("dummy.csv", "text")
    relatorio.__extrair_dados_de_vendas = MagicMock(side_effect=side_effect)

    # Act / Assert
    with pytest.raises(expected_exception) as excinfo:
        relatorio.gerar_relatorio()
    assert expected_message in str(excinfo.value)


def test_validar_formato_raises_value_error():
    # Arrange / Act
    with pytest.raises(ValueError) as excinfo:
        Relatorio("dummy.csv", "xml")
    # Assert
    assert "Formato de relatório desconhecido" in str(excinfo.value)


def test_obter_relatorio_conforme_formato_text(monkeypatch, dummy_csv_file):
    # Arrange
    relatorio = Relatorio("dummy.csv", "text")
    relatorio.vendas = [
        Venda(
            produto=Produto(nome="Camiseta", preco=Decimal("49.90")),
            quantidade=2,
            data_str="2025-01-01",
        )
    ]
    relatorio.base_caminho_relatorio = Path("output/test_relatorio")
    monkeypatch.setattr(
        "helpers.date_handler.DateHandler.obter_data_e_hora_para_salvar_relatorio",
        lambda: "2025-01-01_00-00-00",
    )
    # Act
    result = relatorio._Relatorio__obter_relatorio_conforme_formato()
    # Assert
    assert result.exists()
    with open(result, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Relatório de Vendas" in content
    result.unlink()


def test_obter_relatorio_conforme_formato_json(monkeypatch, dummy_csv_file):
    # Arrange
    relatorio = Relatorio("dummy.csv", "json")
    relatorio.vendas = [
        Venda(
            produto=Produto(nome="Camiseta", preco=Decimal("49.90")),
            quantidade=2,
            data_str="2025-01-01",
        )
    ]
    relatorio.base_caminho_relatorio = Path("output/test_relatorio")
    monkeypatch.setattr(
        "helpers.date_handler.DateHandler.obter_data_e_hora_para_salvar_relatorio",
        lambda: "2025-01-01_00-00-00",
    )
    # Act
    result = relatorio._Relatorio__obter_relatorio_conforme_formato()
    # Assert
    assert result.exists()
    with open(result, "r", encoding="utf-8") as f:
        content = f.read()
        assert "total_vendas" in content
    result.unlink()


def test_extrair_dados_de_vendas_file_not_found():
    # Arrange
    relatorio = Relatorio("arquivo_inexistente.csv", "text")
    # Act / Assert
    with pytest.raises(FileNotFoundError):
        relatorio._Relatorio__extrair_dados_de_vendas()


def test_obter_venda_data_nao_informada():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text")
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act / Assert
    with pytest.raises(ValueError):
        relatorio._Relatorio__obter_venda(linha, produto)


def test_obter_venda_intervalo_datas_valido(monkeypatch):
    # Arrange
    relatorio = Relatorio(
        "dummy.csv", "text", data_inicial="2025-01-01", data_final="2025-01-31"
    )
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-01-15",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is not None
    assert venda.quantidade == 2
    assert venda.produto.nome == "Camiseta"


def test_obter_venda_intervalo_datas_fora(monkeypatch):
    # Arrange
    relatorio = Relatorio(
        "dummy.csv", "text", data_inicial="2025-01-01", data_final="2025-01-31"
    )
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-02-01",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is None


def test_obter_venda_apenas_data_inicial_igual():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text", data_inicial="2025-01-15")
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-01-15",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is not None


def test_obter_venda_apenas_data_inicial_diferente():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text", data_inicial="2025-01-15")
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-01-16",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is None


def test_obter_venda_apenas_data_final_igual():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text", data_final="2025-01-15")
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-01-15",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is not None


def test_obter_venda_apenas_data_final_diferente():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text", data_final="2025-01-15")
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-01-16",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is None


def test_obter_venda_sem_filtro_data():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text")
    linha = {
        "produto": "Camiseta",
        "preco_unitario": "49.90",
        "quantidade": "2",
        "data": "2025-01-15",
    }
    produto = Produto(nome="Camiseta", preco=Decimal("49.90"))
    # Act
    venda = relatorio._Relatorio__obter_venda(linha, produto)
    # Assert
    assert venda is not None
    assert venda.quantidade == 2
    assert venda.produto.nome == "Camiseta"


def test_prepara_e_valida_as_datas_invalida():
    # Arrange
    relatorio = Relatorio(
        "dummy.csv", "text", data_inicial="2025-12-31", data_final="2025-01-01"
    )
    # Act / Assert
    with pytest.raises(ValueError) as excinfo:
        relatorio._Relatorio__prepara_e_valida_as_datas()
    assert "Data inicial não pode ser maior que a data final." in str(excinfo.value)


def test_calcular_total_vendas_sem_vendas():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text")
    relatorio.vendas = []
    # Act
    total = relatorio._Relatorio__calcular_total_vendas()
    # Assert
    assert total == Decimal("0.00")


def test_obter_maior_venda_sem_vendas():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text")
    relatorio.vendas = []
    # Act
    maior = relatorio._Relatorio__obter_maior_venda()
    # Assert
    assert maior is None


def test_obter_maior_venda_com_vendas():
    # Arrange
    relatorio = Relatorio("dummy.csv", "text")
    produto1 = Produto(nome="Camiseta", preco=Decimal("49.90"))
    produto2 = Produto(nome="Calça", preco=Decimal("99.90"))
    venda1 = Venda(produto=produto1, quantidade=2, data_str="2025-01-01")
    venda2 = Venda(produto=produto1, quantidade=3, data_str="2025-01-02")
    venda3 = Venda(produto=produto2, quantidade=1, data_str="2025-01-03")
    relatorio.vendas = [venda1, venda2, venda3]
    # Act
    maior = relatorio._Relatorio__obter_maior_venda()
    # Assert
    assert maior.produto.nome == "Camiseta"
    assert maior.quantidade == 5
