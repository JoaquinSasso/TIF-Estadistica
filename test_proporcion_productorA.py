"""
Test de hipótesis para la proporción de tomates defectuosos del productor A.

Planteo:
- H0: p = 0.15
- H1: p < 0.15
- Nivel de significación: alfa = 0.05 (95% confianza)
- Variable: defecto visible (Sí/No)
- Productor: A

Archivo esperado: "tomates_calidad.csv" en la misma carpeta, con columnas:
- "lote_proveedor" (A, B, C, ...)
- "defecto" ("Sí" / "No")
"""

import math
import pandas as pd

CSV_PATH = "tomates_calidad.csv"
P0 = 0.15          # proporción bajo H0
ALFA = 0.05        # nivel de significación
Z_CRITICO = -1.645 # cuantil para test unilateral a la izquierda (95% confianza)

def normal_cdf(z):
    """
    CDF de la Normal(0,1) usando la función error de math.
    Φ(z) = 0.5 * [1 + erf(z / sqrt(2))]
    """
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def main():
    # Leer base
    df = pd.read_csv(CSV_PATH)

    # Filtrar solo productor A
    df_A = df[df["lote_proveedor"] == "A"]

    n_A = len(df_A)
    x_A = (df_A["defecto"] == "Sí").sum()
    p_hat = x_A / n_A if n_A > 0 else float("nan")

    # Estadístico de prueba Z
    se = math.sqrt(P0 * (1 - P0) / n_A)
    z = (p_hat - P0) / se

    # p-valor (como H1: p < P0, usamos cola izquierda)
    p_valor = normal_cdf(z)

    # Decisión
    rechaza = z < Z_CRITICO

    print("=== Test de hipótesis para la proporción de defectuosos (Productor A) ===")
    print(f"H0: p = {P0:.2f}")
    print(f"H1: p < {P0:.2f}")
    print(f"Nivel de significación: alfa = {ALFA:.2f}\n")

    print("Datos del productor A:")
    print(f"  n_A (tamaño de muestra)     = {n_A}")
    print(f"  x_A (defectuosos)           = {x_A}")
    print(f"  p̂ (proporción muestral)    = {p_hat:.4f}\n")

    print("Cálculos del test (aprox. Normal):")
    print(f"  Error estándar bajo H0      = {se:.6f}")
    print(f"  Estadístico Z               = {z:.4f}")
    print(f"  Z crítico (cola izq, 5%)    = {Z_CRITICO:.4f}")
    print(f"  p-valor (cola izquierda)    = {p_valor:.4f}\n")

    if rechaza:
        print("Conclusión:")
        print("  Como Z < Z_crit (y p-valor < alfa), se RECHAZA H0.")
        print("  Con un 95% de confianza, hay evidencia de que la proporción de defectuosos")
        print("  del productor A es menor al 15%.")
    else:
        print("Conclusión:")
        print("  Como Z >= Z_crit (y p-valor >= alfa), NO se rechaza H0.")
        print("  Con esta muestra y un 95% de confianza, no hay evidencia suficiente para")
        print("  afirmar que la proporción de defectuosos del productor A sea menor al 15%.")

if __name__ == '__main__':
    main()
