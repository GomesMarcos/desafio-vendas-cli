from decimal import Decimal
from typing import List

from vendas.modelos import Produto, Venda


def calcular_total_vendas(vendas: List[Venda]) -> Decimal:
    """Calcula o total das vendas."""
    total = Decimal("0.00")
    for venda in vendas:
        total += venda.produto.preco * Decimal(venda.quantidade)
    return total


def obter_produto_mais_vendido(vendas: List[Venda]) -> Produto | None:
    """Obtém o produto mais vendido."""
    if not vendas:
        return None

    produto_mais_vendido = vendas[0].produto
    quantidade_mais_vendida = vendas[0].quantidade

    for venda in vendas[1:]:
        if venda.quantidade > quantidade_mais_vendida:
            produto_mais_vendido = venda.produto
            quantidade_mais_vendida = venda.quantidade

    return produto_mais_vendido
