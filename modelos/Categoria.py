# models/Projeto.py
from dataclasses import dataclass

@dataclass
class Categoria:
    id: int
    nome: str