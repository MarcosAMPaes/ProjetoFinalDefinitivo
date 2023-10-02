from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id: int
    nome: str
    email: str
    senha: Optional[str] = ""
    telefone: Optional[str] = ""
    endLogradouro: Optional[str] = ""
    endNumero: Optional[str] = ""
    cep: Optional[str] = ""
    token: Optional[str] = ""
    admin: Optional[bool] = False