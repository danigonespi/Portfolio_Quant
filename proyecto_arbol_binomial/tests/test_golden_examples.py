import pytest
from binomial_pricer.equity_model import BinomialStockModel
from binomial_pricer.payoffs import EuropeanCall, LookbackOption, EuropeanPut, AsianOption
from binomial_pricer.engines import PricingEngine, ReducedStateEngine

def test_example_1_1_1(one_period_model):
    """Ejemplo 1.1.1: call strike=5 -> V0=1.20, Delta0=0.5."""
    result = PricingEngine().price(one_period_model, EuropeanCall(strike=5.0), n_periods=1)
    assert result.v0 == pytest.approx(1.20)
    assert result.delta0 == pytest.approx(0.5)

def test_exercise_1_3_derivative_equals_stock(one_period_model):
    """Ejercicio 1.3: V1=S1 (call strike=0) -> V0 debe igualar S0 exactamente."""
    result = PricingEngine().price(one_period_model, EuropeanCall(strike=0.0), n_periods=1)
    assert result.v0 == pytest.approx(one_period_model.S0)
    assert result.delta0 == pytest.approx(1.0)

@pytest.mark.parametrize("delta0, gamma0", [(1.0, 1.0), (-2.0, 3.0), (0.5, -1.5), (10.0, -4.0)])
def test_exercise_1_2_no_arbitrage_at_fair_price(delta0, gamma0):
    """Ejercicio 1.2: al precio justo 1.20 (que coincide con V0 del Ejemplo
    1.1.1), cualquier cartera Delta0 acciones + Gamma0 opciones da X1(H) y
    X1(T) exactamente opuestos -- si uno es positivo el otro es negativo,
    nunca ambos >= 0 con alguno > 0. Se verifica para varias combinaciones
    arbitrarias de Delta0, Gamma0, no solo una."""
    S1_H, S1_T, r, option_price = 8.0, 2.0, 0.25, 1.20
    cash = -4 * delta0 - option_price * gamma0
    X1_H = delta0 * S1_H + gamma0 * max(S1_H - 5, 0) + (1 + r) * cash
    X1_T = delta0 * S1_T + gamma0 * max(S1_T - 5, 0) + (1 + r) * cash
    assert X1_H == pytest.approx(-X1_T)
    assert not (X1_H > 1e-9 and X1_T >= -1e-9)
    assert not (X1_T > 1e-9 and X1_H >= -1e-9)

def test_example_1_2_4_lookback_option():
    """Valores dorados exactos del Ejemplo 1.2.4 (Lookback option multiperíodo)."""
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    payoff = LookbackOption()
    result = PricingEngine().price(model, payoff, n_periods=3)

    # V3 (Valores Terminales)
    assert result.value_grid["HHH"] == pytest.approx(0.0)
    assert result.value_grid["HHT"] == pytest.approx(8.0)
    assert result.value_grid["HTH"] == pytest.approx(0.0)
    assert result.value_grid["HTT"] == pytest.approx(6.0)
    assert result.value_grid["THH"] == pytest.approx(0.0)
    assert result.value_grid["THT"] == pytest.approx(2.0)
    assert result.value_grid["TTH"] == pytest.approx(2.0)
    assert result.value_grid["TTT"] == pytest.approx(3.50)

    # V2
    assert result.value_grid["HH"] == pytest.approx(3.20)
    assert result.value_grid["HT"] == pytest.approx(2.40)
    assert result.value_grid["TH"] == pytest.approx(0.80)
    assert result.value_grid["TT"] == pytest.approx(2.20)

    # V1
    assert result.value_grid["H"] == pytest.approx(2.24)
    assert result.value_grid["T"] == pytest.approx(1.20)

    # V0 y Delta0
    assert result.v0 == pytest.approx(1.376)
    assert result.delta0 == pytest.approx(0.1733, abs=1e-3)

def test_example_1_3_1_put_state_reduction():
    """Valores dorados exactos del Ejemplo 1.3.1 usando reducción de estados v_n(s)."""
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    payoff = EuropeanPut(strike=5.0)
    result = ReducedStateEngine().price(model, payoff, n_periods=3)

    assert result.value_grid[(3, 32.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 8.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 2.0)] == pytest.approx(3.0)
    assert result.value_grid[(3, 0.5)] == pytest.approx(4.50)

    assert result.value_grid[(0, 4.0)] == pytest.approx(0.864)

def test_example_1_3_2_lookback_state_reduction():
    """Valores dorados exactos del Ejemplo 1.3.2 usando reducción de estados v_n(s, m)."""
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    payoff = LookbackOption()
    result = ReducedStateEngine().price(model, payoff, n_periods=3)

    assert result.value_grid[(3, 32.0, 32.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 8.0, 16.0)] == pytest.approx(8.0)
    assert result.value_grid[(3, 8.0, 8.0)] == pytest.approx(0.0)
    assert result.value_grid[(3, 2.0, 8.0)] == pytest.approx(6.0)
    assert result.value_grid[(3, 2.0, 4.0)] == pytest.approx(2.0)
    assert result.value_grid[(3, 0.5, 4.0)] == pytest.approx(3.50)
    assert result.value_grid[(0, 4.0, 4.0)] == pytest.approx(1.376)

def test_exercise_1_8_asian_option_state_reduction():
    """Valores dorados exactos del Ejercicio 1.8 (Asian option).
    Valida que tanto el motor de fuerza bruta como el de reducción de estados
    convergen al mismo V0 de 1.216 usando un agregado de suma corriente."""
    model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
    payoff = AsianOption(strike=4.0, n_periods=3)
    
    res_brute = PricingEngine().price(model, payoff, n_periods=3)
    res_reduced = ReducedStateEngine().price(model, payoff, n_periods=3)
    
    expected_v0 = 1.216
    
    assert res_brute.v0 == pytest.approx(expected_v0)
    assert res_reduced.v0 == pytest.approx(expected_v0)
    assert res_reduced.delta0 == pytest.approx(res_brute.delta0)