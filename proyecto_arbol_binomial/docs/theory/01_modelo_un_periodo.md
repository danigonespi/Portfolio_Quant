1. **Concepto y contexto**
El modelo binomial de un período provee una herramienta introductoria para comprender la teoría de valoración por ausencia de arbitraje y la probabilidad asociada. En este modelo, la replicación de cualquier instrumento derivado se logra construyendo un portafolio con el activo subyacente y una cuenta del mercado monetario, lo que demuestra que el precio de los derivados depende exclusivamente del tamaño de los movimientos del mercado y no de las probabilidades empíricas reales de dichos movimientos (Sección 1.1, p. 1 y p. 8).

2. **Definiciones formales**
* $S_0$: Precio por acción del activo subyacente en el instante cero (cantidad estrictamente positiva).
* $S_1(H)$: Precio de la acción en el instante uno si el lanzamiento de la moneda resulta en cara ($H$).
* $S_1(T)$: Precio de la acción en el instante uno si el lanzamiento de la moneda resulta en cruz ($T$).
* $u$: Factor de subida (*up factor*).
* $d$: Factor de bajada (*down factor*).
* $r$: Tasa de interés aplicable para invertir o pedir prestado en el mercado monetario durante el período.
* $X_0$: Riqueza inicial del portafolio.
* $\Delta_0$: Cantidad de acciones del subyacente compradas o vendidas en corto en el instante cero.
* $V_1(H)$, $V_1(T)$: Valores de pago en el instante uno correspondientes al instrumento derivado, según el resultado de la moneda.
* $\tilde{p}$, $\tilde{q}$: Probabilidades neutrales al riesgo (*risk-neutral probabilities*).
* $V_0$: Precio libre de arbitraje del instrumento derivado en el instante cero.

3. **Ecuaciones clave**
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

5. **Hipótesis y dominio de validez**
* **Condición de ausencia de arbitraje:** Es imperativo que $0 < d < 1 + r < u$. 
  * Si se viola mediante $d \ge 1+r$, un agente podría pedir prestado a tasa $r$ para comprar acciones, garantizando el pago de su deuda en el peor caso ($T$) y logrando arbitraje por la ganancia estricta en el caso óptimo ($H$). 
  * Si se viola mediante $u \le 1+r$, un agente podría vender la acción en corto e invertir los ingresos en el mercado monetario, garantizando cubrir su posición corta con arbitraje.
* **Hipótesis sobre el activo subyacente:** Se asume inicialmente $d < u$. Si ocurriera $d > u$, bastaría con reetiquetar los lados de la moneda. Si $d = u$, el precio no sería aleatorio y el modelo perdería validez analítica de riesgo.
* **Supuestos de fricción de mercado:** El método asume que las acciones pueden subdividirse infinitamente; que las tasas de préstamo y depósito son idénticas; y que el precio de compra iguala al precio de venta (*zero bid-ask spread*). El texto alerta explícitamente que la violación del spread nulo puede ser un problema grave en entornos de baja liquidez.

5. **Teoremas y esquema de demostración**
No cubierto en esta sección (la Sección 1.1 deriva los argumentos de replicación de forma puramente algebraica a modo de ejemplo; los teoremas formales se introducen a partir de la Sección 1.2).

6. **Ejercicios de esta sección**
* **Exercise 1.1:** Asumiendo en el modelo binomial de un período que tanto $H$ como $T$ tienen probabilidad de ocurrencia positiva, demostrar que la condición (1.1.2) previene el arbitraje. Específicamente, demostrar que si $X_0 = 0$ y $X_1 = \Delta_0 S_1 + (1+r)(X_0 - \Delta_0 S_0)$, no se puede tener un $X_1$ estrictamente positivo con probabilidad positiva sin tener un $X_1$ estrictamente negativo con probabilidad positiva, sin importar la elección de $\Delta_0$.
* **Exercise 1.2:** En el escenario del Ejemplo 1.1.1 (donde $r=1/4$), si el precio de la opción en tiempo cero fuera artificialmente $1.20$, considere un agente que comienza con riqueza $X_0 = 0$ y compra en tiempo cero $\Delta_0$ acciones y $\Gamma_0$ opciones. Esta inversión deja una posición en efectivo de $-4\Delta_0 - 1.20\Gamma_0$. Demostrar que el valor total del portafolio en tiempo uno, dado por $X_1 = \Delta_0 S_1 + \Gamma_0 (S_1 - 5)^+ + \frac{5}{4}(-4\Delta_0 - 1.20\Gamma_0)$, cumple que si $P(X_1 > 0) > 0$, entonces necesariamente $P(X_1 < 0) > 0$, probando que el precio $1.20$ previene el arbitraje.
* **Exercise 1.3:** En el modelo de la Sección 1.1, determinar el precio en tiempo cero del derivado $V_1 = S_1$ (cuyo pago es el precio final de la acción en sí misma). Pide calcular explícitamente cuánto resulta $V_0$ aplicando la fórmula de valoración neutral al riesgo (1.1.10).

7. **Referencias cruzadas**
* **Capítulo 2 (*Probability Theory on Coin Toss Space*):** Toma los conceptos intuitivos de probabilidad presentados en esta sección y los formaliza mediante nociones de martingalas y procesos de Markov.
* **Capítulos 4 y 5 del Volumen II:** Se menciona que la independencia del precio frente a las probabilidades reales (fórmula 1.1.10) se extenderá allí a modelos de tiempo continuo, revelando que el precio de los derivados depende en última instancia de la volatilidad y no de la tasa media de crecimiento empírico. El supuesto del salto simple se reemplazará por el *Movimiento Browniano Geométrico*.