from dataclasses import dataclass

@dataclass
class Servico:
    id_servico: int = None
    nome: str = None
    descricao: str = None
    preco: float = None
    duracao_minutos: int = None
    disponivel: bool = True
    id_veterinario: int = None
