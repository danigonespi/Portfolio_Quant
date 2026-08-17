import pytest
import numpy as np
from binomial_pricer.equity_model import BinomialStockModel

class TestNoArbitrageValidation:
    def test_rejects_non_positive_S0(self):
        with pytest.raises(ValueError, match="s0"):
            BinomialStockModel(s0=0.0, u=2.0, d=0.5, r=0.25)

    def test_rejects_non_positive_d(self):
        with pytest.raises(ValueError, match="d must be strictly positive"):
            BinomialStockModel(s0=4.0, u=2.0, d=0.0, r=0.25)

    def test_rejects_d_geq_1_plus_r(self):
        """Exercise 1.1: violates d < 1+r."""
        with pytest.raises(ValueError, match=r"d \(1\.5\) >= 1\+r \(1\.25\)"):
            BinomialStockModel(s0=4.0, u=2.0, d=1.5, r=0.25)

    def test_rejects_1_plus_r_geq_u(self):
        """Exercise 1.1: violates 1+r < u."""
        with pytest.raises(ValueError, match=r"1\+r \(1\.25\) >= u \(1\.1\)"):
            BinomialStockModel(s0=4.0, u=1.1, d=0.5, r=0.25)

    def test_boundary_d_equals_1_plus_r_still_raises(self):
        """Strict equality must also be rejected -- (1.1.2) requires '<', not '<='."""
        with pytest.raises(ValueError):
            BinomialStockModel(s0=4.0, u=2.0, d=1.25, r=0.25)


class TestImmutability:
    def test_model_cannot_be_mutated_after_construction(self, base_model):
        """Without frozen=True, the post_init validation can be bypassed by reassigning an attribute after object construction -- see review."""
        with pytest.raises(Exception):
            base_model.u = 1.0


class TestRiskNeutralProbability:
    def test_matches_example_1_1_1(self, base_model):
        p_tilde, q_tilde = base_model.risk_neutral_prob
        assert p_tilde == pytest.approx(0.5)
        assert q_tilde == pytest.approx(0.5)

    def test_p_and_q_always_sum_to_one(self, base_model):
        """Algebraic identity of (1.1.8): p̃+q̃=1 for any valid u,d,r."""
        p_tilde, q_tilde = base_model.risk_neutral_prob
        assert p_tilde + q_tilde == pytest.approx(1.0)


class TestStockPrices:
    def test_s1_h_and_s1_t(self, base_model):
        assert base_model.s1_h == pytest.approx(8.0)
        assert base_model.s1_t == pytest.approx(2.0)

class TestPricePath:
    def test_price_path_hth_example_1_2_4(self, base_model):
        path = base_model.price_path("HTH")
        np.testing.assert_array_almost_equal(path, [4.0, 8.0, 4.0, 8.0])

    def test_price_path_length(self, base_model):
        seq = "HHTT"
        path = base_model.price_path(seq)
        assert len(path) == len(seq) + 1