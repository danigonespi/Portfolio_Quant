import pytest
import numpy as np
from binomial_pricer.equity_model import BinomialStockModel

class TestNoArbitrageValidation:
    def test_rejects_non_positive_S0(self):
        with pytest.raises(ValueError, match="S0"):
            BinomialStockModel(S0=0.0, u=2.0, d=0.5, r=0.25)

    def test_rejects_non_positive_d(self):
        with pytest.raises(ValueError, match="d debe ser estrictamente positivo"):
            BinomialStockModel(S0=4.0, u=2.0, d=0.0, r=0.25)

    def test_rejects_d_geq_1_plus_r(self):
        """Ejercicio 1.1: viola d < 1+r."""
        with pytest.raises(ValueError, match=r"d \(1\.5\) >= 1\+r \(1\.25\)"):
            BinomialStockModel(S0=4.0, u=2.0, d=1.5, r=0.25)

    def test_rejects_1_plus_r_geq_u(self):
        """Ejercicio 1.1: viola 1+r < u."""
        with pytest.raises(ValueError, match=r"1\+r \(1\.25\) >= u \(1\.1\)"):
            BinomialStockModel(S0=4.0, u=1.1, d=0.5, r=0.25)

    def test_boundary_d_equals_1_plus_r_still_raises(self):
        """Igualdad estricta también debe rechazarse -- (1.1.2) exige '<', no '<='."""
        with pytest.raises(ValueError):
            BinomialStockModel(S0=4.0, u=2.0, d=1.25, r=0.25)


class TestImmutability:
    def test_model_cannot_be_mutated_after_construction(self, one_period_model):
        """Sin frozen=True, la validación de __post_init__ se puede saltar
        reasignando un atributo después de construir el objeto -- ver revisión."""
        with pytest.raises(Exception):
            one_period_model.u = 1.0


class TestRiskNeutralProbability:
    def test_matches_example_1_1_1(self, one_period_model):
        p_tilde, q_tilde = one_period_model.risk_neutral_prob
        assert p_tilde == pytest.approx(0.5)
        assert q_tilde == pytest.approx(0.5)

    def test_p_and_q_always_sum_to_one(self, one_period_model):
        """Identidad algebraica de (1.1.8): p̃+q̃=1 para cualquier u,d,r válidos."""
        p_tilde, q_tilde = one_period_model.risk_neutral_prob
        assert p_tilde + q_tilde == pytest.approx(1.0)


class TestStockPrices:
    def test_s1_h_and_s1_t(self, one_period_model):
        assert one_period_model.s1_h == pytest.approx(8.0)
        assert one_period_model.s1_t == pytest.approx(2.0)

class TestPricePath:
    def test_price_path_hth_example_1_2_4(self):
        model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
        path = model.price_path("HTH")
        np.testing.assert_array_almost_equal(path, [4.0, 8.0, 4.0, 8.0])

    def test_price_path_length(self):
        model = BinomialStockModel(S0=4.0, u=2.0, d=0.5, r=0.25)
        seq = "HHTT"
        path = model.price_path(seq)
        assert len(path) == len(seq) + 1