from dataclasses import dataclass

@dataclass
class Consulta:
    id_consulta: int = None
    id_animal: int = None
    id_veterinario: int = None
    data_consulta: str = None
    horario: str = None
    valor: float = None
    diagnostico: str = None
