# ==============================================================
#   REGRESIÓN LINEAL DESDE CERO + SUPUESTOS ORDENADOS
# ==============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy.stats import shapiro, pearsonr
import scipy.stats as stats

plt.style.use("default")

# --------------------------------------------------------------
# 1) CARGAR CSV
# --------------------------------------------------------------

df = pd.read_csv("tomates_calidad_regenerado.csv")

# Usaremos diametro_mm para explicar peso_g
X = df["diametro_mm"].values
Y = df["peso_g"].values
n = len(df)

# --------------------------------------------------------------
# 2) AJUSTE DEL MODELO OLS
# --------------------------------------------------------------

X_sm = sm.add_constant(X)   # agrega intercepto
model = sm.OLS(Y, X_sm).fit()

print("=== RESUMEN DEL MODELO OLS ===\n")
print(model.summary())

# --------------------------------------------------------------
# 3) SUPUESTO 1: LINEALIDAD
# --------------------------------------------------------------

# A) Gráfico solo con puntos
plt.figure(figsize=(7,5))
plt.scatter(X, Y, alpha=0.7, label="Datos")
plt.xlabel("Diámetro (mm)")
plt.ylabel("Peso (g)")
plt.title("SUPUESTO 1: Linealidad – Solo los puntos")
plt.legend()
plt.show()

# B) Puntos + recta estimada
plt.figure(figsize=(7,5))
plt.scatter(X, Y, alpha=0.7, label="Datos")
plt.plot(X, model.predict(X_sm), linewidth=2, label="Recta estimada")
plt.xlabel("Diámetro (mm)")
plt.ylabel("Peso (g)")
plt.title("SUPUESTO 1: Linealidad – Recta ajustada")
plt.legend()
plt.show()

# C) Residuos vs Ajustados
residuos = model.resid
ajustados = model.fittedvalues

plt.figure(figsize=(7,5))
plt.scatter(ajustados, residuos)
plt.axhline(0, color="black")
plt.xlabel("Valores ajustados")
plt.ylabel("Residuos")
plt.title("SUPUESTO 1: Linealidad – Residuos vs Ajustados")
plt.show()

# --------------------------------------------------------------
# 4) SUPUESTO 2: NORMALIDAD DE LOS ERRORES
# --------------------------------------------------------------

# Histograma
plt.figure(figsize=(7,5))
plt.hist(residuos, bins=10, edgecolor="black")
plt.title("SUPUESTO 2: Normalidad – Histograma de residuos")
plt.xlabel("Residuo")
plt.ylabel("Frecuencia")
plt.show()

# QQ-Plot
stats.probplot(residuos, dist="norm", plot=plt)
plt.title("QQ-Plot")
plt.show()

# Shapiro-Wilk
W, p_shapiro = shapiro(residuos)
print("\n=== SUPUESTO 2: Normalidad (Shapiro-Wilk) ===")
print(f"W = {W:.4f},  p-value = {p_shapiro:.4f}")

# --------------------------------------------------------------
# 5) SUPUESTO 3: HOMOCEDASTICIDAD
# --------------------------------------------------------------

bp_test = het_breuschpagan(residuos, X_sm)
bp_stat, bp_pvalue = bp_test[0], bp_test[1]

print("\n=== SUPUESTO 3: Homocedasticidad (Breusch-Pagan) ===")
print(f"BP statistic = {bp_stat:.4f},  p-value = {bp_pvalue:.4f}")

# --------------------------------------------------------------
# 6) SUPUESTO 4: INDEPENDENCIA DE LOS ERRORES
# --------------------------------------------------------------

dw = sm.stats.stattools.durbin_watson(residuos)
print("\n=== SUPUESTO 4: Independencia (Durbin-Watson) ===")
print(f"Durbin-Watson = {dw:.4f}")

plt.figure(figsize=(7,5))
plt.plot(residuos, marker="o")
plt.axhline(0, color="black")
plt.title("Residuos ordenados – chequeo de independencia")
plt.xlabel("Índice de observación")
plt.ylabel("Residuo")
plt.show()

# --------------------------------------------------------------
# 7) MEDIDAS DEL AJUSTE
# --------------------------------------------------------------

R2 = model.rsquared
SSE = sum(residuos**2)
Se2 = SSE / (n - 2)
Se = np.sqrt(Se2)

print("\n=== MEDIDAS DEL AJUSTE ===")
print(f"R² = {R2:.4f}")
print(f"SSE = {SSE:.4f}")
print(f"S_e^2 = {Se2:.4f}")
print(f"S_e = {Se:.4f}")

# --------------------------------------------------------------
# 8) CORRELACIÓN ENTRE X Y Y
# --------------------------------------------------------------

r, p_r = pearsonr(X, Y)

print("\n=== CORRELACIÓN PEARSON ===")
print(f"r = {r:.4f},  p-value = {p_r:.4e}")
print("Equivale al test de pendiente en la regresión simple.")
