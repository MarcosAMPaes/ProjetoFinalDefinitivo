from Venda import Venda
from Produto import Produto
from dataclasses import dataclass

@dataclass
class ItemVenda:
    idVenda: int
    idProduto: int
    quantidade: str
    valorUnit: str
    subtotal: str
