import pytest
import numpy as np
import time
from binomial_pricer.equity_model import BinomialStockModel
from binomial_pricer.payoffs import EuropeanCall, LookbackOption, EuropeanPut, AsianOption
from binomial_pricer.engines import PricingEngine, ReducedStateEngine

def test_v0_differs_from_naive_real_world_expectation(base_model):
    """V0 (under p̃,q̃, Eq. 1.1.10) must differ from the discounted expectation under an arbitrary real probability p."""
    call = EuropeanCall(strike=5.0)
    engine = PricingEngine()
    result = engine.price(base_model, call, n_periods=1)

    p_real = 0.7
    v1_h = call.compute(np.array([4.0, base_model.s1_h]))
    v1_t = call.compute(np.array([4.0, base_model.s1_t]))
    naive_expectation = (1 / (1 + base_model.r)) * (p_real * v1_h + (1 - p_real) * v1_t)
    assert result.v0 != pytest.approx(naive_expectation)

def test_engine_price_matches_manual_formula(base_model):
    """Confirms that price() applies (1.1.9)/(1.1.10) for any payoff."""
    from binomial_pricer.payoffs import EuropeanPut
    put = EuropeanPut(strike=5.0)
    engine = PricingEngine()
    result = engine.price(base_model, put, n_periods=1)

    v1_h = put.compute(np.array([4.0, base_model.s1_h]))
    v1_t = put.compute(np.array([4.0, base_model.s1_t]))
    p_tilde, q_tilde = base_model.risk_neutral_prob
    expected_delta0 = (v1_h - v1_t) / (base_model.s1_h - base_model.s1_t)
    expected_v0 = (1 / (1 + base_model.r)) * (p_tilde * v1_h + q_tilde * v1_t)

    assert result.delta0 == pytest.approx(expected_delta0)
    assert result.v0 == pytest.approx(expected_v0)

def test_exercise_1_6_hedging_long_position(base_model):
    """Exercise 1.6: hedging a long position inverts the deltas."""
    call = EuropeanCall(strike=5.0)
    engine = PricingEngine()
    res_short = engine.price(base_model, call, n_periods=1, position="short")
    res_long = engine.price(base_model, call, n_periods=1, position="long")
    
    assert res_long.delta_grid[""] == pytest.approx(-res_short.delta_grid[""])

def test_exercise_1_7_hedging_long_multiple_periods(base_model):
    """Exercise 1.7: lookback hedging inverts the deltas throughout the tree."""
    payoff = LookbackOption()
    engine = PricingEngine()
    
    res_short = engine.price(base_model, payoff, n_periods=3, position="short")
    res_long = engine.price(base_model, payoff, n_periods=3, position="long")
    
    for prefix in res_short.delta_grid:
        assert res_long.delta_grid[prefix] == pytest.approx(-res_short.delta_grid[prefix])

def test_cross_validation_reduced_vs_brute_force_one_period(base_model):
    call = EuropeanCall(strike=5.0)
    res_brute = PricingEngine().price(base_model, call, n_periods=1)
    res_reduced = ReducedStateEngine().price(base_model, call, n_periods=1)
    
    assert res_reduced.v0 == pytest.approx(res_brute.v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)

def test_cross_validation_reduced_vs_brute_force_lookback(base_model):
    payoff = LookbackOption()
    res_brute = PricingEngine().price(base_model, payoff, n_periods=3)
    res_reduced = ReducedStateEngine().price(base_model, payoff, n_periods=3)
    
    assert res_reduced.v0 == pytest.approx(res_brute.v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)

def test_cross_validation_reduced_vs_brute_force_put(base_model):
    put = EuropeanPut(strike=5.0)
    res_brute = PricingEngine().price(base_model, put, n_periods=3)
    res_reduced = ReducedStateEngine().price(base_model, put, n_periods=3)
    
    assert res_reduced.v0 == pytest.approx(res_brute.v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)

def test_reduced_engine_long_position_inverts_delta(base_model):
    call = EuropeanCall(strike=5.0)
    res_short = ReducedStateEngine().price(base_model, call, n_periods=1, position="short")
    res_long = ReducedStateEngine().price(base_model, call, n_periods=1, position="long")
    
    assert res_long.delta_grid[(0, base_model.s0)] == pytest.approx(-res_short.delta_grid[(0, base_model.s0)])


def test_reduced_engine_computational_complexity_n50(base_model):
    """
    Verifies that the complexity is truly reduced (polynomial).
    LookbackOption is used because its states (s, max) do recombine.
    """
    payoff = LookbackOption()
    
    start_time = time.time()
    result = ReducedStateEngine().price(base_model, payoff, n_periods=50)
    elapsed = time.time() - start_time
    
    assert elapsed < 1.0, f"Fallo de arquitectura: el motor tardó {elapsed}s. Hay una fuga exponencial."
    
    assert result.v0 > 0.0