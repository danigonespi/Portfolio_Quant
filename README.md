# Portfolio Quant: Valoración de Opciones mediante Árboles Binomiales

Implementación en Python de los modelos de valoración de derivados financieros basados en el marco teórico de *Stochastic Calculus for Finance I* (Steven E. Shreve). Este proyecto traduce rigurosas ecuaciones de cálculo estocástico en una arquitectura de software modular, escalable y optimizada computacionalmente.

## Estado del Proyecto: Hitos Alcanzados (Capítulo 1)

El motor de valoración base está completo y validado, cubriendo los fundamentos del modelo binomial multiperiodo:

*   **Arquitectura Desacoplada:** Separación estricta entre la dinámica del activo subyacente (`equity_model.py`), la definición de los pagos (`payoffs.py`) y la lógica de resolución algorítmica (`engines.py`).
*   **Polimorfismo de Payoffs:** Interfaz unificada que soporta tanto opciones estándar (Europeas) como opciones dependientes de la trayectoria (ej. Lookback Options) sin romper los principios SOLID.
*   **Optimización Algorítmica (State Reduction):** Implementación de un `ReducedStateEngine` que colapsa trayectorias recombinantes. Para derivados no dependientes de la trayectoria (call, put), esto reduce la complejidad e de $O(2^N)$ a $O(N^2)$; para derivados dependientes de la trayectoria como la lookback, la reducción de estado a $(S_n, M_n)$ sigue siendo polinómica $(O(N^3))$ frente a la enumeración exhaustiva, permitiendo valorar árboles de $N=50$ en fracciones de segundo.
*   **Validación de Estrés:** Batería de pruebas exhaustiva (`pytest`) que asegura la ausencia de fugas exponenciales en tiempo de cómputo y garantiza la fidelidad matemática frente a los ejemplos teóricos ("Golden Examples").

## Estructura del Repositorio

La base de código está organizada para separar claramente la teoría matemática de la implementación y las pruebas:

*   **`docs/theory/`**: Notas teóricas en formato Markdown detallando el modelo de un periodo, multiperiodo, la reducción computacional y las particularidades de las opciones asiáticas.
*   **`src/binomial_pricer/`**: Código fuente principal. Contiene las clases del modelo, el generador del árbol (`lattice.py`), y los motores de valoración (`engines.py`).
*   **`tests/`**: Suite de pruebas unitarias y de integración para validar la correcta instanciación de modelos, evaluación de payoffs y eficiencia algorítmica de los motores.
*   **`analisis_convergencia.ipynb`**: Cuaderno Jupyter destinado al análisis empírico y visualización de la convergencia del árbol binomial hacia modelos de tiempo continuo (ej. Black-Scholes).

## Requisitos y Uso

El proyecto utiliza Python 3.9+ y aprovecha el tipado estricto (Type Hints). 

Para ejecutar la suite de validación matemática y computacional:

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar los tests con detalle de salida
pytest tests/ -v