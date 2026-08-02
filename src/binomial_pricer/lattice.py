import itertools
from collections.abc import Iterator

class RecombiningLattice:
    def __init__(self, n_periods: int):
        self.n_periods = n_periods

    def num_nodes(self, step: int) -> int:
        """
        In a standard recombining binomial tree, the number of nodes
        at step n is n + 1.

        Not used yet in chapter 1 -- kept on purpose
        as a pure combinatorial structure utility, with an eye towards
        Chapter 6 (interest rate dependent assets), where
        the shape of the tree will be needed regardless of the
        stochastic process that traverses it.
        """
        return step + 1

    def enumerate_paths(self) -> Iterator[str]:
        """
        Generates the 2n_periods sequences 'HHH...', 'HHT...', etc.
        It is the actual calculation mechanism of this batch since, not yet having
        the state reduction of Section 1.3, the engine traverses
        these complete sequences.
        """
        if self.n_periods == 0:
            yield ""
            return
        
        for p in itertools.product("HT", repeat=self.n_periods):
            yield "".join(p)