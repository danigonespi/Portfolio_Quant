import numpy as np
from dataclasses import dataclass

@dataclass(frozen=True)
class BinomialStockModel:
    S0: float
    u: float
    d: float
    r: float

    def __post_init__(self) -> None:
        """
        Valida la condición de ausencia de arbitraje.
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.2).
        """
        if self.S0 <= 0:
            raise ValueError(f"S0 debe ser estrictamente positivo (S0={self.S0}).")
            
        if self.d <= 0:
            raise ValueError(f"Violación de dominio: d debe ser estrictamente positivo (d={self.d}).")
            
        if self.d >= 1 + self.r:
            raise ValueError(f"Condición de arbitraje violada: d ({self.d}) >= 1+r ({1+self.r}). ")
            
        if 1 + self.r >= self.u:
            raise ValueError(f"Condición de arbitraje violada: 1+r ({1+self.r}) >= u ({self.u}). ")

    @property
    def risk_neutral_prob(self) -> tuple[float, float]:
        """
        Calcula las probabilidades neutrales al riesgo (p̃, q̃).
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.8) y Eq. (1.2.15).
        """
        p_tilde = (1 + self.r - self.d) / (self.u - self.d)
        q_tilde = (self.u - 1 - self.r) / (self.u - self.d)
        return p_tilde, q_tilde

    @property
    def s1_h(self) -> float:
        """
        Calcula el precio de la acción en el instante uno (Cara/H).
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.1).
        """
        return self.S0 * self.u

    @property
    def s1_t(self) -> float:
        """
        Calcula el precio de la acción en el instante uno (Cruz/T).
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.1).
        """
        return self.S0 * self.d

    def price_path(self, coin_sequence: str) -> np.ndarray:
        """
        Genera S_0, S_1, ..., S_n para una secuencia de lanzamientos dada,
        aplicando recursivamente u o d en cada paso.
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.1).
        """
        path = [self.S0]
        current_s = self.S0
        for coin in coin_sequence:
            if coin == 'H':
                current_s *= self.u
            elif coin == 'T':
                current_s *= self.d
            else:
                raise ValueError(f"Moneda no reconocida: {coin}")
            path.append(current_s)
        return np.array(path)