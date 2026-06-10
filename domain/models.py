from dataclasses import dataclass
from datetime import datetime

CURRENCY_CODE_LENGTH = 3


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
            and len(self.currency) == CURRENCY_CODE_LENGTH
        )