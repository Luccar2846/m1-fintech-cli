from datetime import datetime
from domain.models import Transaction
from domain.exceptions import InvalidTransactionError


def make_transaction(**overrides) -> Transaction:
    """Factory helper — evita repetir datos en cada test."""
    defaults = {
        "id": "TXN-001",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": datetime.now(),
        "description": "Pago de prueba",
    }
    return Transaction(**{**defaults, **overrides})


def test_transaction_valida():
    txn = make_transaction()
    assert txn.is_valid() is True


def test_transaction_monto_cero_es_invalida():
    txn = make_transaction(amount=0)
    assert txn.is_valid() is False


def test_transaction_monto_negativo_es_invalida():
    txn = make_transaction(amount=-50.0)
    assert txn.is_valid() is False


def test_transaction_id_vacio_es_invalida():
    txn = make_transaction(id="")
    assert txn.is_valid() is False


def test_transaction_currency_invalida():
    txn = make_transaction(currency="DOLAR")
    assert txn.is_valid() is False