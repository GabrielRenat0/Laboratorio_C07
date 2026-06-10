from mysql.connector import Error

from config import MYSQL_CONFIG
from database import DatabaseManager
from models.dono import Dono
from models.veterinario import Veterinario
from models.animal import Animal
from models.prontuario import Prontuario
from models.servico import Servico
from models.consulta import Consulta
from dao.dono_dao import DonoDAO
from dao.veterinario_dao import VeterinarioDAO
from dao.animal_dao import AnimalDAO
from dao.prontuario_dao import ProntuarioDAO
from dao.servico_dao import ServicoDAO
from dao.consulta_dao import ConsultaDAO


# ---- Input helpers (ENTER keeps the current value when editing) ----

def read_text(prompt, current=None):
    value = input(f"{prompt} [{current}]: " if current is not None
                  else f"{prompt}: ").strip()
    return value or current


def read_optional(prompt, current=None):
    return input(f"{prompt} [{current or ''}]: ").strip() or current


def read_int(prompt, current=None):
    while True:
        try:
            return int(read_text(prompt, current))
        except (TypeError, ValueError):
            print("  -> digite um numero inteiro valido")


def read_float(prompt, current=None):
    while True:
        try:
            return float(read_text(prompt, current))
        except (TypeError, ValueError):
            print("  -> digite um numero valido (use ponto, ex.: 120.50)")


def read_bool(prompt, current=None):
    current = None if current is None else ("s" if current else "n")
    return read_text(f"{prompt} (s/n)", current).lower().startswith("s")


READERS = {"text": read_text, "opt": read_optional, "int": read_int,
           "float": read_float, "bool": read_bool}


# ---- Generic, data-driven CRUD menu used for every table ----

def fill(entity, obj=None):
    """Build a new model (or edit an existing one) field by field."""
    obj = obj or entity["model"]()
    for name, prompt, kind in entity["fields"]:
        setattr(obj, name, READERS[kind](prompt, getattr(obj, name)))
    return obj


def crud_menu(entity):
    dao = entity["dao"]
    search_label, search_method, search_prompt, search_kind = entity["search"]
    join = entity.get("join")

    while True:
        print(f"\n--- {entity['title']} ---")
        line = (f"1.Inserir  2.Listar todos  3.Buscar por id  4.{search_label}  "
                "5.Atualizar  6.Deletar")
        if join:
            line += f"  7.{join[0]}"
        print(line + "  0.Voltar")
        op = input("Opcao: ").strip()

        try:
            if op == "1":
                print(f"  -> inserido com id {dao.insert(fill(entity))}")
            elif op == "2":
                for obj in dao.find_all():
                    print("  ", obj)
            elif op == "3":
                print("  ", dao.find_by_id(read_int("Id")) or "nao encontrado")
            elif op == "4":
                results = getattr(dao, search_method)(READERS[search_kind](search_prompt))
                for obj in results:
                    print("  ", obj)
                if not results:
                    print("  nenhum registro encontrado")
            elif op == "5":
                obj = dao.find_by_id(read_int("Id para atualizar"))
                if obj:
                    dao.update(fill(entity, obj))
                    print("  -> atualizado")
                else:
                    print("  nao encontrado")
            elif op == "6":
                print("  -> deletado" if dao.delete(read_int("Id para deletar"))
                      else "  nada deletado")
            elif op == "7" and join:
                for row in getattr(dao, join[1])():
                    print("  ", " | ".join(str(v) for v in row))
            elif op == "0":
                return
            else:
                print("  opcao invalida")
        except Error as e:
            print(f"  ERRO no banco: {e}")


def build_entities(db):
    """One config entry per table: fields (for insert/update), the search
    method and an optional JOIN report."""
    return {
        "1": {"title": "Donos (dono)", "model": Dono, "dao": DonoDAO(db),
              "fields": [("nome", "Nome", "text"), ("cpf", "CPF", "text"),
                         ("telefone", "Telefone", "opt"), ("email", "Email", "opt")],
              "search": ("Buscar por nome", "find_by_name", "Nome", "text")},

        "2": {"title": "Veterinarios (veterinario)", "model": Veterinario,
              "dao": VeterinarioDAO(db),
              "fields": [("nome", "Nome", "text"), ("crmv", "CRMV", "text"),
                         ("especialidade", "Especialidade", "opt"),
                         ("salario", "Salario", "float")],
              "search": ("Buscar por especialidade", "find_by_specialty",
                         "Especialidade", "text")},

        "3": {"title": "Animais (animal)", "model": Animal, "dao": AnimalDAO(db),
              "fields": [("nome", "Nome", "text"), ("especie", "Especie", "text"),
                         ("raca", "Raca", "opt"),
                         ("data_nascimento", "Data nascimento (AAAA-MM-DD)", "opt"),
                         ("peso", "Peso (kg)", "float"),
                         ("possui_cadastro", "Possui cadastro?", "bool"),
                         ("observacoes", "Observacoes", "opt"),
                         ("id_dono", "Id do dono", "int")],
              "search": ("Buscar por especie", "find_by_species", "Especie", "text"),
              "join": ("Animais com dono (JOIN)", "list_with_owner")},

        "4": {"title": "Prontuarios (prontuario)", "model": Prontuario,
              "dao": ProntuarioDAO(db),
              "fields": [("alergias", "Alergias", "opt"),
                         ("vacinas_em_dia", "Vacinas em dia?", "bool"),
                         ("data_ultima_vacina", "Ultima vacina (AAAA-MM-DD)", "opt"),
                         ("id_animal", "Id do animal", "int")],
              "search": ("Buscar por id do animal", "find_by_animal",
                         "Id do animal", "int"),
              "join": ("Prontuarios com animal (JOIN)", "list_with_animal")},

        "5": {"title": "Servicos (servico)", "model": Servico, "dao": ServicoDAO(db),
              "fields": [("nome", "Nome", "text"), ("descricao", "Descricao", "opt"),
                         ("preco", "Preco", "float"),
                         ("duracao_minutos", "Duracao (min)", "int"),
                         ("disponivel", "Disponivel?", "bool"),
                         ("id_veterinario", "Id do veterinario", "int")],
              "search": ("Buscar por nome", "find_by_name", "Nome", "text"),
              "join": ("Servicos com veterinario (JOIN)", "list_with_vet")},

        "6": {"title": "Consultas (consulta)", "model": Consulta,
              "dao": ConsultaDAO(db),
              "fields": [("id_animal", "Id do animal", "int"),
                         ("id_veterinario", "Id do veterinario", "int"),
                         ("data_consulta", "Data (AAAA-MM-DD)", "text"),
                         ("horario", "Horario (HH:MM:SS)", "text"),
                         ("valor", "Valor", "float"),
                         ("diagnostico", "Diagnostico", "opt")],
              "search": ("Buscar por data", "find_by_date", "Data (AAAA-MM-DD)", "text"),
              "join": ("Relatorio detalhado (JOIN de 4 tabelas)", "list_detailed")},
    }


def main():
    print("=== Clinica Veterinaria - Python + MySQL ===")
    try:
        db = DatabaseManager(**MYSQL_CONFIG)
    except Error as e:
        print(f"Nao foi possivel conectar: {e}\n"
              "Verifique o config.py e rode o script .sql primeiro.")
        return

    entities = build_entities(db)
    while True:
        print("\n===== MENU PRINCIPAL =====")
        for key, entity in entities.items():
            print(f"{key}. {entity['title']}")
        print("0. Sair")
        op = input("Opcao: ").strip()

        if op == "0":
            db.close()
            print("Ate logo!")
            return
        if op in entities:
            crud_menu(entities[op])
        else:
            print("Opcao invalida")


if __name__ == "__main__":
    main()
