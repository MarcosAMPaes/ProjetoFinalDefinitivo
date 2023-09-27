from dataclasses import dataclass

@dataclass
class Cliente:
    idUsuario: int
    nome: str
    email: str
    telefone: str
    endLogradouro: str
    endNumero: str
    endComplemento: str
    endBairro: str
    endCidade:str
    endUf: str