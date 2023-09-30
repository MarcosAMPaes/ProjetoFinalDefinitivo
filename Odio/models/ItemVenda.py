from Venda import Venda
from Produto import Produto
from dataclasses import dataclass

@dataclass
class ItemVenda:
    id: int
    idProduto: int 
    idVenda: int
    quantidade: str
    valorUnit: str
    subtotal: str
