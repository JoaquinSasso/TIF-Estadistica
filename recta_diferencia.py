"""
Intervalo de confianza 95% para la diferencia de medias (Mañana - Tarde)
dibujado sobre una recta numérica, preparado para diapositivas.

Archivo esperado: "tomates_calidad.csv" con columnas:
- "turno" (Mañana / Tarde)
- "peso_g"
"""

import math
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "tomates_calidad.csv"
Z_95 = 1.96

def ci_dif_medias_z(serie1, serie2, z=Z_95):
    # limpiar NA
    x1 = serie1.dropna()
    x2 = serie2.dropna()

    n1, n2 = len(x1), len(x2)
    m1, m2 = x1.mean(), x2.mean()
    s1, s2 = x1.std(ddof=1), x2.std(ddof=1)

    diff = m1 - m2
    se_diff = math.sqrt(s1**2 / n1 + s2**2 / n2)
    ci_inf = diff - z * se_diff
    ci_sup = diff + z * se_diff

    return diff, ci_inf, ci_sup, (m1, s1, n1), (m2, s2, n2)

def main():
    df = pd.read_csv(CSV_PATH)

    peso_maniana = df.loc[df["turno"] == "Mañana", "peso_g"]
    peso_tarde   = df.loc[df["turno"] == "Tarde",  "peso_g"]

    diff, ci_inf, ci_sup, stats_m, stats_t = ci_dif_medias_z(peso_maniana, peso_tarde)

    print("=== IC 95% para la diferencia de medias (Mañana - Tarde) ===")
    print(f"IC 95% = ({ci_inf:.3f} ; {ci_sup:.3f}) g")

    # --- Dibujar la recta numérica con el intervalo ---
    # Tamaño y resolución pensados para diapositivas
    fig, ax = plt.subplots(figsize=(12, 3.5), dpi=150)

    # Eje horizontal (recta numérica)
    ax.axhline(0, color="black", linewidth=1.5)

    # Intervalo IC como segmento grueso
    ax.hlines(
        y=0,
        xmin=ci_inf,
        xmax=ci_sup,
        color="tab:blue",
        linewidth=6,
        label="Intervalo de confianza 95%"
    )

    # Línea vertical en 0 (sin diferencia) más visible
    ax.vlines(
        0, -0.4, 0.4,
        color="gray",
        linestyle="--",
        linewidth=2,
        label="0 (sin diferencia)"
    )

    # Margen del gráfico
    margen = 0.25 * (ci_sup - ci_inf if ci_sup != ci_inf else 1.0)
    x_min = ci_inf - margen
    x_max = ci_sup + margen
    ax.set_xlim(x_min, x_max)

    # Quitar eje y, solo nos interesa la recta
    ax.get_yaxis().set_visible(False)

    ax.set_title(
        "Intervalo de confianza del 95% para la diferencia de medias (Mañana - Tarde)",
        fontsize=16,
        pad=15
    )

    # Anotaciones más grandes y separadas
    ax.text(ci_inf, 0.25, f"{ci_inf:.2f}", ha="center", va="bottom", fontsize=12)
    ax.text(ci_sup, 0.25, f"{ci_sup:.2f}", ha="center", va="bottom", fontsize=12)
    ax.text(diff, -0.3, f"diff = {diff:.2f}", ha="center", va="top", fontsize=12)
    ax.text(0, -0.55, "0", ha="center", va="top", fontsize=12, color="gray")

    # Leyenda más grande
    ax.legend(loc="upper left", fontsize=12)

    plt.tight_layout()

    # Si querés guardarlo directo como imagen para las diapositivas:
    # plt.savefig("IC_diferencia_medias_recta.png")

    plt.show()

if __name__ == "__main__":
    main()
