import numpy as np
from dataclasses import dataclass

@dataclass(frozen=True)
class BinomialStockModel:
    s0: float
    u: float
    d: float
    r: float

    def __post_init__(self) -> None:
        """
        Validates the no-arbitrage condition. Uses Eq. (1.1.2).
        """
        if self.s0 <= 0:
            raise ValueError(f"s0 must be strictly positive (s0={self.s0}).")
            
        if self.d <= 0:
            raise ValueError(f"Domain violation: d must be strictly positive (d={self.d}).")
            
        if self.d >= 1 + self.r:
            raise ValueError(f"Arbitrage condition violated: d ({self.d}) >= 1+r ({1+self.r}). ")
            
        if 1 + self.r >= self.u:
            raise ValueError(f"Arbitrage condition violated: 1+r ({1+self.r}) >= u ({self.u}). ")

    @property
    def risk_neutral_prob(self) -> tuple[float, float]:
        """
        Calculates the risk-neutral probabilities (p̃, q̃). Uses Eq. (1.1.8) and Eq. (1.2.15).
        """
        p_tilde = (1 + self.r - self.d) / (self.u - self.d)
        q_tilde = (self.u - 1 - self.r) / (self.u - self.d)
        return p_tilde, q_tilde

    @property
    def s1_h(self) -> float:
        """
        Calculates the stock price at time one (Heads/H). Uses Eq. (1.1.1).
        """
        return self.s0 * self.u

    @property
    def s1_t(self) -> float:
        """
        Calculates the stock price at time one (Tails/T). Uses Eq. (1.1.1).
        """
        return self.s0 * self.d

    def price_path(self, coin_sequence: str) -> np.ndarray:
        """
        Generates S_0, S_1, ..., S_n for a given sequence of tosses,
        recursively applying u or d at each step. Uses Eq. (1.1.1).
        """
        path = [self.s0]
        current_s = self.s0
        for coin in coin_sequence:
            if coin == 'H':
                current_s *= self.u
            elif coin == 'T':
                current_s *= self.d
            else:
                raise ValueError(f"Unrecognized coin: {coin}")
            path.append(current_s)
        return np.array(path)