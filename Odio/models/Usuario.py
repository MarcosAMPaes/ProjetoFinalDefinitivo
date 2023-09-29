# models/Projeto.py
from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    nome: str
    senha: Optional[str] = ""
    token: Optional[str] = ""
    admin: bool = False