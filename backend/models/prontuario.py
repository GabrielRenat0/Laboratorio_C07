from dataclasses import dataclass

@dataclass
class Prontuario:
    id_prontuario: int = None
    alergias: str = None
    vacinas_em_dia: bool = False
    data_ultima_vacina: str = None
    id_animal: int = None
