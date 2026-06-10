from dao.base_dao import BaseDAO
from models.veterinario import Veterinario


class VeterinarioDAO(BaseDAO):
    table, pk, model = "veterinario", "id_veterinario", Veterinario

    def find_by_specialty(self, specialty):
        return self._search(
            "SELECT * FROM veterinario WHERE LOWER(especialidade) LIKE LOWER(%s) "
            "ORDER BY nome",
            (f"%{specialty}%",))
