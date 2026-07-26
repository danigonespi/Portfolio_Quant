import pytest
from binomial_pricer.equity_model import BinomialStockModel

@pytest.fixture
def one_period_model():
    """Modelo del Ejemplo 1.1.1: S0=4, u=2, d=0.5, r=0.25 -> p̃=q̃=0.5."""
    return BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)