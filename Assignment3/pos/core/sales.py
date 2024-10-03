from dataclasses import dataclass


@dataclass
class Sales:
    n_receipts: int = 0
    revenue: float = 0

    def get_n_receipts(self) -> int:
        return self.n_receipts

    def get_revenue(self) -> float:
        return self.revenue

    def add_revenue(self, revenue: float) -> None:
        self.revenue += revenue

    def add_receipt(self) -> None:
        self.n_receipts += 1
