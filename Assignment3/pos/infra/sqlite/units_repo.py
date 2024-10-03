import uuid
from dataclasses import dataclass
from sqlite3 import Connection, Cursor
from uuid import UUID

from pos.core.errors import DoesNotExistError, ExistsError
from pos.core.units import Unit


@dataclass
class SQLUnitRepository:
    con: Connection
    cur: Cursor

    def create(self, unit: Unit) -> None:
        self.cur.execute(
            "SELECT * FROM units WHERE Name = :name", {"name": unit.get_name()}
        )
        if len(list(self.cur.fetchall())) != 0:
            raise ExistsError(unit.get_name())
        self.cur.execute(
            "INSERT INTO units VALUES (?, ?)",
            (str(unit.get_id()), unit.get_name()),
        )

        self.con.commit()

    def read_one(self, unit_id: UUID) -> Unit:
        id = str(unit_id)
        self.cur.execute("SELECT * FROM units WHERE ID = :id", {"id": id})
        res = list(self.cur.fetchall())
        if len(res) == 0:
            raise DoesNotExistError(unit_id)
        res = res[0]
        return Unit(id=uuid.UUID(res[0]), name=res[1])

    def list(self) -> list[Unit]:
        self.cur.execute("SELECT * FROM units")
        res = list(self.cur.fetchall())
        return [Unit(id=uuid.UUID(r[0]), name=r[1]) for r in res]
