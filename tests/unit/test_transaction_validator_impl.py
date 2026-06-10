from datetime import datetime
from domain.models import Transaction
from infrastructure.transaction_validator_impl import TransactionValidatorImpl


def test_impl_retorna_true_para_transaccion_valida(make_transaction):
    validator = TransactionValidatorImpl()
    txn = make_transaction()
    assert validator.validate(txn) is True


def test_impl_retorna_false_para_monto_cero(make_transaction):
    validator = TransactionValidatorImpl()
    txn = make_transaction(amount=0)
    assert validator.validate(txn) is False


def test_impl_retorna_false_para_monto_negativo(make_transaction):
    validator = TransactionValidatorImpl()
    txn = make_transaction(amount=-50.0)
    assert validator.validate(txn) is False