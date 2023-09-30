# models/Projeto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    admin: bool = False