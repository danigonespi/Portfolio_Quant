from abc import ABC, abstractmethod
import numpy as np
from typing import Any


class Payoff(ABC):
    def initial_aggregate(self, s0: float) -> Any:
        return None
        
    def update_aggregate(self, aggregate: Any, s_next: float) -> Any:
        return None
        
    def terminal_value(self, s_final: float, aggregate_final: Any) -> float:
        """By default, stateless payoffs evaluate only the final price."""
        return self.compute(np.array([s_final]))
        
    @abstractmethod
    def compute(self, path: np.ndarray) -> float:
        """
        Calculates the derivative payoff.
        Although in the one-period model only the final price is evaluated,
        the signature requires the complete path [s_0, ..., s_n] to keep
        the interface compatible with path-dependent options (see PathDependentPayoff).
        """
        pass


class PathDependentPayoff(Payoff, ABC):
    """
    Payoff reducible to a state (s_n, aggregate_n). compute()
    is implemented only once here from three hooks, so that
    ReducedStateEngine (Section 1.3) can never silently diverge from this
    reference version -- see test_cross_validation_* in test_engines.py.
    """
    
    @abstractmethod
    def initial_aggregate(self, s0: float) -> float:
        pass

    @abstractmethod
    def update_aggregate(self, aggregate: float, s_next: float) -> float:
        pass

    @abstractmethod
    def terminal_value(self, s_final: float, aggregate_final: float) -> float:
        pass

    def compute(self, path: np.ndarray) -> float:
        agg = self.initial_aggregate(path[0])
        for s in path[1:]:
            agg = self.update_aggregate(agg, s)
        return self.terminal_value(path[-1], agg)


class EuropeanCall(Payoff):
    def __init__(self, strike: float) -> None:
        self.strike = strike

    def compute(self, path: np.ndarray) -> float:
        """European call option payoff: max(s_N - K, 0)."""
        return max(path[-1] - self.strike, 0.0)


class EuropeanPut(Payoff):
    def __init__(self, strike: float) -> None:
        self.strike = strike

    def compute(self, path: np.ndarray) -> float:
        """European put option payoff: max(s - S_N, 0)."""
        return max(self.strike - path[-1], 0.0)


class Forward(Payoff):
    def __init__(self, delivery_price: float) -> None:
        self.delivery_price = delivery_price

    def compute(self, path: np.ndarray) -> float:
        """Forward contract payoff: s_N - K."""
        return path[-1] - self.delivery_price


class LookbackOption(PathDependentPayoff):
    """Payoff m_N - s_N, m_n = max(s_0..s_n). Example 1.2.4."""
    
    def initial_aggregate(self, s0: float) -> float:
        return s0

    def update_aggregate(self, aggregate: float, s_next: float) -> float:
        return max(aggregate, s_next)

    def terminal_value(self, s_final: float, aggregate_final: float) -> float:
        return aggregate_final - s_final


class AsianOption(PathDependentPayoff):
    """Payoff max(y_N/(N+1) - K, 0), y_n = running sum s_0..s_n. Exercise 1.8."""

    def __init__(self, strike: float, n_periods: int) -> None:
        self.strike = strike
        self.n_periods = n_periods

    def initial_aggregate(self, s0: float) -> float:
        return s0

    def update_aggregate(self, aggregate: float, s_next: float) -> float:
        return aggregate + s_next

    def terminal_value(self, s_final: float, aggregate_final: float) -> float:
        return max(aggregate_final / (self.n_periods + 1) - self.strike, 0.0)