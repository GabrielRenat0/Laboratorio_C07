from dataclasses import dataclass

@dataclass
class Veterinario:
    id_veterinario: int = None
    nome: str = None
    crmv: str = None
    especialidade: str = None
    salario: float = None
