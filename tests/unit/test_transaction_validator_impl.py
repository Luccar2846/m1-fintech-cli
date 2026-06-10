from datetime import datetime
from domain.models import Transaction
from infrastructure.transaction_validator_impl import TransactionValidatorImpl


def make_transaction(**overrides) -> Transaction:
    defaults = {
        "id": "TXN-001",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": datetime.now(),
        "description": "Pago de prueba",
    }
    return Transaction(**{**defaults, **overrides})


def test_impl_retorna_true_para_transaccion_valida():
    validator = TransactionValidatorImpl()
    txn = make_transaction()
    assert validator.validate(txn) is True


def test_impl_retorna_false_para_monto_cero():
    validator = TransactionValidatorImpl()
    txn = make_transaction(amount=0)
    assert validator.validate(txn) is False


def test_impl_retorna_false_para_monto_negativo():
    validator = TransactionValidatorImpl()
    txn = make_transaction(amount=-50.0)
    assert validator.validate(txn) is False