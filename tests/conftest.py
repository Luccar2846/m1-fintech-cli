import pytest
from datetime import datetime
from domain.models import Transaction


@pytest.fixture
def make_transaction():
    """Factory fixture — disponible en todos los tests sin importar."""
    def _factory(**overrides) -> Transaction:
        defaults = {
            "id": "TXN-001",
            "amount": 100.0,
            "currency": "USD",
            "timestamp": datetime.now(),
            "description": "Pago de prueba",
        }
        return Transaction(**{**defaults, **overrides})
    return _factory