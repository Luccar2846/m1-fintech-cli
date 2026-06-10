from datetime import datetime
from domain.models import Transaction
from domain.exceptions import InvalidTransactionError


def test_transaction_valida(make_transaction):
    txn = make_transaction()
    assert txn.is_valid() is True


def test_transaction_monto_cero_es_invalida(make_transaction):
    txn = make_transaction(amount=0)
    assert txn.is_valid() is False


def test_transaction_monto_negativo_es_invalida(make_transaction):
    txn = make_transaction(amount=-50.0)
    assert txn.is_valid() is False


def test_transaction_id_vacio_es_invalida(make_transaction):
    txn = make_transaction(id="")
    assert txn.is_valid() is False


def test_transaction_currency_invalida(make_transaction):
    txn = make_transaction(currency="DOLAR")
    assert txn.is_valid() is False

