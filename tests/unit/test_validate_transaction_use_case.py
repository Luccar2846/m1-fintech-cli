import pytest
from datetime import datetime
from domain.models import Transaction
from domain.exceptions import InvalidTransactionError
from application.ports.transaction_validator import TransactionValidatorPort
from application.use_cases.validate_transaction import ValidateTransactionUseCase


# Mock: implementación falsa del puerto — solo para tests
class ValidatorMockValido(TransactionValidatorPort):
    def validate(self, transaction: Transaction) -> bool:
        return True


class ValidatorMockInvalido(TransactionValidatorPort):
    def validate(self, transaction: Transaction) -> bool:
        return False


def make_transaction() -> Transaction:
    return Transaction(
        id="TXN-001",
        amount=100.0,
        currency="USD",
        timestamp=datetime.now(),
        description="Pago de prueba",
    )


def test_use_case_retorna_true_cuando_transaccion_es_valida():
    use_case = ValidateTransactionUseCase(validator=ValidatorMockValido())
    result = use_case.execute(make_transaction())
    assert result is True


def test_use_case_lanza_excepcion_cuando_transaccion_es_invalida():
    use_case = ValidateTransactionUseCase(validator=ValidatorMockInvalido())
    with pytest.raises(InvalidTransactionError):
        use_case.execute(make_transaction())