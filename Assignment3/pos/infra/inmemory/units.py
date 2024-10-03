from dataclasses import dataclass, field
from uuid import UUID

from pos.core.errors import DoesNotExistError, ExistsError
from pos.core.units import Unit


@dataclass
class UnitsInMemory:
    units: dict[UUID, Unit] = field(default_factory=dict)

    def create(self, unit: Unit) -> None:
        for un in self.units.values():
            if unit.get_name() == un.get_name():
                raise ExistsError(unit.get_name())
        self.units[unit.id] = unit

    def read_one(self, unit_id: UUID) -> Unit:
        try:
            return self.units[unit_id]
        except KeyError:
            raise DoesNotExistError(unit_id)

    def list(self) -> list[Unit]:
        return list(self.units.values())
