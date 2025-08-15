from csv import DictReader
from decimal import Decimal
from pathlib import Path
from typing import List

from helpers.date_handler import DateHandler
from helpers.logger import logger
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
        self.base_caminho_relatorio = Path("output/relatorio")

    def __validar_formato(self):
        """
        Valida o formato do relatório.
        Lança ValueError se o formato não for suportado.
        """
        logger.debug(f"Validando formato do relatório: {self.formato}")
        formatos_validos = ["text", "txt", "json"]
        if self.formato not in formatos_validos:
            mensagem = f"Formato de relatório desconhecido: {self.formato}. "
            mensagem += f"Formatos válidos: {', '.join(formatos_validos)}"
            logger.error(mensagem)
            raise ValueError(mensagem)

    def gerar_relatorio(self) -> Path:
        """
        Gera o relatório e retorna o caminho do relatório gerado.
        """
        logger.debug("Iniciando relatório")
        # Lê as vendas do arquivo
        self.__extrair_dados_de_vendas()
        if not self.vendas:
            message = "Nenhuma venda encontrada."
            logger.warning(message)
            raise ValueError(message)

        return self.__obter_relatorio_conforme_formato()

    def __obter_relatorio_conforme_formato(self) -> Path:
        logger.debug("Obtendo relatório conforme o formato")
        match self.formato:
            case "json":
                relatorio = self.__gerar_relatorio_json()
            case _:
                relatorio = self.__gerar_relatorio_texto()

        caminho_completo = Path(
            f"{self.base_caminho_relatorio}_{DateHandler.obter_data_e_hora_para_salvar_relatorio()}.{self.formato}"  # noqa: E501
        )
        with open(caminho_completo, "w", encoding="utf-8") as file:
            file.write(relatorio)
            logger.info(
                f"Relatório gerado com sucesso! Acesse-o em: {caminho_completo}"
            )

        return caminho_completo

    def __gerar_relatorio_json(self):
        """Gera o relatório no formato JSON."""
        import json

        # Calcula o total de vendas
        total_vendas = self.__calcular_total_vendas()

        # Obtém a maior venda
        maior_venda = self.__obter_maior_venda()
        produto_mais_vendido = maior_venda.produto if maior_venda else None
        quantidade_mais_vendida = maior_venda.quantidade if maior_venda else 0

        # Obtém o total de vendas por produto
        total_vendas_por_produto = self.__obter_total_de_vendas_por_produto()

        relatorio = {
            "total_vendas": str(total_vendas),
            "total_por_produto": {
                nome: str(valor) for nome, valor in total_vendas_por_produto.items()
            },
            "produto_mais_vendido": (
                {
                    "nome": produto_mais_vendido.nome,
                    "preco": f"R${produto_mais_vendido.preco}",
                    "quantidade": quantidade_mais_vendida,
                    "data": maior_venda.data_str,
                }
                if produto_mais_vendido
                else None
            ),
        }
        logger.info("Relatório de vendas em JSON gerado com sucesso!")
        return json.dumps(relatorio, indent=4)

    def __gerar_relatorio_texto(self):
        """Gera o relatório no formato de texto."""

        self.formato = "txt"

        # Calcula o total de vendas
        total_vendas = self.__calcular_total_vendas()

        # Obtém a maior venda
        maior_venda = self.__obter_maior_venda()
        produto_mais_vendido = maior_venda.produto if maior_venda else None
        quantidade_mais_vendida = maior_venda.quantidade if maior_venda else 0

        # Obtém o total de vendas por produto
        total_vendas_por_produto = self.__obter_total_de_vendas_por_produto()

        relatorio = "Relatório de Vendas\n"
        relatorio += f"Total em Vendas: R${total_vendas:.2f}\n"
        relatorio += "Total de vendas por produto:\n"
        for nome, valor in total_vendas_por_produto.items():
            relatorio += f"  - {nome}: R${valor:.2f}\n"

        produto_nome = produto_mais_vendido.nome
        produto_preco = produto_mais_vendido.preco
        relatorio += f"Produto Mais Vendido:\n"
        relatorio += f"  - Nome: {produto_nome}\n"
        relatorio += f"  - Preço: R${produto_preco:.2f}\n"
        relatorio += f"  - Quantidade Vendida: {quantidade_mais_vendida}\n"
        relatorio += f"  - Data da venda: {maior_venda.data_str}\n"
        logger.info("Relatório de vendas em texto gerado com sucesso!")
        return relatorio

    def __extrair_dados_de_vendas(self) -> None:
        """
        Lê um arquivo CSV e retorna seu conteúdo como uma lista de objetos Venda,
        Usando um Produto instanciado do cabeçalho.
        """
        logger.debug("Extraindo dados de vendas do arquivo CSV")
        caminho_arquivo = Path(self.caminho_arquivo)

        if not caminho_arquivo.exists():
            mensagem = f"Arquivo {caminho_arquivo} não encontrado."
            logger.error(mensagem)
            raise FileNotFoundError(mensagem)

        with caminho_arquivo.open("r", encoding="utf-8") as file:
            reader = DictReader(file)
            produto_instanciado = None
            for linha in reader:
                # Instancia o produto
                produto_instanciado = Produto(
                    nome=linha.get("produto", ""),
                    preco=Decimal(linha.get("preco_unitario", "0.00")),
                )
                self.produtos.append(produto_instanciado)
                if venda := self.__obter_venda(linha, produto_instanciado):
                    self.vendas.append(venda)
            logger.info(f"Total de vendas extraídas: {len(self.vendas)}")

    def __obter_venda(self, linha: dict, produto_instanciado: Produto) -> Venda | None:
        """
        Cria uma instância de Venda a partir de uma linha do CSV.
        Se houver filtro de data, verifica se a data da venda está dentro do intervalo.
        Retorna None se a venda não atender aos critérios de data.
        """

        if not (data_venda := DateHandler.str_to_date(linha.get("data", ""))):
            mensagem = f"Data não informada na linha: {linha}"
            logger.error(mensagem)
            raise ValueError(mensagem)

        venda = Venda(
            produto=produto_instanciado,
            quantidade=int(linha.get("quantidade", "0")),
            data_str=linha["data"],
        )
        if self.data_inicial and self.data_final:
            # Se houver filtro de data, verifica se a data
            # da venda está dentro do intervalo

            self.__prepara_e_valida_as_datas()

            if not DateHandler.valida_data_entre_intervalo(
                data_venda, self.data_inicial, self.data_final
            ):
                return None
            logger.info("Venda dentro do intervalo de datas.")
        elif self.data_inicial or self.data_final:
            # Se houver apenas uma data, verifica se a data da venda
            # é igual à data inicial ou final
            datas = []
            if self.data_inicial:
                datas.append(DateHandler.str_to_date(self.data_inicial))
            if self.data_final:
                datas.append(DateHandler.str_to_date(self.data_final))
            if datas and data_venda not in datas:
                return None
            logger.info(f"Data informada para filtro: {data_venda}")
        logger.debug(f"Venda obtida: {venda}")
        return venda

    def __prepara_e_valida_as_datas(self):
        """
        Prepara e valida as datas de início e fim.
        Converte as strings para datetime.date
        E verifica se a data inicial não é maior que a final.
        """
        logger.debug("Preparando e validando as datas do filtro")
        self.data_inicial = DateHandler.str_to_date(self.data_inicial)
        self.data_final = DateHandler.str_to_date(self.data_final)

        if self.data_inicial > self.data_final:
            mensagem = "Data inicial não pode ser maior que a data final."
            logger.error(mensagem)
            raise ValueError(mensagem)

    def __calcular_total_vendas(self) -> Decimal:
        """Calcula o total das vendas."""
        logger.debug("Calculando o total das vendas")
        total = Decimal("0.00")
        if not self.vendas:
            return total
        total += sum(
            venda.produto.preco * Decimal(venda.quantidade) for venda in self.vendas
        )
        return total

    def __obter_maior_venda(self) -> Venda | None:
        """Obtém a maior venda, somando quantidades de produtos com o mesmo nome."""
        if not self.vendas:
            return None

        # Agrupa vendas por nome do produto e soma as quantidades
        vendas_por_produto = {}
        for venda in self.vendas:
            nome = venda.produto.nome
            if nome not in vendas_por_produto:
                vendas_por_produto[nome] = Venda(
                    produto=venda.produto,
                    quantidade=venda.quantidade,
                    data_str=venda.data_str,
                )
            else:
                vendas_por_produto[nome].quantidade += venda.quantidade

        # Retorna a venda com maior quantidade
        return max(vendas_por_produto.values(), key=lambda v: v.quantidade)

    def __obter_total_de_vendas_por_produto(self):
        """Obtém o total de vendas por produto."""
        logger.debug("Obtendo o total de vendas por produto")
        total_por_produto = {}
        for venda in self.vendas:
            nome = venda.produto.nome
            if nome not in total_por_produto:
                total_por_produto[nome] = Decimal("0.00")
            total_por_produto[nome] += venda.produto.preco * Decimal(venda.quantidade)
        return total_por_produto
