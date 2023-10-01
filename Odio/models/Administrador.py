# models/Projeto.py
from dataclasses import dataclass


@dataclass
class Administrador:
    id: int
    idUsuario: int
    nome: str
    email: str
    telefone: str