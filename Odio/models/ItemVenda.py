from dataclasses import dataclass

@dataclass
class ItemVenda:
    id: int
    idVenda: int
    idProduto: int 
    quantidade: str
    subtotal: str
