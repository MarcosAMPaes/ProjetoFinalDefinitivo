# models/Projeto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: int
    idCategoria: int
    nome: str
    estoque: str
    preco: float
    descricao: str
    imgProduto: Optional[str] = ""