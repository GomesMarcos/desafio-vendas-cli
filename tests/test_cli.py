import sys
from unittest.mock import MagicMock, patch

import pytest

from parser.main import main
from tests.fixtures.cli import (
    happy_cli_ids,
    happy_cli_params,
)


@pytest.mark.parametrize(
    "cli_args, relatorio_return, expected_print",
    happy_cli_params,
    ids=happy_cli_ids,
)
def test_main_cli_happy_and_edge_cases(cli_args, relatorio_return, expected_print):
    # Arranjo
    with (
        patch.object(sys, "argv", cli_args),
        patch("parser.main.Relatorio") as mock_relatorio_class,
        patch("builtins.print") as mock_print,
    ):
        mock_instance = MagicMock()
        mock_instance.gerar_relatorio.return_value = relatorio_return
        mock_relatorio_class.return_value = mock_instance

        # Ação
        main()

        # Asserção
        mock_relatorio_class.assert_called_once()
        mock_instance.gerar_relatorio.assert_called_once()
        mock_print.assert_called_once_with(expected_print)


@pytest.mark.parametrize(
    "cli_args, expected_error, expected_message",
    [
        (
            # Caso de erro: argumento caminho_arquivo obrigatório ausente
            ["main.py"],
            SystemExit,
            "usage:",
        ),
        (
            # Caso de erro: valor inválido para format
            ["main.py", "dummy.csv", "--format", "xml"],
            SystemExit,
            "invalid choice",
        ),
    ],
    ids=[
        "erro-ausente-caminho_arquivo",
        "erro-formato-invalido",
    ],
)
def test_main_cli_error_cases(cli_args, expected_error, expected_message):
    # Arranjo
    import io
    from contextlib import redirect_stderr

    with patch.object(sys, "argv", cli_args), patch("builtins.print") as mock_print:
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            with pytest.raises(expected_error):
                main()
        # Verifica se a mensagem esperada está no stderr
        stderr_output = stderr.getvalue()
        assert expected_message in stderr_output
        mock_print.assert_not_called()
