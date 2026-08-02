import numpy as np
from typing import Literal, Any
from dataclasses import dataclass, field

from .equity_model import BinomialStockModel
from .payoffs import Payoff, PathDependentPayoff
from .lattice import RecombiningLattice

StateKey = tuple[int, float] | tuple[int, float, Any] | str

@dataclass
class PricingResult:
    v0: float
    delta0: float
    value_grid: dict[StateKey, float] = field(default_factory=dict)
    delta_grid: dict[StateKey, float] = field(default_factory=dict)

class PricingEngine:
    def price(self, model: BinomialStockModel, payoff: Payoff, n_periods: int,
              position: Literal["short", "long"] = "short") -> PricingResult:
        """
        Calculates the arbitrage-free price and the hedge using backward induction.
        The complete symmetric recursive case (including T) is proved in Exercise 1.4.
        Uses Eq. (1.2.18), Eq. (1.2.16) and Eq. (1.2.17)
        """
        lattice = RecombiningLattice(n_periods)
        value_grid = {}
        delta_grid = {}

        p_tilde, q_tilde = model.risk_neutral_prob
        all_paths = list(lattice.enumerate_paths())

        for seq in all_paths:
            path_prices = model.price_path(seq)
            value_grid[seq] = payoff.compute(path_prices)

        discount = 1 / (1 + model.r)

        for n in range(n_periods - 1, -1, -1):
            prefixes = set(seq[:n] for seq in all_paths) if n_periods > 0 else {""}
            
            for prefix in prefixes:
                v_next_h = value_grid[prefix + "H"]
                v_next_t = value_grid[prefix + "T"]

                current_s = model.price_path(prefix)[-1] if prefix else model.S0
                s_next_h = current_s * model.u
                s_next_t = current_s * model.d

                v_n = discount * (p_tilde * v_next_h + q_tilde * v_next_t)
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
        Calculates the arbitrage-free price and the hedge through state space reduction (Section 1.3).

        Applies Eq. (1.3.1) for the risk-neutral value recursion,
        generalized by the unnumbered canonical algorithmic formulas
        for v_n(s) and Delta_n(s) (path-independent options), 
        and v_n(s, m) and Delta_n(s, m) (path-dependent options).
        """
        value_grid = {}
        delta_grid = {}
        p_tilde, q_tilde = model.risk_neutral_prob

        u_powers = [1.0] * (n_periods + 2)
        d_powers = [1.0] * (n_periods + 2)
        for i in range(1, n_periods + 2):
            u_powers[i] = u_powers[i-1] * model.u
            d_powers[i] = d_powers[i-1] * model.d
            
        def get_s(j: int, n_step: int) -> float:
            return model.S0 * u_powers[j] * d_powers[n_step - j]

        states_by_level = {n: set() for n in range(n_periods + 1)}
        
        m0 = payoff.initial_aggregate(model.S0)
        states_by_level[0].add((0, m0)) 
        
        for n in range(n_periods):
            for j, m in states_by_level[n]:
                s_up = get_s(j + 1, n + 1)
                m_up = payoff.update_aggregate(m, s_up)
                states_by_level[n + 1].add((j + 1, m_up))
                
                s_down = get_s(j, n + 1)
                m_down = payoff.update_aggregate(m, s_down)
                states_by_level[n + 1].add((j, m_down))
                
        for j, m in states_by_level[n_periods]:
            s = get_s(j, n_periods)
            state_key = (n_periods, s) if m is None else (n_periods, s, m)
            value_grid[state_key] = payoff.terminal_value(s, m)
            
        discount = 1 / (1 + model.r)
        
        for n in range(n_periods - 1, -1, -1):
            for j, m in states_by_level[n]:
                s = get_s(j, n)
                
                s_up = get_s(j + 1, n + 1)
                s_down = get_s(j, n + 1)
                
                m_up = payoff.update_aggregate(m, s_up)
                m_down = payoff.update_aggregate(m, s_down)
                
                key_up = (n+1, s_up) if m_up is None else (n+1, s_up, m_up)
                key_down = (n+1, s_down) if m_down is None else (n+1, s_down, m_down)
                
                v_n = discount * (p_tilde * value_grid[key_up] + q_tilde * value_grid[key_down])
                
                delta_n = (value_grid[key_up] - value_grid[key_down]) / (s_up - s_down)
                
                if position == "long":
                    delta_n = -delta_n
                    
                state_key = (n, s) if m is None else (n, s, m)
                value_grid[state_key] = v_n
                delta_grid[state_key] = delta_n
                
        key0 = (0, model.S0) if m0 is None else (0, model.S0, m0)
        v0 = value_grid.get(key0, 0.0)
        delta0 = delta_grid.get(key0, 0.0)
        
        return PricingResult(v0=v0, delta0=delta0, value_grid=value_grid, delta_grid=delta_grid)