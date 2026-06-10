from dao.base_dao import BaseDAO
from models.dono import Dono


class DonoDAO(BaseDAO):
    table, pk, model = "dono", "id_dono", Dono

    def find_by_name(self, name):
        return self._search(
            "SELECT * FROM dono WHERE LOWER(nome) LIKE LOWER(%s) ORDER BY nome",
            (f"%{name}%",))
