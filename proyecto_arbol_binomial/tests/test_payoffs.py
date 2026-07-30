import pytest
import numpy as np
from binomial_pricer.payoffs import Payoff, EuropeanCall, EuropeanPut, Forward, LookbackOption, PathDependentPayoff, AsianOption

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
        assert Forward(delivery_price=5.0).compute(np.array([4.0, 2.0])) == -3.0
    def test_can_be_positive(self):
        assert Forward(delivery_price=5.0).compute(np.array([4.0, 8.0])) == 3.0

class TestLookbackOption:
    def test_compute_manual_path_htt(self):
        """V3(HTT) del Ejemplo 1.2.4 evaluado de forma aislada."""
        payoff = LookbackOption()
        path = np.array([4.0, 8.0, 4.0, 2.0])
        assert payoff.compute(path) == 6.0

class TestPathDependentPayoffHooks:
    def test_hooks_called_in_correct_order(self):
        class DummyPayoff(PathDependentPayoff):
            def initial_aggregate(self, s0: float) -> float:
                self.init_called = True
                return s0
                
            def update_aggregate(self, aggregate: float, s_next: float) -> float:
                self.update_called = True
                return aggregate + s_next
                
            def terminal_value(self, s_final: float, aggregate_final: float) -> float:
                self.terminal_called = True
                return aggregate_final * s_final

        dummy = DummyPayoff()
        path = np.array([2.0, 3.0])
        res = dummy.compute(path)
        
        assert getattr(dummy, "init_called", False)
        assert getattr(dummy, "update_called", False)
        assert getattr(dummy, "terminal_called", False)
        assert res == 15.0  # (2.0 + 3.0) * 3.0 = 15.0

class TestAsianOption:
    def test_compute_manual_path_hth(self):
        """Trayectoria manual HTH aislada: S=[4, 8, 4, 8], Y_3=24. Payoff = max(24/4 - 4, 0) = 2.0."""
        payoff = AsianOption(strike=4.0, n_periods=3)
        path = np.array([4.0, 8.0, 4.0, 8.0])
        assert payoff.compute(path) == 2.0