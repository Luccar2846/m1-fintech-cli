from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    id: str
    amount: float
    currency: str
    timestamp: datetime
    description: str

    def is_valid(self) -> bool:
        return (
            len(self.id) > 0
            and self.amount > 0
            and len(self.currency) == 3
        )