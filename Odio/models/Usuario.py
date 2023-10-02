# models/Projeto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id: int
    idCliente: int
    nome: str
    email: str
    admin: bool = False