import itertools
from typing import Iterator

class RecombiningLattice:
    def __init__(self, n_periods: int):
        self.n_periods = n_periods

    def num_nodes(self, step: int) -> int:
        """
        En un árbol binomial recombinante estándar, el número de nodos
        en el paso n es n + 1.
        """
        return step + 1

    def enumerate_paths(self) -> Iterator[str]:
        """Genera las 2**n_periods secuencias 'HHH...', 'HHT...', etc.
        Es el mecanismo de cálculo real de este batch (no un oráculo
        futuro): al no tener aún la reducción de estado de la Sección
        1.3, el motor recorre estas secuencias completas."""
        if self.n_periods == 0:
            yield ""
            return
        
        for p in itertools.product("HT", repeat=self.n_periods):
            yield "".join(p)