1. **Concept and context**
Section 1.3 addresses the computational impracticability of naively applying the multiperiod binomial pricing algorithm, whose computation time grows exponentially (with $2^{100} \approx 10^{30}$ possible paths existing for 100 periods). The author demonstrates how to efficiently organize the algorithm through state space reduction, expressing the derivative's price as a function of a few key current variables (such as the stock price or its historical maximum) instead of depending on the entire historical sequence of coin tosses (Section 1.3, pp. 15-18).

2. **Formal definitions**
* $v_n(s)$: Value or price of the option at time $n$ expressed exclusively as a function of the current stock price $S_n = s$, used when the final payoff is not path-dependent.
* $M_n$: Maximum stock price reached to date at time $n$, implicitly defined as $\max_{0 \le k \le n} S_k$.
* $v_n(s, m)$: Value or price of the option at time $n$ expressed as a function of the current stock price $S_n = s$ and the maximum price reached to date $M_n = m$.
* $m \vee (2s)$: Mathematical operator introduced in the algorithm denoting the maximum between the value $m$ and the value $2s$.

3. **Key equations**
The only equation with explicit numbering assigned by the author in this section is the adaptation of the risk-neutral formula evaluated at step 2:
$$V_2(\omega_1\omega_2) = \frac{1}{1+r} [\tilde{p}V_3(\omega_1\omega_2H) + \tilde{q}V_3(\omega_1\omega_2T)] \quad \text{(1.3.1)}$$
*Key computational equations (unnumbered in the original text, but presented as canonical algorithmic formulas in the section):*
For an option dependent only on the current stock price (Example 1.3.1):
$$v_n(s) = \frac{1}{1+r} [\tilde{p}v_{n+1}(us) + \tilde{q}v_{n+1}(ds)]$$
$$\Delta_n(s) = \frac{v_{n+1}(us) - v_{n+1}(ds)}{(u-d)s}$$
For a lookback option dependent on the maximum (Example 1.3.2):
$$v_n(s, m) = \frac{1}{1+r} [\tilde{p}v_{n+1}(us, m \vee (us)) + \tilde{q}v_{n+1}(ds, m)]$$
$$\Delta_n(s, m) = \frac{v_{n+1}(us, m \vee (us)) - v_{n+1}(ds, m)}{(u-d)s}$$

4. **Assumptions and domain of validity**
* **For path-independent options (Example 1.3.1):** The validity of reducing the process $V_n(\omega_1\dots\omega_n)$ to $v_n(s)$ strictly requires that the final payoff of the option depends *only* on the stock price at the final time $N$.
* **For path-dependent options (Example 1.3.2):** The validity of reducing the problem to $v_n(s, m)$ requires that the option payoff can be determined by exclusively tracking the current price and a cumulative state variable (the maximum $m$).
* The author explicitly states that the lack of algorithmic grouping and state reduction triggers an exponential complexity that makes it impossible to process large trees in practice.

5. **Theorems and proof outline**
Not covered in this section (Section 1.3 does not introduce new theorems, but rather is a purely algorithmic optimization of Theorem 1.2.2 proven in the previous section).

6. **Exercises in this section**
*(Note: By explicitly excluding Exercise 1.8, which is the only exercise in the chapter directly linked to this section for modeling a path-dependent option, there are no more exercises corresponding to this section. Below, the complete theoretical examples required in your prompt are extracted).*

* **Example 1.3.1 (European Put Option with state reduction):**
Parameters: $S_0=4$, $u=2$, $d=1/2$, $r=1/4$, $\tilde{p}=\tilde{q}=1/2$, Strike $K=5$, expiration at $n=3$. Final payoff: $(5 - S_3)^+$.
*Tabulated values at step 3:*
$v_3(32) = 0, \quad v_3(8) = 0, \quad v_3(2) = 3, \quad v_3(0.50) = 4.50.$
*Tabulated values at step 2:*
$v_2(16) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(0)\right] = 0.$
$v_2(4) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(3)\right] = 1.20.$
$v_2(1) = \frac{4}{5}\left[\frac{1}{2}(3) + \frac{1}{2}(4.50)\right] = 3.$
*Tabulated values at step 1:*
$v_1(8) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(1.20)\right] = 0.48.$
$v_1(2) = \frac{4}{5}\left[\frac{1}{2}(1.20) + \frac{1}{2}(3)\right] = 1.68.$
*Tabulated value at step 0:*
$v_0(4) = \frac{4}{5}\left[\frac{1}{2}(0.48) + \frac{1}{2}(1.68)\right] = 0.864.$
* **Example 1.3.2 (Lookback Option with state reduction):**
Parameters: Inherited from Example 1.2.4 ($S_0=4, u=2, d=1/2, r=1/4, \tilde{p}=\tilde{q}=1/2$). Final payoff: $M_3 - S_3$.
*Tabulated values at step 3 ($v_3(s, m)$):*
$v_3(32, 32) = 0, \quad v_3(8, 16) = 8, \quad v_3(8, 8) = 0,$
$v_3(2, 8) = 6, \quad v_3(2, 4) = 2, \quad v_3(0.50, 4) = 3.50.$
*Tabulated values at step 2 ($v_2(s, m)$):*
$v_2(16, 16) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(8)\right] = 3.20.$
$v_2(4, 8) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(6)\right] = 2.40.$
$v_2(4, 4) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(2)\right] = 0.80.$
$v_2(1, 4) = \frac{4}{5}\left[\frac{1}{2}(2) + \frac{1}{2}(3.50)\right] = 2.20.$
*Tabulated values at step 1 ($v_1(s, m)$):*
$v_1(8, 8) = \frac{4}{5}\left[\frac{1}{2}(3.20) + \frac{1}{2}(2.40)\right] = 2.24.$
$v_1(2, 4) = \frac{4}{5}\left[\frac{1}{2}(0.80) + \frac{1}{2}(2.20)\right] = 1.20.$
*Tabulated value at step 0 ($v_0(s, m)$):*
$v_0(4, 4) = \frac{4}{5}\left[\frac{1}{2}(2.24) + \frac{1}{2}(1.20)\right] = 1.376.$

7. **Cross-references**
* **Theorem 1.2.2 (Section 1.2):** The theoretical basis for the backward pricing equation (1.3.1) comes from the proof of market completeness and replication established in the previous section.
* **Example 1.2.4 (Section 1.2):** Example 1.3.2 references the raw results of this previous example to empirically demonstrate that state grouping provides the same initial price much more efficiently.
* **Markov Processes (Section 2.5):** The author conceptually mentions that the basis of this optimization is the exclusive dependence on the current states to define the function $v_n$, an intuition that will act as a precursor for the rigorous theoretical definition of *Markov Processes* that will be developed in Chapter 2.