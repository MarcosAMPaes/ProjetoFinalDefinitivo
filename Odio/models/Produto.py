# models/Projeto.py
from dataclasses import dataclass

@dataclass
class Produto:
    id: int
    nome: str
    estoque: str
    preco: float
    descricao: str