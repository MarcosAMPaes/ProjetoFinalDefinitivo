# models/Projeto.py
from dataclasses import dataclass

from Usuario import Usuario

@dataclass
class Administrador:
    id: int
    idUsuario: int
    nome: str
    email: str
    telefone: str