from unittest.mock import MagicMock, patch

import pytest

from parser.relatorios import Relatorio
from tests.fixtures import (
    dummy_csv_file,  # noqa: F401 # Importa explicitamente a fixture
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
    relatorio.__extrair_dados_de_vendas = MagicMock(return_value=vendas)
    relatorio.__obter_relatorio_conforme_formato = MagicMock(
        return_value=expected_output
    )

    # Act
    result = relatorio.gerar_relatorio()

    # Assert
    assert result == expected_output
    relatorio.__extrair_dados_de_vendas.assert_called_once()
    relatorio.__obter_relatorio_conforme_formato.assert_called_once()


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
    relatorio.__extrair_dados_de_vendas = MagicMock(return_value=vendas)

    # Act / Assert
    with patch("core.logger.logger") as mock_logger:
        with pytest.raises(ValueError) as excinfo:
            relatorio.gerar_relatorio()
        assert str(excinfo.value) == expected_message
        mock_logger.warning.assert_called_once_with(expected_message)


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
