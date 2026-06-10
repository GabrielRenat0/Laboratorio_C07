from dataclasses import dataclass

@dataclass
class Animal:
    id_animal: int = None
    nome: str = None
    especie: str = None
    raca: str = None
    data_nascimento: str = None
    peso: float = None
    possui_cadastro: bool = False
    observacoes: str = None
    id_dono: int = None
