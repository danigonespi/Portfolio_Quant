import pytest
import numpy as np
from binomial_pricer.equity_model import BinomialStockModel
from binomial_pricer.payoffs import EuropeanCall
from binomial_pricer.engines import PricingEngine

def test_v0_differs_from_naive_real_world_expectation(one_period_model):
    """V0 (bajo p̃,q̃, Eq. 1.1.10) debe diferir de la esperanza descontada
    bajo una probabilidad real p arbitraria -- demuestra computacionalmente
    que el precio no es una esperanza genérica, sino específicamente bajo
    la medida neutral al riesgo."""
    call = EuropeanCall(strike=5.0)
    engine = PricingEngine()
    v0, _ = engine.price(one_period_model, call)

    p_real = 0.7  # arbitraria, distinta de p̃=0.5
    v1_h = call.compute(np.array([4.0, one_period_model.s1_h]))
    v1_t = call.compute(np.array([4.0, one_period_model.s1_t]))
    naive_expectation = (1 / (1 + one_period_model.r)) * (p_real * v1_h + (1 - p_real) * v1_t)
    assert v0 != pytest.approx(naive_expectation)

def test_engine_price_matches_manual_formula(one_period_model):
    """Test de caracterización, no de valor dorado: confirma que price()
    aplica exactamente (1.1.9) y (1.1.10) para CUALQUIER payoff, no solo
    para el call del Ejemplo 1.1.1."""
    from binomial_pricer.payoffs import EuropeanPut
    put = EuropeanPut(strike=5.0)
    engine = PricingEngine()
    v0, delta0 = engine.price(one_period_model, put)

    v1_h = put.compute(np.array([4.0, one_period_model.s1_h]))  # = 0.0
    v1_t = put.compute(np.array([4.0, one_period_model.s1_t]))  # = 3.0
    p_tilde, q_tilde = one_period_model.risk_neutral_prob

    expected_delta0 = (v1_h - v1_t) / (one_period_model.s1_h - one_period_model.s1_t)
    expected_v0 = (1 / (1 + one_period_model.r)) * (p_tilde * v1_h + q_tilde * v1_t)

    assert delta0 == pytest.approx(expected_delta0)
    assert v0 == pytest.approx(expected_v0)