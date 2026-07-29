1. **Concepto y contexto**
La Sección 1.3 aborda la impracticabilidad computacional de aplicar ingenuamente el algoritmo de valoración binomial multiperíodo, cuyo tiempo de cálculo crece de forma exponencial (existiendo $2^{100} \approx 10^{30}$ trayectorias posibles para 100 periodos). El autor demuestra cómo organizar el algoritmo de manera eficiente mediante la reducción del espacio de estados, expresando el precio del derivado como función de unas pocas variables actuales clave (como el precio de la acción o su máximo histórico) en lugar de depender de toda la secuencia histórica de lanzamientos de la moneda (Sección 1.3, pp. 15-18).

2. **Definiciones formales**
*   $v_n(s)$: Valor o precio de la opción en el instante $n$ expresado como función exclusiva del precio actual de la acción $S_n = s$, utilizado cuando el pago final no es dependiente de la trayectoria.
*   $M_n$: Máximo precio de la acción alcanzado hasta la fecha en el instante $n$, definido implícitamente como $\max_{0 \le k \le n} S_k$.
*   $v_n(s, m)$: Valor o precio de la opción en el instante $n$ expresado como función del precio actual de la acción $S_n = s$ y el precio máximo alcanzado hasta la fecha $M_n = m$.
*   $m \vee (2s)$: Operador matemático introducido en el algoritmo que denota el máximo entre el valor $m$ y el valor $2s$.

3. **Ecuaciones clave**
La única ecuación con numeración explícita asignada por el autor en esta sección es la adaptación de la fórmula neutral al riesgo evaluada en el paso 2:
$$V_2(\omega_1\omega_2) = \frac{1}{1+r} [\tilde{p}V_3(\omega_1\omega_2H) + \tilde{q}V_3(\omega_1\omega_2T)] \quad \text{(1.3.1)}$$

*Ecuaciones computacionales clave (sin numerar en el texto original, pero presentadas como fórmulas algorítmicas canónicas en la sección):*
Para una opción dependiente solo del precio actual de la acción (Ejemplo 1.3.1):
$$v_n(s) = \frac{1}{1+r} [\tilde{p}v_{n+1}(us) + \tilde{q}v_{n+1}(ds)]$$
$$\Delta_n(s) = \frac{v_{n+1}(us) - v_{n+1}(ds)}{(u-d)s}$$

Para una opción *lookback* dependiente del máximo (Ejemplo 1.3.2):
$$v_n(s, m) = \frac{1}{1+r} [\tilde{p}v_{n+1}(us, m \vee (us)) + \tilde{q}v_{n+1}(ds, m)]$$
$$\Delta_n(s, m) = \frac{v_{n+1}(us, m \vee (us)) - v_{n+1}(ds, m)}{(u-d)s}$$

4. **Hipótesis y dominio de validez**
*   **Para opciones independientes de la trayectoria (Ejemplo 1.3.1):** La validez de reducir el proceso $V_n(\omega_1\dots\omega_n)$ a $v_n(s)$ exige estrictamente que el pago final de la opción dependa *únicamente* del precio de la acción en el instante final $N$.
*   **Para opciones dependientes de la trayectoria (Ejemplo 1.3.2):** La validez de reducir el problema a $v_n(s, m)$ requiere que el pago de la opción pueda determinarse rastreando exclusivamente el precio actual y una variable de estado acumulativa (el máximo $m$). 
*   El autor establece explícitamente que la falta de agrupación algorítmica y reducción de estados desencadena una complejidad exponencial que imposibilita procesar árboles grandes en la práctica.

5. **Teoremas y esquema de demostración**
No cubierto en esta sección (la Sección 1.3 no introduce teoremas nuevos, sino que es una optimización puramente algorítmica del Teorema 1.2.2 demostrado en la sección anterior).

6. **Ejercicios de esta sección** 
*(Nota: Al excluirse explícitamente el Ejercicio 1.8, que es el único ejercicio del capítulo ligado directamente a esta sección para modelar una opción dependiente de la trayectoria, no hay más ejercicios correspondientes a esta sección. A continuación se extraen los ejemplos teóricos completos requeridos en tu *prompt*).*

*   **Ejemplo 1.3.1 (Opción Put Europea con reducción de estado):** 
    Parámetros: $S_0=4$, $u=2$, $d=1/2$, $r=1/4$, $\tilde{p}=\tilde{q}=1/2$, Strike $K=5$, expiración en $n=3$. Pago final: $(5 - S_3)^+$.
    *Valores tabulados en el paso 3:*
    $v_3(32) = 0, \quad v_3(8) = 0, \quad v_3(2) = 3, \quad v_3(0.50) = 4.50.$
    *Valores tabulados en el paso 2:*
    $v_2(16) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(0)\right] = 0.$
    $v_2(4) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(3)\right] = 1.20.$
    $v_2(1) = \frac{4}{5}\left[\frac{1}{2}(3) + \frac{1}{2}(4.50)\right] = 3.$
    *Valores tabulados en el paso 1:*
    $v_1(8) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(1.20)\right] = 0.48.$
    $v_1(2) = \frac{4}{5}\left[\frac{1}{2}(1.20) + \frac{1}{2}(3)\right] = 1.68.$
    *Valor tabulado en el paso 0:*
    $v_0(4) = \frac{4}{5}\left[\frac{1}{2}(0.48) + \frac{1}{2}(1.68)\right] = 0.864.$

*   **Ejemplo 1.3.2 (Opción Lookback con reducción de estado):** 
    Parámetros: Heredados del Ejemplo 1.2.4 ($S_0=4, u=2, d=1/2, r=1/4, \tilde{p}=\tilde{q}=1/2$). Pago final: $M_3 - S_3$.
    *Valores tabulados en el paso 3 ($v_3(s, m)$):*
    $v_3(32, 32) = 0, \quad v_3(8, 16) = 8, \quad v_3(8, 8) = 0,$ 
    $v_3(2, 8) = 6, \quad v_3(2, 4) = 2, \quad v_3(0.50, 4) = 3.50.$
    *Valores tabulados en el paso 2 ($v_2(s, m)$):*
    $v_2(16, 16) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(8)\right] = 3.20.$
    $v_2(4, 8) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(6)\right] = 2.40.$
    $v_2(4, 4) = \frac{4}{5}\left[\frac{1}{2}(0) + \frac{1}{2}(2)\right] = 0.80.$
    $v_2(1, 4) = \frac{4}{5}\left[\frac{1}{2}(2) + \frac{1}{2}(3.50)\right] = 2.20.$
    *Valores tabulados en el paso 1 ($v_1(s, m)$):*
    $v_1(8, 8) = \frac{4}{5}\left[\frac{1}{2}(3.20) + \frac{1}{2}(2.40)\right] = 2.24.$
    $v_1(2, 4) = \frac{4}{5}\left[\frac{1}{2}(0.80) + \frac{1}{2}(2.20)\right] = 1.20.$
    *Valor tabulado en el paso 0 ($v_0(s, m)$):*
    $v_0(4, 4) = \frac{4}{5}\left[\frac{1}{2}(2.24) + \frac{1}{2}(1.20)\right] = 1.376.$

7. **Referencias cruzadas**
*   **Teorema 1.2.2 (Sección 1.2):** La base teórica para la ecuación de valoración hacia atrás (1.3.1) proviene de la demostración de completitud de mercado y replicación probada en la sección anterior.
*   **Ejemplo 1.2.4 (Sección 1.2):** El Ejemplo 1.3.2 referencia los resultados crudos de este ejemplo anterior para demostrar empíricamente que la agrupación de estados proporciona el mismo precio inicial de forma mucho más eficiente.
*   **Procesos de Markov (Sección 2.5):** El autor menciona conceptualmente que la base de esta optimización es la dependencia exclusiva de los estados actuales para definir la función $v_n$, una intuición que actuará como precursor para la definición teórica rigurosa de los *Procesos de Markov* que se desarrollará en el Capítulo 2.