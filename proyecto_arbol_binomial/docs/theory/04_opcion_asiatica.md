1. **Concepto y contexto**
El Ejercicio 1.8 introduce una opción Asiática, la cual es un derivado financiero dependiente de la trayectoria (*path-dependent*) cuyo pago final se basa en el precio promedio de la acción durante la vida del contrato, en lugar de depender únicamente del precio final. El objetivo conceptual de este ejercicio es aplicar las técnicas de reducción computacional (vistas en la Sección 1.3) introduciendo una nueva variable de estado acumulativa (la suma de los precios pasados) para que el algoritmo de valoración hacia atrás siga siendo eficiente (Sección 1.6, pp. 22-23).

2. **Definiciones formales**
*   $S_0$: Precio inicial de la acción.
*   $u, d$: Factores de subida y bajada del precio de la acción, respectivamente.
*   $r$: Tasa de interés constante por período.
*   $\tilde{p}, \tilde{q}$: Probabilidades neutrales al riesgo.
*   $n$: Índice de tiempo o período.
*   $K$: Precio de ejercicio (*strike price*).
*   $S_k$: Precio de la acción en el instante $k$.
*   $Y_n$: Suma acumulada de los precios de la acción entre el instante cero y el instante $n$.
*   $v_n(s, y)$: Precio de la opción Asiática en el instante $n$, condicionado a que el precio actual de la acción es $S_n = s$ y la suma de precios acumulada es $Y_n = y$.
*   $\Delta_n(s, y)$: Número de acciones que debe mantener el portafolio replicante en el instante $n$ si $S_n = s$ e $Y_n = y$.

3. **Ecuaciones clave**
*(Nota: El autor no asigna números de ecuación explícitos dentro de este ejercicio específico. Se exponen las definiciones matemáticas formuladas en el enunciado con la notación exacta)*.
$$Y_n = \sum_{k=0}^n S_k$$
$$v_3(s, y) = \left(\frac{y}{4} - 4\right)^+$$

4. **Hipótesis y dominio de validez**
*   El ejercicio asume la validez de los parámetros estándar del modelo binomial presentados en el Ejemplo 1.2.1 ($0 < d < 1+r < u$).
*   Dado que el pago de la opción depende del promedio histórico, la reducción del modelo para fijar el precio requiere estrictamente incluir tanto el precio actual de la acción ($S_n$) como la suma histórica ($Y_n$). Omitir la variable $Y_n$ invalidaría el algoritmo, ya que la dependencia de la trayectoria impediría calcular el pago final correctamente sin conocer el camino completo de los lanzamientos de moneda.

5. **Teoremas y esquema de demostración**
No cubierto en esta sección (al tratarse de un ejercicio práctico de modelado, no introduce teoremas formales ni demostraciones matemáticas propias).

6. **Ejercicios de esta sección**
*   **Exercise 1.8 (Asian option):** Basado en el modelo de tres períodos del Ejemplo 1.2.1 donde $S_0=4$, $u=2$, $d=1/2$, $r=1/4$, y donde las probabilidades neutrales al riesgo resultan ser $\tilde{p}=\tilde{q}=1/2$. Se define $Y_n = \sum_{k=0}^n S_k$. Se considera una opción de compra Asiática (*Asian call option*) que expira en $n=3$ con precio de ejercicio $K=4$, cuyo pago final es $\left(\frac{Y_3}{4} - 4\right)^+$. Definiendo $v_n(s, y)$ como el precio de esta opción en el instante $n$ si $S_n = s$ e $Y_n = y$, el ejercicio pide exclusivamente:
    *   (i) Desarrollar un algoritmo para calcular $v_n$ recursivamente. En particular, escribir una fórmula para $v_n$ en términos de $v_{n+1}$.
    *   (ii) Aplicar el algoritmo desarrollado en (i) para calcular $v_0(4, 4)$, que es el precio de la opción Asiática en el instante cero.
    *   (iii) Proveer una fórmula para $\Delta_n(s, y)$, el número de acciones de la acción subyacente que deben mantenerse en el portafolio replicante en el instante $n$ si $S_n = s$ e $Y_n = y$.

7. **Referencias cruzadas**
*   **Sección 1.2 (Ejemplo 1.2.1):** El ejercicio importa directamente la estructura y los valores numéricos del árbol binomial planteado en este ejemplo básico.
*   **Sección 1.3 (Consideraciones Computacionales):** Este ejercicio aplica directamente el razonamiento expuesto en el Ejemplo 1.3.2 (Opción *Lookback*), requiriendo la agrupación de estados mediante una variable acumulativa adicional para evitar el cálculo de la complejidad exponencial de todas las trayectorias de la moneda.
*   **Capítulo 2 (Procesos de Markov):** La definición de las funciones $v_n(s,y)$ anticipa rigurosamente el uso de vectores de estado bidimensionales en los Procesos de Markov, que el autor formaliza matemáticamente en la Sección 2.5 y ejemplifica en los Ejercicios 2.13 y 2.14 con esta misma opción Asiática.