from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Produto:
    nome: str
    preco: Decimal


@dataclass
class Venda:
    produto: Produto
    quantidade: int
    data_str: str = field(repr=False)
