from dao.base_dao import BaseDAO
from models.animal import Animal


class AnimalDAO(BaseDAO):
    table, pk, model = "animal", "id_animal", Animal

    def find_by_species(self, species):
        return self._search(
            "SELECT * FROM animal WHERE LOWER(especie) LIKE LOWER(%s) ORDER BY nome",
            (f"%{species}%",))

    def list_with_owner(self):
        return self.db.fetch_all(
            "SELECT a.id_animal, a.nome, a.especie, d.nome, d.telefone "
            "FROM animal a "
            "INNER JOIN dono d ON d.id_dono = a.id_dono "
            "ORDER BY a.nome")
