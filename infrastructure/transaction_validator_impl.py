from domain.models import Transaction
from application.ports.transaction_validator import TransactionValidatorPort


class TransactionValidatorImpl(TransactionValidatorPort):
    """Adaptador concreto — implementa el puerto usando lógica del dominio.
    Infrastructure cumple el contrato que application definió."""

    def validate(self, transaction: Transaction) -> bool:
        return transaction.is_valid()