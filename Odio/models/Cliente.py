from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    idUsuario: int
    nome: str
    email: str
    telefone: str
    endLogradouro: Optional[str] = ""
    endNumero: Optional[str] = ""
    endComplemento: Optional[str] = ""
    endBairro: Optional[str] = ""
    endCidade:Optional[str] = ""
    endUf: Optional[str] = ""