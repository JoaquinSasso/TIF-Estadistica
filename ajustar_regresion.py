import pandas as pd
import numpy as np

df = pd.read_csv("tomates_calidad.csv")

X = df["diametro_mm"].values

# Tomá a y b del modelo actual, o elegí unos razonables
a =  -200    # EJEMPLO
b =   4.5    # EJEMPLO

sigma = 5.0  # ruido relativamente chico → r alto y homocedástico

np.random.seed(42)  # para que sea reproducible
eps = np.random.normal(loc=0, scale=sigma, size=len(X))

df["peso_g"] = a + b * X + eps

df.to_csv("tomates_calidad_regenerado.csv", index=False)
