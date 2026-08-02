1. **Concept and context**
The one-period binomial model provides an introductory tool to understand arbitrage-free pricing theory and the associated probability. In this model, the replication of any derivative instrument is achieved by constructing a portfolio with the underlying asset and a money market account, which demonstrates that the price of derivatives depends exclusively on the size of the market movements and not on the actual probabilities of these movements (Section 1.1, p. 1 and p. 8).

2. **Formal definitions**
* $S_0$: Price per share of the underlying asset at time zero (strictly positive quantity).
* $S_1(H)$: Stock price at time one if the coin toss results in heads ($H$).
* $S_1(T)$: Stock price at time one if the coin toss results in tails ($T$).
* $u$: Up factor.
* $d$: Down factor.
* $r$: Interest rate applicable for investing or borrowing in the money market during the period.
* $X_0$: Initial wealth of the portfolio.
* $\Delta_0$: Number of shares of the underlying asset bought or short-sold at time zero.
* $V_1(H)$, $V_1(T)$: Payoff values at time one corresponding to the derivative instrument, depending on the coin toss result.
* $\tilde{p}$, $\tilde{q}$: Risk-neutral probabilities.
* $V_0$: Arbitrage-free price of the derivative instrument at time zero.

3. **Key equations**
$$u = \frac{S_1(H)}{S_0}, \quad d = \frac{S_1(T)}{S_0} \quad \text{(1.1.1)}$$
$$0 < d < 1 + r < u \quad \text{(1.1.2)}$$
$$X_0 + \Delta_0 \left( \frac{S_1(H)}{1+r} - S_0 \right) = \frac{V_1(H)}{1+r} \quad \text{(1.1.3)}$$
$$X_0 + \Delta_0 \left( \frac{S_1(T)}{1+r} - S_0 \right) = \frac{V_1(T)}{1+r} \quad \text{(1.1.4)}$$
$$X_0 + \Delta_0 \left( \frac{1}{1+r} [\tilde{p}S_1(H) + \tilde{q}S_1(T)] - S_0 \right) = \frac{1}{1+r} [\tilde{p}V_1(H) + \tilde{q}V_1(T)] \quad \text{(1.1.5)}$$
$$S_0 = \frac{1}{1+r} [\tilde{p}S_1(H) + \tilde{q}S_1(T)] \quad \text{(1.1.6)}$$
$$X_0 = \frac{1}{1+r} [\tilde{p}V_1(H) + \tilde{q}V_1(T)] \quad \text{(1.1.7)}$$
$$\tilde{p} = \frac{1+r-d}{u-d} \quad \tilde{q} = \frac{u-1-r}{u-d} \quad \text{(1.1.8)}$$
$$\Delta_0 = \frac{V_1(H) - V_1(T)}{S_1(H) - S_1(T)} \quad \text{(1.1.9)}$$
$$V_0 = \frac{1}{1+r} [\tilde{p}V_1(H) + \tilde{q}V_1(T)] \quad \text{(1.1.10)}$$

4. **Assumptions and domain of validity**
* **No-arbitrage condition:** It is imperative that $0 < d < 1 + r < u$.
* If violated by $d \ge 1+r$, an agent could borrow at rate $r$ to buy shares, guaranteeing the repayment of their debt in the worst case ($T$) and achieving arbitrage through strict profit in the optimal case ($H$).
* If violated by $u \le 1+r$, an agent could short-sell the stock and invest the proceeds in the money market, guaranteeing to cover their short position with arbitrage.
* **Assumptions about the underlying asset:** It is initially assumed that $d < u$. If $d > u$ were to occur, it would suffice to relabel the sides of the coin. If $d = u$, the price would not be random and the model would lose analytical risk validity.
* **Market friction assumptions:** The method assumes that shares can be infinitely subdivided; that borrowing and lending rates are identical; and that the buying price equals the selling price (*zero bid-ask spread*). The text explicitly warns that violating the zero spread can be a serious problem in low-liquidity environments.

5. **Theorems and proof outline**
Not covered in this section (Section 1.1 derives the replication arguments purely algebraically as an example; formal theorems are introduced starting in Section 1.2).

6. **Exercises in this section**
* **Exercise 1.1:** Assuming in the one-period binomial model that both $H$ and $T$ have a positive probability of occurrence, prove that condition (1.1.2) prevents arbitrage. Specifically, prove that if $X_0 = 0$ and $X_1 = \Delta_0 S_1 + (1+r)(X_0 - \Delta_0 S_0)$, one cannot have a strictly positive $X_1$ with positive probability without having a strictly negative $X_1$ with positive probability, regardless of the choice of $\Delta_0$.
* **Exercise 1.2:** In the scenario of Example 1.1.1 (where $r=1/4$), if the option price at time zero were artificially $1.20$, consider an agent who starts with wealth $X_0 = 0$ and buys at time zero $\Delta_0$ shares and $\Gamma_0$ options. This investment leaves a cash position of $-4\Delta_0 - 1.20\Gamma_0$. Prove that the total value of the portfolio at time one, given by $X_1 = \Delta_0 S_1 + \Gamma_0 (S_1 - 5)^+ + \frac{5}{4}(-4\Delta_0 - 1.20\Gamma_0)$, satisfies that if $P(X_1 > 0) > 0$, then necessarily $P(X_1 < 0) > 0$, proving that the price $1.20$ prevents arbitrage.
* **Exercise 1.3:** In the model of Section 1.1, determine the time-zero price of the derivative $V_1 = S_1$ (whose payoff is the final price of the stock itself). It asks to explicitly calculate what $V_0$ is by applying the risk-neutral pricing formula (1.1.10).

7. **Cross-references**
* **Chapter 2 (*Probability Theory on Coin Toss Space*):** Takes the intuitive probability concepts presented in this section and formalizes them through notions of martingales and Markov processes.
* **Chapters 4 and 5 of Volume II:** It is mentioned that the independence of the price from actual probabilities (formula 1.1.10) will be extended there to continuous-time models, revealing that the price of derivatives ultimately depends on volatility and not on the mean empirical growth rate. The simple jump assumption will be replaced by *Geometric Brownian Motion*.