1. **Concept and context**
Section 1.2 extends the single-period arbitrage-free pricing logic to a dynamic environment of successive coin tosses, creating the multiperiod binomial model. The central objective is to demonstrate that the market is **complete**, meaning that any path-dependent contingent claim (derivative) can be exactly replicated through a self-financing trading strategy that adjusts positions in the underlying asset and the money market account at each point in time (Section 1.2, p. 8-14).

2. **Formal definitions**
* $S_0$: Initial price (strictly positive) of the underlying asset at time zero.
* $S_n(\omega_1 \dots \omega_n)$: Asset price at time $n$, which depends on the first $n$ tosses.
* $u$: Up factor.
* $d$: Down factor.
* $r$: Interest rate per period for investing and borrowing.
* $\omega_1 \omega_2 \dots \omega_n$: Sequence of the coin toss results (where $\omega_i \in \{H, T\}$).
* $\Delta_n(\omega_1 \dots \omega_n)$: Number of shares held in the portfolio from period $n$ to $n+1$.
* $X_n(\omega_1 \dots \omega_n)$: Value of the portfolio (wealth) at time $n$.
* $V_N$: Random variable representing the contractual final payoff of the derivative at time $N$.
* $V_n(\omega_1 \dots \omega_n)$: Arbitrage-free price of the derivative at time $n$.
* $\tilde{p}, \tilde{q}$: Risk-neutral probabilities.

3. **Key equations**

$$X_1 = \Delta_0 S_1 + (1+r)(V_0 - \Delta_0 S_0) \quad \text{(1.2.1)}$$
$$X_1(H) = \Delta_0 S_1(H) + (1+r)(V_0 - \Delta_0 S_0) \quad \text{(1.2.2)}$$
$$X_1(T) = \Delta_0 S_1(T) + (1+r)(V_0 - \Delta_0 S_0) \quad \text{(1.2.3)}$$
$$V_2 = \Delta_1 S_2 + (1+r)(X_1 - \Delta_1 S_1) \quad \text{(1.2.4)}$$
$$V_2(HH) = \Delta_1(H)S_2(HH) + (1+r)(X_1(H) - \Delta_1(H)S_1(H)) \quad \text{(1.2.5)}$$
$$V_2(HT) = \Delta_1(H)S_2(HT) + (1+r)(X_1(H) - \Delta_1(H)S_1(H)) \quad \text{(1.2.6)}$$
$$V_2(TH) = \Delta_1(T)S_2(TH) + (1+r)(X_1(T) - \Delta_1(T)S_1(T)) \quad \text{(1.2.7)}$$
$$V_2(TT) = \Delta_1(T)S_2(TT) + (1+r)(X_1(T) - \Delta_1(T)S_1(T)) \quad \text{(1.2.8)}$$
$$\Delta_1(T) = \frac{V_2(TH) - V_2(TT)}{S_2(TH) - S_2(TT)} \quad \text{(1.2.9)}$$
$$X_1(T) = \frac{1}{1+r} [\tilde{p}V_2(TH) + \tilde{q}V_2(TT)] \quad \text{(1.2.10)}$$
$$V_1(T) = \frac{1}{1+r} [\tilde{p}V_2(TH) + \tilde{q}V_2(TT)] \quad \text{(1.2.11)}$$
$$\Delta_1(H) = \frac{V_2(HH) - V_2(HT)}{S_2(HH) - S_2(HT)} \quad \text{(1.2.12)}$$
$$V_1(H) = \frac{1}{1+r} [\tilde{p}V_2(HH) + \tilde{q}V_2(HT)] \quad \text{(1.2.13)}$$
$$X_{n+1} = \Delta_n S_{n+1} + (1+r)(X_n - \Delta_n S_n) \quad \text{(1.2.14)}$$
$$\tilde{p} = \frac{1+r-d}{u-d}, \quad \tilde{q} = \frac{u-1-r}{u-d} \quad \text{(1.2.15)}$$
$$V_n(\omega_1\omega_2\dots\omega_n) = \frac{1}{1+r}[\tilde{p}V_{n+1}(\omega_1\omega_2\dots\omega_nH) + \tilde{q}V_{n+1}(\omega_1\omega_2\dots\omega_nT)] \quad \text{(1.2.16)}$$
$$\Delta_n(\omega_1\dots\omega_n) = \frac{V_{n+1}(\omega_1\dots\omega_nH) - V_{n+1}(\omega_1\dots\omega_nT)}{S_{n+1}(\omega_1\dots\omega_nH) - S_{n+1}(\omega_1\dots\omega_nT)} \quad \text{(1.2.17)}$$
$$X_N(\omega_1\omega_2\dots\omega_N) = V_N(\omega_1\omega_2\dots\omega_N) \text{ for all } \omega_1\omega_2\dots\omega_N \quad \text{(1.2.18)}$$
$$X_n(\omega_1\dots\omega_n) = V_n(\omega_1\dots\omega_n) \quad \text{(1.2.19)}$$
$$X_{n+1}(H) = \Delta_n u S_n + (1+r)(X_n - \Delta_n S_n) \quad \text{(1.2.20)}$$

4. **Assumptions and domain of validity**
* **No-arbitrage condition:** It is strictly necessary that $0 < d < 1+r < u$. If this condition is violated, arbitrage opportunities exist and the model becomes invalid for fair pricing.
* **Frictionless and fractional model:** It is implicitly assumed, inherited from section 1.1, that borrowing and lending interest rates are the same, and there is no bid-ask spread.

5. **Theorems and proof outline**
**Theorem 1.2.2 (Replication in the multiperiod binomial model):** In an $N$-period binomial model with $0 < d < 1+r < u$, and letting $V_N$ be a random variable depending on the first $N$ tosses. If we recursively define $V_n$ backward using equation (1.2.16) and the portfolio $\Delta_n$ using (1.2.17), and if we start with $X_0 = V_0$, then the wealth recursively defined forward via equation (1.2.14) will satisfy $X_N(\omega_1 \dots \omega_N) = V_N(\omega_1 \dots \omega_N)$ for every scenario.
*Proof outline:*
1. The proof is constructed by induction on $n$ moving forward in time.
2. The base case is assumed from the hypothesis by setting $X_0 = V_0$.
3. The induction hypothesis is established by assuming that $X_n(\omega_1 \dots \omega_n) = V_n(\omega_1 \dots \omega_n)$ for an arbitrary $n$.
4. The recursive wealth equation $X_{n+1}(H) = (1+r)X_n + \Delta_n S_n (u - (1+r))$ is used, evaluated for a toss $H$.
5. Substituting $X_n = V_n$ and the value of $\Delta_n$ (Eq. 1.2.17), the algebraic term $(u - (1+r))$ is manipulated to factor the expressions as functions of $\tilde{p}$ and $\tilde{q}$.
6. The algebra reduces the equation to $X_{n+1}(H) = V_{n+1}(H)$. Similarly, the same is inferred for tails ($T$), proving that the portfolio matches exactly the value of the derivative $V_{n+1}$ no matter what happens, completing the induction up to $N$.

6. **Exercises in this section** (and required examples)
* **Example 1.2.4 (Lookback option):** In a three-period model where $S_0=4$, $u=2$, $d=1/2$, $r=1/4$, which implies that $\tilde{p} = \tilde{q} = 1/2$. The payoff of the lookback derivative at time 3 is $V_3 = \max_{0\le n \le 3} S_n - S_3$.
Final payoff values evaluated:
$V_3(HHH) = 32 - 32 = 0$, $V_3(HHT) = 16 - 8 = 8$
$V_3(HTH) = 8 - 8 = 0$, $V_3(HTT) = 8 - 2 = 6$
$V_3(THH) = 8 - 8 = 0$, $V_3(THT) = 4 - 2 = 2$
$V_3(TTH) = 4 - 2 = 2$, $V_3(TTT) = 4 - 0.50 = 3.50$
Values at step 2:
$V_2(HH) = \frac{4}{5}[\frac{1}{2}(0) + \frac{1}{2}(8)] = 3.20$
$V_2(HT) = \frac{4}{5}[\frac{1}{2}(0) + \frac{1}{2}(6)] = 2.40$
$V_2(TH) = \frac{4}{5}[\frac{1}{2}(0) + \frac{1}{2}(2)] = 0.80$
$V_2(TT) = \frac{4}{5}[\frac{1}{2}(2) + \frac{1}{2}(3.50)] = 2.20$
Values at step 1:
$V_1(H) = \frac{4}{5}[\frac{1}{2}(3.20) + \frac{1}{2}(2.40)] = 2.24$
$V_1(T) = \frac{4}{5}[\frac{1}{2}(0.80) + \frac{1}{2}(2.20)] = 1.20$
Value at step 0:
$V_0 = \frac{4}{5}[\frac{1}{2}(2.24) + \frac{1}{2}(1.20)] = 1.376$.
(Shreve indicates in the related Exercise 1.5 that the corresponding initial delta is $\Delta_0 = 0.1733$).
* **Exercise 1.4:** In the proof of Theorem 1.2.2, using the induction hypothesis (1.2.19) and previous equations, show step-by-step that $X_{n+1}(\omega_1 \dots \omega_n T) = V_{n+1}(\omega_1 \dots \omega_n T)$.
* **Exercise 1.6 (Hedging a long position—one period):** Consider a bank that holds a long position in the European call option of the one-period model shown in Figure 1.1.2 ($S_0=4$, $u=2$, $d=1/2$, $r=1/4$). The option expires at $t=1$ and has a strike $K=5$. Its initial price is $V_0 = 1.20$. The bank wishes to earn the $25\%$ interest rate on this capital ($1.20$) tied up in the option, so that at $t=1$, after collecting the payoff of the option (if any), the bank has exactly $1.50$. You are asked to specify how the bank's trader should invest in stock and in the money market to achieve this goal.
* **Exercise 1.7 (Hedging a long position—multiple periods):** Consider a bank that has a long position in the lookback option of Example 1.2.4. The bank intends to hold the option until the expiration date and receive the payoff $V_3$. At time zero, the capital tied up in the option is $V_0 = 1.376$. The bank wants to earn $25\%$ interest on this capital up to time 3, so that it has $(5/4)^3 \cdot 1.376 = 2.6875$ at time 3 regardless of how the coin tosses turn out, after collecting the option payoff. You are asked to specify how the trader should invest in stock and in the money market to achieve this.

7. **Cross-references**
* **Path-dependent options:** This section defines that the model is complete and handles even options where the payoff depends on the entire price history (such as the lookback), a concept that will be computationally refined in **Section 1.3** through the establishment of Markov state variables.
* **Replication Theorem:** The conceptual foundations established by the multiperiod hedging equations will be formalized using the rigorous language of Probability Calculus (martingales and conditional expectations) throughout **Chapter 2**.