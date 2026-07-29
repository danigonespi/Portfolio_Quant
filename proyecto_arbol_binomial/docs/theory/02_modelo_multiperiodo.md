1. **Concepto y contexto**
La Sección 1.2 extiende la lógica de valoración por ausencia de arbitraje de un solo período a un entorno dinámico de lanzamientos sucesivos de moneda, creando el modelo binomial multiperíodo. El objetivo central es demostrar que el mercado es **completo**, lo que significa que cualquier valor contingente (derivado) dependiente de la trayectoria puede ser replicado exactamente mediante una estrategia de negociación auto-financiada que ajusta las posiciones en el activo subyacente y la cuenta de mercado monetario en cada instante de tiempo (Sección 1.2, p. 8-14).

2. **Definiciones formales**
* $S_0$: Precio inicial (estrictamente positivo) del activo subyacente en el instante cero.
* $S_n(\omega_1 \dots \omega_n)$: Precio del activo en el instante $n$, que depende de los $n$ primeros lanzamientos. 
* $u$: Factor de subida (*up factor*).
* $d$: Factor de bajada (*down factor*).
* $r$: Tasa de interés por período para invertir y pedir prestado.
* $\omega_1 \omega_2 \dots \omega_n$: Secuencia de los resultados de los lanzamientos de moneda (donde $\omega_i \in \{H, T\}$).
* $\Delta_n(\omega_1 \dots \omega_n)$: Cantidad de acciones mantenidas en la cartera en el período $n$ hasta $n+1$.
* $X_n(\omega_1 \dots \omega_n)$: Valor de la cartera (riqueza) en el instante $n$.
* $V_N$: Variable aleatoria que representa el pago final contractual del derivado en el instante $N$.
* $V_n(\omega_1 \dots \omega_n)$: Precio libre de arbitraje del derivado en el instante $n$.
* $\tilde{p}, \tilde{q}$: Probabilidades neutrales al riesgo (*risk-neutral probabilities*).

3. **Ecuaciones clave**
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
$$X_N(\omega_1\omega_2\dots\omega_N) = V_N(\omega_1\omega_2\dots\omega_N) \text{ para todo } \omega_1\omega_2\dots\omega_N \quad \text{(1.2.18)}$$
$$X_n(\omega_1\dots\omega_n) = V_n(\omega_1\dots\omega_n) \quad \text{(1.2.19)}$$
$$X_{n+1}(H) = \Delta_n u S_n + (1+r)(X_n - \Delta_n S_n) \quad \text{(1.2.20)}$$

4. **Hipótesis y dominio de validez**
* **Condición de ausencia de arbitraje:** Es estrictamente necesario que $0 < d < 1+r < u$. Si esta condición se viola, existen oportunidades de arbitraje y el modelo se vuelve inválido para fijar precios equitativos.
* **Modelo sin fricciones y fracciones:** Se asume implícitamente, heredado de la sección 1.1, que las tasas de interés activa y pasiva son las mismas, y no existe el diferencial (*bid-ask spread*).

5. **Teoremas y esquema de demostración**
**Teorema 1.2.2 (Replication in the multiperiod binomial model):** En un modelo binomial de $N$ períodos con $0 < d < 1+r < u$, y siendo $V_N$ una variable aleatoria dependiente de los primeros $N$ lanzamientos. Si se define recursivamente $V_n$ hacia atrás usando la ecuación (1.2.16) y el portafolio $\Delta_n$ usando (1.2.17), y si iniciamos con $X_0 = V_0$, entonces la riqueza definida recursivamente hacia adelante mediante la ecuación (1.2.14) cumplirá que $X_N(\omega_1 \dots \omega_N) = V_N(\omega_1 \dots \omega_N)$ para todo escenario.
*Esquema de la demostración:*
1. La prueba se construye por inducción sobre $n$ moviéndose hacia adelante en el tiempo.
2. El caso base se asume desde la hipótesis al establecer $X_0 = V_0$.
3. Se plantea la hipótesis de inducción asumiendo que $X_n(\omega_1 \dots \omega_n) = V_n(\omega_1 \dots \omega_n)$ para un $n$ arbitrario.
4. Se utiliza la ecuación recursiva de la riqueza $X_{n+1}(H) = (1+r)X_n + \Delta_n S_n (u - (1+r))$ evaluada para un lanzamiento $H$.
5. Sustituyendo $X_n = V_n$ y el valor de $\Delta_n$ (Ec. 1.2.17), el término algebraico $(u - (1+r))$ se manipula para factorizar las expresiones como funciones de $\tilde{p}$ y $\tilde{q}$.
6. El álgebra reduce la ecuación a $X_{n+1}(H) = V_{n+1}(H)$. Análogamente, se infiere lo mismo para la cola ($T$), demostrando que el portafolio coincide de manera exacta con el valor del derivado $V_{n+1}$ pase lo que pase, completando la inducción hasta $N$.

6. **Ejercicios de esta sección** (y ejemplos requeridos)
* **Ejemplo 1.2.4 (Lookback option):** En un modelo de tres períodos donde $S_0=4$, $u=2$, $d=1/2$, $r=1/4$, lo que implica que $\tilde{p} = \tilde{q} = 1/2$. El pago del derivado *lookback* en el instante 3 es $V_3 = \max_{0\le n \le 3} S_n - S_3$.  
  Valores de pago final evaluados:
  $V_3(HHH) = 32 - 32 = 0$, $V_3(HHT) = 16 - 8 = 8$
  $V_3(HTH) = 8 - 8 = 0$, $V_3(HTT) = 8 - 2 = 6$
  $V_3(THH) = 8 - 8 = 0$, $V_3(THT) = 4 - 2 = 2$
  $V_3(TTH) = 4 - 2 = 2$, $V_3(TTT) = 4 - 0.50 = 3.50$  
  Valores en el paso 2:
  $V_2(HH) = \frac{4}{5}[\frac{1}{2}(0) + \frac{1}{2}(8)] = 3.20$
  $V_2(HT) = \frac{4}{5}[\frac{1}{2}(0) + \frac{1}{2}(6)] = 2.40$
  $V_2(TH) = \frac{4}{5}[\frac{1}{2}(0) + \frac{1}{2}(2)] = 0.80$
  $V_2(TT) = \frac{4}{5}[\frac{1}{2}(2) + \frac{1}{2}(3.50)] = 2.20$  
  Valores en el paso 1:
  $V_1(H) = \frac{4}{5}[\frac{1}{2}(3.20) + \frac{1}{2}(2.40)] = 2.24$
  $V_1(T) = \frac{4}{5}[\frac{1}{2}(0.80) + \frac{1}{2}(2.20)] = 1.20$  
  Valor en el paso 0:
  $V_0 = \frac{4}{5}[\frac{1}{2}(2.24) + \frac{1}{2}(1.20)] = 1.376$.  
  (Shreve indica en el Ejercicio 1.5 relacionado que el delta inicial correspondiente es $\Delta_0 = 0.1733$).

* **Exercise 1.4:** En la demostración del Teorema 1.2.2, usando la hipótesis de inducción (1.2.19) y las ecuaciones previas, mostrar paso a paso que $X_{n+1}(\omega_1 \dots \omega_n T) = V_{n+1}(\omega_1 \dots \omega_n T)$.
* **Exercise 1.6 (Hedging a long position—one period):** Considerar un banco que tiene una posición larga en la opción call europea del modelo de un período mostrado en la Figura 1.1.2 ($S_0=4$, $u=2$, $d=1/2$, $r=1/4$). La opción expira en $t=1$ y tiene strike $K=5$. Su precio inicial es $V_0 = 1.20$. El banco desea ganar la tasa de interés del $25\%$ sobre este capital ($1.20$) atado a la opción, de modo que en $t=1$, tras recolectar el pago de la opción (si lo hay), el banco obtenga exactamente $1.50$. Se pide especificar cómo debe invertir el operador del banco en acciones y en el mercado monetario para lograr este objetivo.
* **Exercise 1.7 (Hedging a long position—multiple periods):** Considerar un banco que tiene una posición larga en la opción *lookback* del Ejemplo 1.2.4. El banco pretende mantener la opción hasta la fecha de expiración y recibir el pago $V_3$. En el instante cero, el capital atado en la opción es $V_0 = 1.376$. El banco quiere ganar un $25\%$ de interés sobre dicho capital hasta el instante 3, de modo que tenga $(5/4)^3 \cdot 1.376 = 2.6875$ en el instante 3 independientemente de cómo resulten los lanzamientos, tras recolectar el pago de la opción. Se pide especificar cómo debe invertir el operador en acciones y en el mercado monetario para lograr esto.

7. **Referencias cruzadas**
* **Opciones dependientes de la trayectoria (*path-dependent*):** En esta sección se define que el modelo es completo y maneja incluso opciones donde el pago depende de toda la historia del precio (como en la *lookback*), concepto que será depurado computacionalmente en la **Sección 1.3** a través del establecimiento de variables de estado de Markov.
* **Teorema de Replicación:** Las bases conceptuales establecidas por las ecuaciones de cobertura multiperíodo serán formalizadas usando el lenguaje riguroso del Cálculo de Probabilidades (martingalas y esperanzas condicionales) a lo largo del **Capítulo 2**.