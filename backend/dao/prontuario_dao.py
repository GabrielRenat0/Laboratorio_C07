from dao.base_dao import BaseDAO
from models.prontuario import Prontuario


class ProntuarioDAO(BaseDAO):
    table, pk, model = "prontuario", "id_prontuario", Prontuario

    def find_by_animal(self, id_animal):
        return self._search(
            "SELECT * FROM prontuario WHERE id_animal = %s", (id_animal,))

    def list_with_animal(self):
        return self.db.fetch_all(
            "SELECT p.id_prontuario, an.nome, p.alergias, p.vacinas_em_dia, "
            "p.data_ultima_vacina "
            "FROM prontuario p "
            "INNER JOIN animal an ON an.id_animal = p.id_animal "
            "ORDER BY an.nome")
