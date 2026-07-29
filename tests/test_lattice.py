import pytest
from binomial_pricer.lattice import RecombiningLattice

def test_num_nodes():
    lattice = RecombiningLattice(n_periods=3)
    assert lattice.num_nodes(0) == 1
    assert lattice.num_nodes(3) == 4

def test_enumerate_paths_generates_2_to_the_n_paths():
    lattice_3 = RecombiningLattice(n_periods=3)
    paths_3 = list(lattice_3.enumerate_paths())
    assert len(paths_3) == 8
    assert "HHH" in paths_3
    assert "TTT" in paths_3

    lattice_0 = RecombiningLattice(n_periods=0)
    paths_0 = list(lattice_0.enumerate_paths())
    assert len(paths_0) == 1
    assert paths_0[0] == ""