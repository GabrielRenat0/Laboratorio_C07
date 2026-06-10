from dao.base_dao import BaseDAO
from models.consulta import Consulta


class ConsultaDAO(BaseDAO):
    table, pk, model = "consulta", "id_consulta", Consulta

    def find_by_date(self, date):
        return self._search(
            "SELECT * FROM consulta WHERE data_consulta = %s ORDER BY horario",
            (date,))
    
    def list_detailed(self):
        return self.db.fetch_all(
            "SELECT c.id_consulta, a.nome, a.especie, d.nome, v.nome, "
            "c.data_consulta, c.horario, c.valor, c.diagnostico "
            "FROM consulta c "
            "INNER JOIN animal      a ON a.id_animal      = c.id_animal "
            "INNER JOIN dono        d ON d.id_dono        = a.id_dono "
            "INNER JOIN veterinario v ON v.id_veterinario = c.id_veterinario "
            "ORDER BY c.data_consulta, c.horario")
