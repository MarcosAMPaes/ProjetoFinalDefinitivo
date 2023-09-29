from Venda import Venda
from Produto import Produto
from dataclasses import dataclass

@dataclass
class ItemVenda:
    idProduto: int
    idVenda: int
    quantidade: str
    valorUnit: str
    subtotal: str
