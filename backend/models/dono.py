from dataclasses import dataclass

@dataclass
class Dono:
    id_dono: int = None
    nome: str = None
    cpf: str = None
    telefone: str = None
    email: str = None
