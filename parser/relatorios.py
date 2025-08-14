from csv import DictReader
from decimal import Decimal
from pathlib import Path
from typing import List

from core.logger import logger
from parser.modelos import Produto, Venda


class Relatorio:
    def __init__(
        self,
        caminho_arquivo: str,
        formato: str = "text",
        data_inicial: str = "",
        data_final: str = "",
    ):
        """
        Inicializa o relatório com o caminho do arquivo, formato e datas opcionais.
        """
        self.caminho_arquivo: str = caminho_arquivo
        self.formato: str = formato.lower()
        self.__validar_formato()

        # As datas são strings, mas serão convertidas para datetime.date caso necessário
        self.data_inicial: str = data_inicial
        self.data_final: str = data_final
        self.vendas: List[Venda] = []
        self.produtos: List[Produto] = []

    def __validar_formato(self):
        """
        Valida o formato do relatório.
        Lança ValueError se o formato não for suportado.
        """
        formatos_validos = ["text", "txt", "json"]
        if self.formato not in formatos_validos:
            mensagem = f"Formato de relatório desconhecido: {self.formato}. "
            mensagem += f"Formatos válidos: {', '.join(formatos_validos)}"
            logger.error(mensagem)
            raise ValueError(mensagem)

    def gerar_relatorio(self):
        """
        Gera o relatório com base no formato especificado.
        Retorna o relatório como uma string.
        """
        # Lê as vendas do arquivo
        self.vendas = self.__extrair_dados_de_vendas()
        if not self.vendas:
            message = "Nenhuma venda encontrada."
            logger.warning(message)
            raise ValueError(message)

        return self.__obter_relatorio_conforme_formato()

    def __obter_relatorio_conforme_formato(self):
        match self.formato:
            case "json":
                return self.__obter_relatorio_json()
            case _:
                return self.__obter_relatorio_texto()

    def __obter_relatorio_json(self):
        """Gera o relatório no formato JSON."""
        import json

        # Calcula o total de vendas
        total_vendas = self.calcular_total_vendas()

        # Obtém o produto mais vendido
        produto_mais_vendido = self.obter_produto_mais_vendido()
        relatorio = {
            "total_vendas": str(total_vendas),
            "produto_mais_vendido": (
                {
                    "nome": produto_mais_vendido.nome,
                    "preco": str(produto_mais_vendido.preco),
                }
                if produto_mais_vendido
                else None
            ),
        }
        return json.dumps(relatorio, indent=4)

    def __obter_relatorio_texto(self):
        """Gera o relatório no formato de texto."""

        # Calcula o total de vendas
        total_vendas = self.calcular_total_vendas()

        # Obtém o produto mais vendido
        produto_mais_vendido = self.obter_produto_mais_vendido()
        relatorio = "Relatório de Vendas\n"
        relatorio += f"Total de Vendas: {total_vendas:.2f}\n"

        if produto_mais_vendido:
            produto_nome = produto_mais_vendido.nome
            produto_preco = produto_mais_vendido.preco
            relatorio += f"Produto Mais Vendido: {produto_nome} ({produto_preco:.2f})\n"
        else:
            relatorio += "Nenhum produto vendido.\n"
        return relatorio

    def __extrair_dados_de_vendas(self) -> List[Venda]:
        """Lê um arquivo CSV e retorna seu conteúdo como uma lista de objetos Venda."""
        caminho_arquivo = Path(self.caminho_arquivo)
        if not caminho_arquivo.exists():
            mensagem = f"Arquivo {caminho_arquivo} não encontrado."
            logger.error(mensagem)
            raise FileNotFoundError(mensagem)

        with caminho_arquivo.open("r", encoding="utf-8") as file:
            reader = DictReader(file)
            return [Venda(**linha) for linha in reader]

    def calcular_total_vendas(self) -> Decimal:
        """Calcula o total das vendas."""
        total = Decimal("0.00")
        for venda in self.vendas:
            total += venda.produto.preco * Decimal(venda.quantidade)
        return total

    def obter_produto_mais_vendido(self) -> Produto | None:
        """Obtém o produto mais vendido."""
        if not self.vendas:
            return None

        produto_mais_vendido = self.vendas[0].produto
        quantidade_mais_vendida = self.vendas[0].quantidade

        for venda in self.vendas[1:]:
            if venda.quantidade > quantidade_mais_vendida:
                produto_mais_vendido = venda.produto
                quantidade_mais_vendida = venda.quantidade

        return produto_mais_vendido
