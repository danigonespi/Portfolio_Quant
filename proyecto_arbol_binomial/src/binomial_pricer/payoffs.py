from abc import ABC, abstractmethod
import numpy as np


class Payoff(ABC):
    @abstractmethod
    def compute(self, path: np.ndarray) -> float:
        """
        Calcula el pago (payoff) del derivado.
        Aunque en el modelo de un período solo se evalúa el último precio,
        la firma requiere la trayectoria completa [S0, ..., Sn] para
        mantener la interfaz compatible con opciones path-dependent en el futuro.
        """
        pass

class PathDependentPayoff(Payoff, ABC):
    """Payoff reducible a un estado (S_n, agregado_n). compute()
    se implementa una sola vez aquí a partir de tres hooks, para
    que una versión 'rápida' futura (Sección 1.3) nunca pueda
    divergir silenciosamente de esta versión de referencia."""

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

class LookbackOption(PathDependentPayoff):
    """Payoff M_N - S_N, M_n = max(S_0..S_n). Ejemplo 1.2.4."""
    
    def initial_aggregate(self, s0: float) -> float:
        return s0

    def update_aggregate(self, aggregate: float, s_next: float) -> float:
        return max(aggregate, s_next)

    def terminal_value(self, s_final: float, aggregate_final: float) -> float:
        return aggregate_final - s_final


class EuropeanCall(Payoff):
    def __init__(self, strike: float):
        self.strike = strike

    def compute(self, path: np.ndarray) -> float:
        """Pago de una opción call europea: max(S_N - K, 0)."""
        return max(path[-1] - self.strike, 0.0)


class EuropeanPut(Payoff):
    def __init__(self, strike: float):
        self.strike = strike

    def compute(self, path: np.ndarray) -> float:
        """Pago de una opción put europea: max(K - S_N, 0)."""
        return max(self.strike - path[-1], 0.0)


class Forward(Payoff):
    def __init__(self, delivery_price: float):
        self.delivery_price = delivery_price

    def compute(self, path: np.ndarray) -> float:
        """Pago de un contrato forward: S_N - K."""
        return path[-1] - self.delivery_price