from abc import ABC, abstractmethod
from domain.models import Transaction


class TransactionValidatorPort(ABC):
    """Puerto: contrato que define QUÉ necesita la aplicación.
    No sabe CÓMO se implementa — eso es trabajo de infrastructure."""

    @abstractmethod
    def validate(self, transaction: Transaction) -> bool:
        raise NotImplementedError