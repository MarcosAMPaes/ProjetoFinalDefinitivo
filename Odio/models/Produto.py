# models/Projeto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: int
    idCategoria: int
    nome: str
    descricao: str
    estoque: str
    preco: float
    imgProduto: Optional[str] = ""