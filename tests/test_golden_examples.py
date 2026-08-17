import pytest
from binomial_pricer.equity_model import BinomialStockModel
from binomial_pricer.payoffs import EuropeanCall, LookbackOption, EuropeanPut, AsianOption
from binomial_pricer.engines import PricingEngine, ReducedStateEngine

def test_example_1_1_1(base_model):
    """Example 1.1.1: call strike=5 -> V0=1.20, Delta0=0.5."""
    result = PricingEngine().price(base_model, EuropeanCall(strike=5.0), n_periods=1)
    assert result.v0 == pytest.approx(1.20)
    assert result.delta0 == pytest.approx(0.5)

def test_exercise_1_3_derivative_equals_stock(base_model):
    """Exercise 1.3: V1=S1 (call strike=0) -> V0 must equal s0 exactly."""
    result = PricingEngine().price(base_model, EuropeanCall(strike=0.0), n_periods=1)
    assert result.v0 == pytest.approx(base_model.s0)
    assert result.delta0 == pytest.approx(1.0)

@pytest.mark.parametrize("delta0, gamma0", [(1.0, 1.0), (-2.0, 3.0), (0.5, -1.5), (10.0, -4.0)])
def test_exercise_1_2_no_arbitrage_at_fair_price(delta0, gamma0):
    """
    Exercise 1.2: at the fair price 1.20 (which coincides with V0 from Example (1.1.1),
    any portfolio of Delta0 shares + Gamma0 options yields exactly opposite X1(H) and
    X1(T) -- if one is positive the other is negative, never both >= 0 with one > 0.
    Verified for several arbitrary combinations of Delta0, Gamma0, not just one.
    """
    S1_H, S1_T, r, option_price = 8.0, 2.0, 0.25, 1.20
    cash = -4 * delta0 - option_price * gamma0
    X1_H = delta0 * S1_H + gamma0 * max(S1_H - 5, 0) + (1 + r) * cash
    X1_T = delta0 * S1_T + gamma0 * max(S1_T - 5, 0) + (1 + r) * cash
    assert X1_H == pytest.approx(-X1_T)
    assert not (X1_H > 1e-9 and X1_T >= -1e-9)
    assert not (X1_T > 1e-9 and X1_H >= -1e-9)

def test_example_1_2_4_lookback_option(base_model):
    """Exact values from Example 1.2.4 (Multi-period Lookback option)."""
    payoff = LookbackOption()
    result = PricingEngine().price(base_model, payoff, n_periods=3)

    assert result.value_grid["HHH"] == pytest.approx(0.0)
    assert result.value_grid["HHT"] == pytest.approx(8.0)
    assert result.value_grid["HTH"] == pytest.approx(0.0)
    assert result.value_grid["HTT"] == pytest.approx(6.0)
    assert result.value_grid["THH"] == pytest.approx(0.0)
    assert result.value_grid["THT"] == pytest.approx(2.0)
    assert result.value_grid["TTH"] == pytest.approx(2.0)
    assert result.value_grid["TTT"] == pytest.approx(3.50)

    assert result.value_grid["HH"] == pytest.approx(3.20)
    assert result.value_grid["HT"] == pytest.approx(2.40)
    assert result.value_grid["TH"] == pytest.approx(0.80)
    assert result.value_grid["TT"] == pytest.approx(2.20)

    assert result.value_grid["H"] == pytest.approx(2.24)
    assert result.value_grid["T"] == pytest.approx(1.20)

    assert result.v0 == pytest.approx(1.376)
    assert result.delta0 == pytest.approx(0.1733, abs=1e-3)

def test_example_1_3_1_put_state_reduction(base_model):
    """Exact values from Example 1.3.1 using state reduction v_n(s)."""
    payoff = EuropeanPut(strike=5.0)
    result = ReducedStateEngine().price(base_model, payoff, n_periods=3)

    assert result.value_grid[(3, 32.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 8.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 2.0)] == pytest.approx(3.0)
    assert result.value_grid[(3, 0.5)] == pytest.approx(4.50)

    assert result.value_grid[(0, 4.0)] == pytest.approx(0.864)

def test_example_1_3_2_lookback_state_reduction(base_model):
    """Exact values from Example 1.3.2 using state reduction v_n(s, m)."""
    payoff = LookbackOption()
    result = ReducedStateEngine().price(base_model, payoff, n_periods=3)

    assert result.value_grid[(3, 32.0, 32.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 8.0, 16.0)] == pytest.approx(8.0)
    assert result.value_grid[(3, 8.0, 8.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 2.0, 8.0)] == pytest.approx(6.0)
    assert result.value_grid[(3, 2.0, 4.0)] == pytest.approx(2.0)
    assert result.value_grid[(3, 0.5, 4.0)] == pytest.approx(3.50)
    assert result.value_grid[(0, 4.0, 4.0)] == pytest.approx(1.376)

def test_exercise_1_8_asian_option_state_reduction(base_model):
    """
    Exact values from Exercise 1.8 (Asian option).
    Validates that both the brute force engine and the state reduction engine
    converge to the same V0 of 1.216 using a running sum aggregate.
    """
    payoff = AsianOption(strike=4.0, n_periods=3)
    
    res_brute = PricingEngine().price(base_model, payoff, n_periods=3)
    res_reduced = ReducedStateEngine().price(base_model, payoff, n_periods=3)
    
    expected_v0 = 1.216
    
    assert res_brute.v0 == pytest.approx(expected_v0)
    assert res_reduced.v0 == pytest.approx(expected_v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)