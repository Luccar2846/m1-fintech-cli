from domain.models import Transaction
from domain.exceptions import InvalidTransactionError
from application.ports.transaction_validator import TransactionValidatorPort


class ValidateTransactionUseCase:
    """Caso de uso: orquesta el dominio y el puerto.
    No sabe nada de infrastructure — solo coordina."""

    def __init__(self, validator: TransactionValidatorPort) -> None:
        self.validator = validator

    def execute(self, transaction: Transaction) -> bool:
        if not self.validator.validate(transaction):
            raise InvalidTransactionError(
                f"Transacción {transaction.id} no pasó la validación."
            )
        return True