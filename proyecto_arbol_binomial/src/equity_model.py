from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class BinomialStockModel:
    S0: float
    u: float
    d: float
    r: float

    def __post_init__(self):
        """
        Valida la condición de ausencia de arbitraje.
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.2).
        """
        if self.S0 <= 0:
            raise ValueError(f"S0 debe ser estrictamente positivo (S0={self.S0}).")
            
        if self.d <= 0:
            raise ValueError(f"Violación de dominio: d debe ser estrictamente positivo (d={self.d}).")
            
        if self.d >= 1 + self.r:
            raise ValueError(f"Condición de arbitraje violada: d ({self.d}) >= 1+r ({1+self.r}). "
                "Un agente podría pedir prestado a la tasa r para comprar acciones, "
                "garantizando repagar su deuda y logrando arbitraje."
            )
            
        if 1 + self.r >= self.u:
            raise ValueError(f"Condición de arbitraje violada: 1+r ({1+self.r}) >= u ({self.u}). "
                "Un agente podría vender en corto la acción e invirtiendo los ingresos "
                "a la tasa r lograría arbitraje."
            )

    @property
    def risk_neutral_prob(self) -> Tuple[float, float]:
        """
        Calcula las probabilidades neutrales al riesgo (p̃, q̃).
        Ver docs/theory/01_modelo_un_periodo.md -- Eq. (1.1.8).
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