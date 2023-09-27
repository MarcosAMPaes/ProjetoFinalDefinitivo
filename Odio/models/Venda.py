from dataclasses import dataclass
from datetime import date
from xmlrpc.client import Boolean, boolean
from Cliente import Cliente
@dataclass
class Venda:
    id: int
    idCliente: int
    DataHora: date
    status: str
    valorTotal: int