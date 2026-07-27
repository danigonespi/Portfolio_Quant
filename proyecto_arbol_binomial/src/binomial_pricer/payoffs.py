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