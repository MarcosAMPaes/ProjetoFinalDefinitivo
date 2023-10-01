from dataclasses import dataclass
from datetime import date
@dataclass
class Venda:
    id: int
    idCliente: int
    dataHora: date
    status: str
    valorTotal: int