import numpy as np
from typing import Dict, Literal, Any, Tuple, Union
from dataclasses import dataclass, field
from .equity_model import BinomialStockModel
from .payoffs import Payoff
from .lattice import RecombiningLattice

StateKey = Union[Tuple[int, float], Tuple[int, float, Any]]

@dataclass
class PricingResult:
    v0: float
    delta0: float
    value_grid: Dict[StateKey, float] = field(default_factory=dict)
    delta_grid: Dict[StateKey, float] = field(default_factory=dict)

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

                current_s = model.price_path(prefix)[-1] if prefix else model.S0
                s_next_h = current_s * model.u
                s_next_t = current_s * model.d

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

        # Tubería algorítmica universal (Opciones estándar y Path-Dependent)
        states_by_level = {n: set() for n in range(n_periods + 1)}
        
        s0 = model.S0
        m0 = payoff.initial_aggregate(s0)
        states_by_level[0].add((s0, m0))
        
        for n in range(n_periods):
            for s, m in states_by_level[n]:
                s_up = s * model.u
                m_up = payoff.update_aggregate(m, s_up)
                states_by_level[n + 1].add((s_up, m_up))
                
                s_down = s * model.d
                m_down = payoff.update_aggregate(m, s_down)
                states_by_level[n + 1].add((s_down, m_down))
                
        for s, m in states_by_level[n_periods]:
            state_key = (n_periods, s) if m is None else (n_periods, s, m)
            value_grid[state_key] = payoff.terminal_value(s, m)
            
        for n in range(n_periods - 1, -1, -1):
            for s, m in states_by_level[n]:
                s_up = s * model.u
                m_up = payoff.update_aggregate(m, s_up)
                s_down = s * model.d
                m_down = payoff.update_aggregate(m, s_down)
                
                key_up = (n+1, s_up) if m_up is None else (n+1, s_up, m_up)
                key_down = (n+1, s_down) if m_down is None else (n+1, s_down, m_down)
                
                v_n = (1 / (1 + model.r)) * (p_tilde * value_grid[key_up] + q_tilde * value_grid[key_down])
                delta_n = (value_grid[key_up] - value_grid[key_down]) / ((model.u - model.d) * s)
                
                if position == "long":
                    delta_n = -delta_n
                    
                state_key = (n, s) if m is None else (n, s, m)
                value_grid[state_key] = v_n
                delta_grid[state_key] = delta_n
                
        key0 = (0, s0) if m0 is None else (0, s0, m0)
        v0 = value_grid.get(key0, 0.0)
        delta0 = delta_grid.get(key0, 0.0)
        
        return PricingResult(v0=v0, delta0=delta0, value_grid=value_grid, delta_grid=delta_grid)