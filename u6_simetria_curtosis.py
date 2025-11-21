"""
Unidad 6 – Simetría (asimetría) y curtosis (apuntamiento)
Este script calcula ambas medidas "a mano" usando las fórmulas de momentos centrales
que suelen aparecer en EDA:

Sea x1,...,xn una muestra.

1) Media muestral:
   x̄ = (1/n) Σ xi

2) Momento central de orden k (con divisor n):
   m_k = (1/n) Σ (xi - x̄)^k

3) Coeficiente de asimetría (simetría):
   g1 = m_3 / (m_2)^(3/2)

   Interpretación:
   - g1 ≈ 0  -> distribución aproximadamente simétrica
   - g1 > 0  -> sesgo a la derecha (cola derecha más larga)
   - g1 < 0  -> sesgo a la izquierda (cola izquierda más larga)

4) Coeficiente de curtosis (exceso de curtosis):
   g2 = m_4 / (m_2)^2 - 3

   Interpretación (exceso):
   - g2 ≈ 0  -> mesocúrtica (similar a Normal)
   - g2 > 0  -> leptocúrtica (más apuntada, colas más pesadas)
   - g2 < 0  -> platicúrtica (más achatada, colas más livianas)

Notas:
- Estas fórmulas usan divisor n, que es lo más común en la Unidad 6.
- Abajo también se calcula la versión "ajustada" (opcional) para referencia.
"""

import pandas as pd
import math

def central_moment(x, k):
    """m_k = (1/n) Σ (xi - x̄)^k"""
    n = len(x)
    mean = sum(x) / n
    return sum((xi - mean)**k for xi in x) / n

def skewness_g1(x):
    """g1 = m3 / m2^(3/2)"""
    m2 = central_moment(x, 2)
    m3 = central_moment(x, 3)
    return m3 / (m2 ** 1.5)

def kurtosis_excess_g2(x):
    """g2 = m4 / m2^2 - 3"""
    m2 = central_moment(x, 2)
    m4 = central_moment(x, 4)
    return m4 / (m2 ** 2) - 3

# --- Versiones ajustadas (opcional) ---
def skewness_adjusted(x):
    """
    Asimetría ajustada tipo Fisher-Pearson:
    G1 = sqrt(n*(n-1)) / (n-2) * g1
    """
    n = len(x)
    g1 = skewness_g1(x)
    if n < 3:
        return float("nan")
    return math.sqrt(n*(n-1)) / (n-2) * g1

def kurtosis_excess_adjusted(x):
    """
    Exceso de curtosis ajustado (unbiased approx):
    G2 = [(n-1)/((n-2)(n-3))] * [(n+1)g2 + 6]
    """
    n = len(x)
    g2 = kurtosis_excess_g2(x)
    if n < 4:
        return float("nan")
    return ((n-1)/((n-2)*(n-3))) * ((n+1)*g2 + 6)


def describe_shape(series, name):
    x = series.dropna().tolist()
    n = len(x)
    mean = sum(x)/n
    m2 = central_moment(x,2)
    m3 = central_moment(x,3)
    m4 = central_moment(x,4)

    g1 = skewness_g1(x)
    g2 = kurtosis_excess_g2(x)
    G1 = skewness_adjusted(x)
    G2 = kurtosis_excess_adjusted(x)

    print(f"\n=== {name} ===")
    print(f"n = {n}")
    print(f"media x̄ = {mean:.4f}")
    print(f"m2 = {m2:.6f}")
    print(f"m3 = {m3:.6f}")
    print(f"m4 = {m4:.6f}")
    print(f"g1 (asimetría) = {g1:.4f}")
    print(f"g2 (exceso curtosis) = {g2:.4f}")
    print(f"G1 ajustada (ref) = {G1:.4f}")
    print(f"G2 ajustada (ref) = {G2:.4f}")

    # interpretación corta
    if abs(g1) < 0.1:
        sim = "aprox. simétrica"
    elif g1 > 0:
        sim = "sesgo a la derecha"
    else:
        sim = "sesgo a la izquierda"

    if abs(g2) < 0.1:
        kur = "mesocúrtica (similar a normal)"
    elif g2 > 0:
        kur = "leptocúrtica (más apuntada)"
    else:
        kur = "platicúrtica (más achatada)"

    print(f"Interpretación: {sim}; {kur}.")


if __name__ == "__main__":
    # Cambiá el path si el CSV está en otro lado
    df = pd.read_csv("tomates_calidad.csv")

    describe_shape(df["diametro_mm"], "Diámetro (mm)")
    describe_shape(df["peso_g"], "Peso (g)")
