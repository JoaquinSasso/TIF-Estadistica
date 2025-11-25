"""
Cálculo de la recta de regresión lineal según Teoría N°10.

Modelo: Y = beta0 + beta1 * X + e

En este ejemplo:
    X = diametro_mm
    Y = peso_g

Archivo esperado: "tomates_calidad.csv" en la misma carpeta, con
las columnas:
    - diametro_mm
    - peso_g

Salidas:
    - n, sumas y promedios
    - Sxx, Syy, Sxy
    - beta0_hat, beta1_hat
    - ecuación de la recta
    - SCE, SCR, SCT
    - s^2 (varianza residual), s
    - R^2
    - r (correlación)
"""

import math
import pandas as pd

CSV_PATH = "tomates_calidad_regenerado.csv"

def main():
    # Leer datos
    df = pd.read_csv(CSV_PATH)

    # Cambiá estos nombres si tus columnas se llaman distinto
    x = df["diametro_mm"].astype(float).values
    y = df["peso_g"].astype(float).values

    n = len(x)

    # --- 1) Sumas básicas ---
    sum_x  = x.sum()
    sum_y  = y.sum()
    sum_x2 = (x**2).sum()
    sum_y2 = (y**2).sum()
    sum_xy = (x*y).sum()

    x_bar = sum_x / n
    y_bar = sum_y / n

    # --- 2) Sxx, Syy, Sxy (definiciones de la teoría) ---
    Sxx = sum_x2 - (sum_x**2) / n
    Syy = sum_y2 - (sum_y**2) / n
    Sxy = sum_xy - (sum_x * sum_y) / n

    # --- 3) Coeficientes de la recta de regresión ---
    beta1_hat = Sxy / Sxx              # pendiente
    beta0_hat = y_bar - beta1_hat*x_bar  # ordenada al origen

    # Recta estimada: y_hat = beta0_hat + beta1_hat * x
    y_hat = beta0_hat + beta1_hat * x
    residuos = y - y_hat

    # --- 4) Sumas de cuadrados ---
    # SCT = suma (yi - y_bar)^2 = Syy
    SCT = Syy
    # SCE = suma (yi - y_hat)^2
    SCE = (residuos**2).sum()
    # SCR = SCT - SCE
    SCR = SCT - SCE

    # --- 5) Varianza residual y error estándar ---
    s2 = SCE / (n - 2)       # varianza de los errores estimada
    s  = math.sqrt(s2)       # desvío estándar residual

    # --- 6) R^2 y correlación r ---
    R2 = SCR / SCT
    r  = Sxy / math.sqrt(Sxx * Syy)

    # --- 7) Mostrar resultados ---
    print("=== DATOS BÁSICOS ===")
    print(f"n       = {n}")
    print(f"Σx      = {sum_x:.4f}")
    print(f"Σy      = {sum_y:.4f}")
    print(f"Σx²     = {sum_x2:.4f}")
    print(f"Σy²     = {sum_y2:.4f}")
    print(f"Σxy     = {sum_xy:.4f}")
    print(f"x̄      = {x_bar:.4f}")
    print(f"ȳ      = {y_bar:.4f}\n")

    print("=== SUMAS DE CUADRADOS (Teoría 10) ===")
    print(f"Sxx     = {Sxx:.4f}")
    print(f"Syy     = {Syy:.4f}")
    print(f"Sxy     = {Sxy:.4f}\n")

    print("=== COEFICIENTES DE LA RECTA ===")
    print(f"beta1̂ (pendiente)        = {beta1_hat:.6f}")
    print(f"beta0̂ (ordenada al origen) = {beta0_hat:.6f}")
    print(f"\nRecta estimada:")
    print(f"  ŷ = {beta0_hat:.4f} + {beta1_hat:.4f} * x\n")

    print("=== DESCOMPOSICIÓN DE SUMAS DE CUADRADOS ===")
    print(f"SCT (total)        = {SCT:.4f}")
    print(f"SCE (error)        = {SCE:.4f}")
    print(f"SCR (regresión)    = {SCR:.4f}\n")

    print("=== MEDIDAS DEL AJUSTE ===")
    print(f"s² (varianza error) = {s2:.6f}")
    print(f"s  (desvío error)   = {s:.6f}")
    print(f"R²                  = {R2:.4f}")
    print(f"r (correlación)     = {r:.4f}")

if __name__ == "__main__":
    main()
