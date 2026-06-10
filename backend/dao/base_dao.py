from dataclasses import fields


class BaseDAO:
    """Generic CRUD shared by every DAO."""

    table = pk = model = None

    def __init__(self, db):
        self.db = db

    def _cols(self):
        return [f.name for f in fields(self.model) if f.name != self.pk]

    def _to_model(self, row):
        return self.model(*row)

    def insert(self, obj):
        cols = self._cols()
        placeholders = ", ".join(["%s"] * len(cols))
        query = f"INSERT INTO {self.table} ({', '.join(cols)}) VALUES ({placeholders})"
        new_id, _ = self.db.execute(query, [getattr(obj, c) for c in cols])
        setattr(obj, self.pk, new_id)
        return new_id

    def find_all(self):
        rows = self.db.fetch_all(f"SELECT * FROM {self.table} ORDER BY {self.pk}")
        return [self._to_model(r) for r in rows]

    def find_by_id(self, id_):
        row = self.db.fetch_one(
            f"SELECT * FROM {self.table} WHERE {self.pk} = %s", (id_,))
        return self._to_model(row) if row else None

    def update(self, obj):
        cols = self._cols()
        sets = ", ".join(f"{c} = %s" for c in cols)
        query = f"UPDATE {self.table} SET {sets} WHERE {self.pk} = %s"
        values = [getattr(obj, c) for c in cols] + [getattr(obj, self.pk)]
        _, affected = self.db.execute(query, values)
        return affected

    def delete(self, id_):
        _, affected = self.db.execute(
            f"DELETE FROM {self.table} WHERE {self.pk} = %s", (id_,))
        return affected

    def _search(self, query, params):
        return [self._to_model(r) for r in self.db.fetch_all(query, params)]
