import numpy as np
from typing import Tuple
from .equity_model import BinomialStockModel
from .payoffs import Payoff

class PricingEngine:
    def price(self, model: BinomialStockModel, payoff: Payoff) -> Tuple[float, float]:
        """
        Calcula el precio libre de arbitraje en t=0 y la cobertura inicial.
        Devuelve (V0, Δ0).
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.9) para Δ0, Eq. (1.1.10) para V0.
        """
        path_h = np.array([model.S0, model.s1_h])
        path_t = np.array([model.S0, model.s1_t])
        
        v1_h = payoff.compute(path_h)
        v1_t = payoff.compute(path_t)
        
        p_tilde, q_tilde = model.risk_neutral_prob
        
        # Cálculo de la cantidad de acciones (delta) en el portafolio replicante
        # Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.9).
        delta_0 = (v1_h - v1_t) / (model.s1_h - model.s1_t)
        
        # Implementa la fórmula de valoración neutral al riesgo.
        # Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.10).
        v_0 = (1 / (1 + model.r)) * (p_tilde * v1_h + q_tilde * v1_t)
        
        return v_0, delta_0