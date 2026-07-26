import pytest
import numpy as np
from binomial_pricer.payoffs import Payoff, EuropeanCall, EuropeanPut, Forward

def test_payoff_abc_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Payoff()

class TestEuropeanCall:
    def test_in_the_money(self):
        assert EuropeanCall(strike=5.0).compute(np.array([4.0, 8.0])) == 3.0
    def test_out_of_the_money(self):
        assert EuropeanCall(strike=5.0).compute(np.array([4.0, 2.0])) == 0.0

class TestEuropeanPut:
    def test_in_the_money(self):
        assert EuropeanPut(strike=5.0).compute(np.array([4.0, 2.0])) == 3.0
    def test_out_of_the_money(self):
        assert EuropeanPut(strike=5.0).compute(np.array([4.0, 8.0])) == 0.0

class TestForward:
    def test_can_be_negative(self):
        """A diferencia de call/put, el forward no tiene floor en cero."""
        assert Forward(delivery_price=5.0).compute(np.array([4.0, 2.0])) == -3.0
    def test_can_be_positive(self):
        assert Forward(delivery_price=5.0).compute(np.array([4.0, 8.0])) == 3.0