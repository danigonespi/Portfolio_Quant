import pytest
import numpy as np
from binomial_pricer.equity_model import BinomialStockModel
from binomial_pricer.payoffs import EuropeanCall, LookbackOption, EuropeanPut
from binomial_pricer.engines import PricingEngine, ReducedStateEngine

def test_v0_differs_from_naive_real_world_expectation(one_period_model):
    """V0 (bajo p̃,q̃, Eq. 1.1.10) debe diferir de la esperanza descontada
    bajo una probabilidad real p arbitraria."""
    call = EuropeanCall(strike=5.0)
    engine = PricingEngine()
    result = engine.price(one_period_model, call, n_periods=1)

    p_real = 0.7
    v1_h = call.compute(np.array([4.0, one_period_model.s1_h]))
    v1_t = call.compute(np.array([4.0, one_period_model.s1_t]))
    naive_expectation = (1 / (1 + one_period_model.r)) * (p_real * v1_h + (1 - p_real) * v1_t)
    assert result.v0 != pytest.approx(naive_expectation)

def test_engine_price_matches_manual_formula(one_period_model):
    """Confirma que price() aplica (1.1.9)/(1.1.10) para cualquier payoff."""
    from binomial_pricer.payoffs import EuropeanPut
    put = EuropeanPut(strike=5.0)
    engine = PricingEngine()
    result = engine.price(one_period_model, put, n_periods=1)

    v1_h = put.compute(np.array([4.0, one_period_model.s1_h]))
    v1_t = put.compute(np.array([4.0, one_period_model.s1_t]))
    p_tilde, q_tilde = one_period_model.risk_neutral_prob
    expected_delta0 = (v1_h - v1_t) / (one_period_model.s1_h - one_period_model.s1_t)
    expected_v0 = (1 / (1 + one_period_model.r)) * (p_tilde * v1_h + q_tilde * v1_t)

    assert result.delta0 == pytest.approx(expected_delta0)
    assert result.v0 == pytest.approx(expected_v0)

def test_exercise_1_6_hedging_long_position(one_period_model):
    """Ejercicio 1.6: cobertura de posición larga invierte las deltas."""
    call = EuropeanCall(strike=5.0)
    engine = PricingEngine()
    res_short = engine.price(one_period_model, call, n_periods=1, position="short")
    res_long = engine.price(one_period_model, call, n_periods=1, position="long")
    
    assert res_long.delta_grid[""] == pytest.approx(-res_short.delta_grid[""])

def test_exercise_1_7_hedging_long_multiple_periods():
    """Ejercicio 1.7: cobertura de lookback invierte las deltas en todo el árbol."""
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    payoff = LookbackOption()
    engine = PricingEngine()
    
    res_short = engine.price(model, payoff, n_periods=3, position="short")
    res_long = engine.price(model, payoff, n_periods=3, position="long")
    
    for prefix in res_short.delta_grid:
        assert res_long.delta_grid[prefix] == pytest.approx(-res_short.delta_grid[prefix])

def test_cross_validation_reduced_vs_brute_force_one_period(one_period_model):
    call = EuropeanCall(strike=5.0)
    res_brute = PricingEngine().price(one_period_model, call, n_periods=1)
    res_reduced = ReducedStateEngine().price(one_period_model, call, n_periods=1)
    
    assert res_reduced.v0 == pytest.approx(res_brute.v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)

def test_cross_validation_reduced_vs_brute_force_lookback():
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    payoff = LookbackOption()
    res_brute = PricingEngine().price(model, payoff, n_periods=3)
    res_reduced = ReducedStateEngine().price(model, payoff, n_periods=3)
    
    assert res_reduced.v0 == pytest.approx(res_brute.v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)

def test_cross_validation_reduced_vs_brute_force_put():
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    put = EuropeanPut(strike=5.0)
    res_brute = PricingEngine().price(model, put, n_periods=3)
    res_reduced = ReducedStateEngine().price(model, put, n_periods=3)
    
    assert res_reduced.v0 == pytest.approx(res_brute.v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)

def test_reduced_engine_long_position_inverts_delta(one_period_model):
    call = EuropeanCall(strike=5.0)
    res_short = ReducedStateEngine().price(one_period_model, call, n_periods=1, position="short")
    res_long = ReducedStateEngine().price(one_period_model, call, n_periods=1, position="long")
    
    # Comprobamos en el nodo raíz de la reducción (0, S0)
    assert res_long.delta_grid[(0, one_period_model.S0)] == pytest.approx(-res_short.delta_grid[(0, one_period_model.S0)])