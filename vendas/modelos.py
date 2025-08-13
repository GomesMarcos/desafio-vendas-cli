from decimal import Decimal


class Produto:
    def __init__(self, id: int, nome: str, preco: Decimal):
        self.id = id
        self.nome = nome
        self.preco = preco

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome}, preco={self.preco})"


class Venda:
    def __init__(self, id: int, produto: Produto, quantidade: int):
        self.id = id
        self.produto = produto
        self.quantidade = quantidade

    def __repr__(self):
        return (
            f"Venda(id={self.id}, produto={self.produto}, quantidade={self.quantidade})"
        )
