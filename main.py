from datetime import datetime
from domain.models import Transaction
from infrastructure.transaction_validator_impl import TransactionValidatorImpl
from application.use_cases.validate_transaction import ValidateTransactionUseCase
from domain.exceptions import InvalidTransactionError


def main() -> None:
    # Composition root — aquí se cablea todo
    validator = TransactionValidatorImpl()
    use_case = ValidateTransactionUseCase(validator=validator)

    # Transacción válida
    txn_ok = Transaction(
        id="TXN-001",
        amount=250.0,
        currency="USD",
        timestamp=datetime.now(),
        description="Transferencia internacional",
    )

    # Transacción inválida
    txn_bad = Transaction(
        id="TXN-002",
        amount=-100.0,
        currency="USD",
        timestamp=datetime.now(),
        description="Monto negativo",
    )

    try:
        result = use_case.execute(txn_ok)
        print(f"✓ TXN-001 válida: {result}")
    except InvalidTransactionError as e:
        print(f"✗ Error: {e}")

    try:
        result = use_case.execute(txn_bad)
        print(f"✓ TXN-002 válida: {result}")
    except InvalidTransactionError as e:
        print(f"✗ TXN-002 rechazada: {e}")


if __name__ == "__main__":
    main()
