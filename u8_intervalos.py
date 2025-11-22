"""
IC del 95% para la media del peso de los tomates
entre turno Mañana y Tarde (y diferencia de medias).

Suposiciones:
- Archivo "tomates_calidad.csv" en la misma carpeta.
- Columnas: "turno" (Mañana/Tarde), "peso_g".

Se usa un IC aproximado normal:
    IC = x̄ ± z * s / sqrt(n)
con z = 1.96 para 95% y s la desviación estándar muestral (ddof=1).
Con n >= 30 por grupo, la aproximación normal es muy buena.
"""

import math
import pandas as pd
import matplotlib.pyplot as plt

# --- Parámetros generales ---
CSV_PATH = "tomates_calidad.csv"
CONF_LEVEL = 0.95
Z_95 = 1.96  # cuantíl aproximado para 95% (N(0,1))

# --- Funciones auxiliares ---
def ci_media_z(serie, z=Z_95):
    """
    Calcula IC para la media usando distribución normal (z).
    Devuelve (media, inf, sup, n, s).
    """
    x = serie.dropna()
    n = len(x)
    mean = x.mean()
    s = x.std(ddof=1)  # desviación estándar muestral
    se = s / math.sqrt(n)  # error estándar
    ci_inf = mean - z * se
    ci_sup = mean + z * se
    return mean, ci_inf, ci_sup, n, s

def ci_dif_medias_z(serie1, serie2, z=Z_95):
    """
    IC del 95% para la diferencia de medias: mu1 - mu2, usando aproximación normal.

    Fórmula:
      diff = x̄1 - x̄2
      SE_diff = sqrt( s1^2/n1 + s2^2/n2 )
      IC = diff ± z * SE_diff
    """
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

# --- Cargar datos ---
df = pd.read_csv(CSV_PATH)

# Filtrar por turno
peso_maniana = df.loc[df["turno"] == "Mañana", "peso_g"]
peso_tarde   = df.loc[df["turno"] == "Tarde",  "peso_g"]

# --- IC para cada turno ---
mean_m, ci_m_inf, ci_m_sup, n_m, s_m = ci_media_z(peso_maniana)
mean_t, ci_t_inf, ci_t_sup, n_t, s_t = ci_media_z(peso_tarde)

# --- IC para la diferencia de medias (Mañana - Tarde) ---
diff_mt, ci_diff_inf, ci_diff_sup, stats_m, stats_t = ci_dif_medias_z(
    peso_maniana, peso_tarde
)

# --- Mostrar resultados numéricos en consola ---
print("=== Intervalos de confianza 95% para la media de peso (g) ===")
print(f"Turno MAÑANA (n = {n_m}):")
print(f"  media = {mean_m:.3f} g")
print(f"  s = {s_m:.3f} g")
print(f"  IC 95% = ({ci_m_inf:.3f} ; {ci_m_sup:.3f}) g\n")

print(f"Turno TARDE (n = {n_t}):")
print(f"  media = {mean_t:.3f} g")
print(f"  s = {s_t:.3f} g")
print(f"  IC 95% = ({ci_t_inf:.3f} ; {ci_t_sup:.3f}) g\n")

print("=== Intervalo de confianza 95% para la diferencia de medias (Mañana - Tarde) ===")
print(f"  diferencia de medias = {diff_mt:.3f} g")
print(f"  IC 95% diferencia = ({ci_diff_inf:.3f} ; {ci_diff_sup:.3f}) g")
print("  Si el IC incluye 0, no hay evidencia fuerte de diferencia en la media.")
print("  Si el IC está completamente por encima/debajo de 0, hay diferencia significativa.")

# --- Gráficas para interpretar el resultado ---

# 1) Boxplot de peso por turno
plt.figure(figsize=(6, 4))
df.boxplot(column="peso_g", by="turno")
plt.title("Peso de los tomates por turno")
plt.suptitle("")  # quita el título automático de pandas
plt.xlabel("Turno")
plt.ylabel("Peso (g)")
plt.tight_layout()
plt.show()

# 2) Gráfico de medias con IC 95%
labels = ["Mañana", "Tarde"]
means = [mean_m, mean_t]
# semi-amplitud del IC: media - límite inferior = media - ci_inf
ci_lower = [mean_m - ci_m_inf, mean_t - ci_t_inf]
ci_upper = [ci_m_sup - mean_m, ci_t_sup - mean_t]

plt.figure(figsize=(6, 4))
x_pos = range(len(labels))

# Barras de media
plt.bar(x_pos, means, yerr=[ci_lower, ci_upper], capsize=8)
plt.xticks(x_pos, labels)
plt.ylabel("Peso medio (g)")
plt.title("Medias de peso por turno con IC 95%")
plt.tight_layout()
plt.show()
