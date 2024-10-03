from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Unit:
    name: str
    id: UUID = field(default_factory=uuid4)

    def get_id(self) -> UUID:
        return self.id

    def get_name(self) -> str:
        return self.name


class UnitRepository(Protocol):
    def create(self, unit: Unit) -> None:
        pass

    def read_one(self, unit_id: UUID) -> Unit:
        pass

    def list(self) -> list[Unit]:
        pass
