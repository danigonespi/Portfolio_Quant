import numpy as np
from typing import Dict, Literal
from dataclasses import dataclass, field
from .equity_model import BinomialStockModel
from .payoffs import Payoff
from .lattice import RecombiningLattice

@dataclass
class PricingResult:
    v0: float
    delta0: float
    value_grid: Dict[str, float] = field(default_factory=dict)
    delta_grid: Dict[str, float] = field(default_factory=dict)

class PricingEngine:
    def price(self, model: BinomialStockModel, payoff: Payoff, n_periods: int,
              position: Literal["short", "long"] = "short") -> PricingResult:
        """
        Calcula el precio libre de arbitraje y la cobertura usando inducción hacia atrás.
        El caso recursivo simétrico completo (incluyendo T) se demuestra en el Ejercicio 1.4.
        Utiliza Eq. (1.2.18), Eq. (1.2.16) y Eq. (1.2.17)
        """
        lattice = RecombiningLattice(n_periods)
        value_grid = {}
        delta_grid = {}

        p_tilde, q_tilde = model.risk_neutral_prob
        all_paths = list(lattice.enumerate_paths())

        for seq in all_paths:
            path_prices = model.price_path(seq)
            value_grid[seq] = payoff.compute(path_prices)

        for n in range(n_periods - 1, -1, -1):
            prefixes = set(seq[:n] for seq in all_paths) if n_periods > 0 else {""}
            
            for prefix in prefixes:
                v_next_h = value_grid[prefix + "H"]
                v_next_t = value_grid[prefix + "T"]

                s_next_h = model.price_path(prefix + "H")[-1]
                s_next_t = model.price_path(prefix + "T")[-1]

                v_n = (1 / (1 + model.r)) * (p_tilde * v_next_h + q_tilde * v_next_t)
                value_grid[prefix] = v_n

                delta_n = (v_next_h - v_next_t) / (s_next_h - s_next_t)
                
                if position == "long":
                    delta_n = -delta_n
                    
                delta_grid[prefix] = delta_n

        v0 = value_grid.get("", 0.0)
        delta0 = delta_grid.get("", 0.0)

        return PricingResult(v0=v0, delta0=delta0, value_grid=value_grid, delta_grid=delta_grid)