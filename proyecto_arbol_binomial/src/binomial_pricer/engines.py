import numpy as np
from typing import Dict, Literal, Any
from dataclasses import dataclass, field
from .equity_model import BinomialStockModel
from .payoffs import Payoff, PathDependentPayoff
from .lattice import RecombiningLattice

@dataclass
class PricingResult:
    v0: float
    delta0: float
    value_grid: Dict[Any, float] = field(default_factory=dict)
    delta_grid: Dict[Any, float] = field(default_factory=dict)

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

class ReducedStateEngine:
    @staticmethod
    def _combine_backward(v_up: float, v_down: float, s: float, model: BinomialStockModel,
                           p_tilde: float, q_tilde: float, position: str):
        """Un paso de inducción hacia atrás sobre estado reducido: aplica la
        fórmula de v_n (Eq. 1.3.1 generalizada) y de Delta_n (fórmula
        canónica sin numerar, Sección 1.3). Compartido por ambas ramas de
        price() -- solo cambia cómo se construye la clave del estado,
        nunca la fórmula en sí."""
        v_n = (1 / (1 + model.r)) * (p_tilde * v_up + q_tilde * v_down)
        delta_n = (v_up - v_down) / ((model.u - model.d) * s)
        if position == "long":
            delta_n = -delta_n
        return v_n, delta_n
    
    def price(self, model: BinomialStockModel, payoff: Payoff, n_periods: int,
              position: Literal["short", "long"] = "short") -> PricingResult:
        """
        Calcula el precio libre de arbitraje y la cobertura mediante la reducción
        del espacio de estados (Sección 1.3).
        
        Aplica la Eq. (1.3.1) para la recursión del valor neutral al riesgo,
        generalizada mediante las fórmulas algorítmicas canónicas sin numerar
        para v_n(s) y Delta_n(s) (opciones independientes de trayectoria), 
        y v_n(s, m) y Delta_n(s, m) (opciones dependientes de trayectoria).
        """
        value_grid = {}
        delta_grid = {}
        p_tilde, q_tilde = model.risk_neutral_prob

        if isinstance(payoff, PathDependentPayoff):
            lattice = RecombiningLattice(n_periods)
            states_by_level = {n: set() for n in range(n_periods + 1)}
            
            for seq in lattice.enumerate_paths():
                s = model.S0
                m = payoff.initial_aggregate(s)
                states_by_level[0].add((s, m))
                for n, coin in enumerate(seq):
                    s = s * model.u if coin == 'H' else s * model.d
                    m = payoff.update_aggregate(m, s)
                    states_by_level[n + 1].add((s, m))
            
            for s, m in states_by_level[n_periods]:
                value_grid[(n_periods, s, m)] = payoff.terminal_value(s, m)
                
            for n in range(n_periods - 1, -1, -1):
                for s, m in states_by_level[n]:
                    s_up = s * model.u
                    m_up = payoff.update_aggregate(m, s_up)
                    s_down = s * model.d
                    m_down = payoff.update_aggregate(m, s_down)
                    
                    v_n, delta_n = self._combine_backward(value_grid[(n+1, s_up, m_up)], value_grid[(n+1, s_down, m_down)],s, model, p_tilde, q_tilde, position)
                    value_grid[(n, s, m)] = v_n
                    delta_grid[(n, s, m)] = delta_n
                    
            v0 = value_grid.get((0, model.S0, payoff.initial_aggregate(model.S0)), 0.0)
            delta0 = delta_grid.get((0, model.S0, payoff.initial_aggregate(model.S0)), 0.0)
            
        else:
            for k in range(n_periods + 1):
                s = model.price_path("H" * k + "T" * (n_periods - k))[-1]
                value_grid[(n_periods, s)] = payoff.compute(np.array([s]))
                
            for n in range(n_periods - 1, -1, -1):
                for k in range(n + 1):
                    s = model.price_path("H" * k + "T" * (n - k))[-1]
                    s_up = model.price_path("H" * (k + 1) + "T" * (n - k))[-1]
                    s_down = model.price_path("H" * k + "T" * (n - k + 1))[-1]
                    
                    v_n, delta_n = self._combine_backward(value_grid[(n+1, s_up)], value_grid[(n+1, s_down)], s, model, p_tilde, q_tilde, position)
                    value_grid[(n, s)] = v_n
                    delta_grid[(n, s)] = delta_n
                    
            v0 = value_grid.get((0, model.S0), 0.0)
            delta0 = delta_grid.get((0, model.S0), 0.0)

        return PricingResult(v0=v0, delta0=delta0, value_grid=value_grid, delta_grid=delta_grid)        