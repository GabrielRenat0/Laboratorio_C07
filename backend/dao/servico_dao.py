from dao.base_dao import BaseDAO
from models.servico import Servico


class ServicoDAO(BaseDAO):
    table, pk, model = "servico", "id_servico", Servico

    def find_by_name(self, name):
        return self._search(
            "SELECT * FROM servico WHERE LOWER(nome) LIKE LOWER(%s) ORDER BY nome",
            (f"%{name}%",))

    # SELECT with JOIN: each service with the veterinarian in charge.
    def list_with_vet(self):
        return self.db.fetch_all(
            "SELECT s.id_servico, s.nome, s.preco, v.nome, v.especialidade "
            "FROM servico s "
            "INNER JOIN veterinario v ON v.id_veterinario = s.id_veterinario "
            "ORDER BY s.nome")
