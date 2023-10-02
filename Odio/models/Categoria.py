# models/Projeto.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Categoria:
    id: int
    nome: str
    