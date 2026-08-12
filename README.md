# The Binomial Asset Pricing Model

Python implementation of financial derivative pricing models based on the theoretical framework of *Stochastic Calculus for Finance I* (Steven E. Shreve). This project translates rigorous stochastic calculus equations into a modular, scalable, and computationally optimized software architecture.

## Project Status: Milestones Achieved (Chapter 1)

The core pricing engine is complete and validated, covering the fundamentals of the multi-period binomial model:

* **Decoupled Architecture:** Strict separation between the underlying asset dynamics (`equity_model.py`), payoff definitions (`payoffs.py`), and algorithmic resolution logic (`engines.py`).
* **Payoff Polymorphism:** Unified interface supporting both standard (European) and path-dependent options (e.g., Lookback Options) without breaking SOLID principles.
* **Algorithmic Optimization (State Reduction):** Implementation of a `ReducedStateEngine` that collapses recombining paths. For path-independent derivatives (call, put), this reduces time complexity from $O(2^N)$ to $O(N^2)$; for path-dependent derivatives like the lookback option, the state reduction to $(S_n, M_n)$ remains polynomial $(O(N^3))$ compared to exhaustive enumeration, allowing trees of $N=50$ to be priced in fractions of a second.
* **Stress Validation:** Exhaustive test suite (`pytest`) that ensures the absence of exponential leaks in compute time and guarantees mathematical fidelity against theoretical examples ("Golden Examples").

## Repository Structure

The codebase is organized to clearly separate mathematical theory from implementation and testing:

* **`docs/theory/`**: Theoretical notes in Markdown format detailing the one-period and multi-period models, computational state reduction, and the specificities of Asian options.
* **`src/binomial_pricer/`**: Main source code. Contains the model classes, the tree generator (`lattice.py`), and the pricing engines (`engines.py`).
* **`tests/`**: Unit and integration testing suite to validate correct model instantiation, payoff evaluation, and the algorithmic efficiency of the engines.
* **`shreve_v1_notebook.ipynb`**: Jupyter Notebook intended for model analysis and usage.

## Requirements and Usage

The project uses Python 3.10+ and leverages strict typing (Type Hints).

To run the mathematical and computational validation suite:

```bash
# Run all tests
pytest tests/

# Run tests with detailed output
pytest tests/ -v

```

## License

Released under the MIT License — see [LICENSE](../LICENSE).
