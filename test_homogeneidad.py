"""
Prueba de homogeneidad para el diámetro de los tomates entre productores.

Ajustado para que las clases de diámetro se definan por CUANTILES
(en lugar de anchos iguales) y así evitar frecuencias esperadas < 5.

Hipótesis:
    H0: el diámetro de los tomates se comporta de manera homogénea
        entre los productores.
    H1: el diámetro NO se comporta de manera homogénea entre productores.

Archivo esperado: "tomates_calidad.csv"
    - "lote_proveedor"  (A, B, C, ...)
    - "diametro_mm"

Dependencias:
    pip install pandas numpy scipy matplotlib openpyxl
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2
import matplotlib.pyplot as plt

CSV_PATH = "tomates_calidad.csv"
ALFA = 0.05
Q_CLASES = 6       # número de clases por cuantiles (ajustable)

def main():
    # Leer datos
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["lote_proveedor", "diametro_mm"])

    # --- 1) Definir intervalos de diámetro POR CUANTILES ----------------
    # Cada clase tendrá aproximadamente N / Q_CLASES observaciones
    categorias = pd.qcut(
        df["diametro_mm"],
        q=Q_CLASES,
        duplicates="drop"   # por si hay muchos empates
    )

    # --- 2) Tabla de contingencia: clases x productor -------------------
    tabla = pd.crosstab(categorias, df["lote_proveedor"])

    print("=== Tabla de contingencia: diámetro (clases-cuantil) x productor (O_ij) ===")
    print(tabla, "\n")

    O = tabla.values.astype(float)
    r, c = O.shape
    productores = list(tabla.columns)
    intervalos = tabla.index.astype(str).tolist()

    filas = O.sum(axis=1).reshape(-1, 1)   # totales por fila
    cols = O.sum(axis=0).reshape(1, -1)    # totales por columna
    N = O.sum()

    # --- 3) Frecuencias esperadas bajo H0 -------------------------------
    E = filas @ cols / N

    # --- 4) Estadístico chi-cuadrado ------------------------------------
    chi2_stat = ((O - E) ** 2 / E).sum()
    gl = (r - 1) * (c - 1)
    chi2_crit = chi2.ppf(1 - ALFA, gl)
    p_valor = chi2.sf(chi2_stat, gl)

    # --- 5) Construir tabla resumen Obs/Esp + totales -------------------
    filas_tabla = []
    for i in range(r):
        row_data = []
        for j in range(c):
            obs = O[i, j]
            esp = E[i, j]
            row_data.extend([obs, esp])
        row_data.append(filas[i, 0])  # total fila
        filas_tabla.append(row_data)

    cols_tabla = []
    for prod in productores:
        cols_tabla.extend([f"{prod}_obs", f"{prod}_esp"])
    cols_tabla.append("Total_fila")

    tot_row = []
    for j in range(c):
        col_obs = O[:, j].sum()
        col_esp = E[:, j].sum()
        tot_row.extend([col_obs, col_esp])
    tot_row.append(N)

    filas_tabla.append(tot_row)
    index_tabla = intervalos + ["Total"]

    df_resumen = pd.DataFrame(filas_tabla, columns=cols_tabla, index=index_tabla)
    df_resumen = df_resumen.round(2)

    print("=== Tabla resumen Obs/Esp (cuantiles) ===")
    print(df_resumen, "\n")

    # Exportar tabla para diapositivas (opcional, igual que antes)
    df_resumen.to_csv("tabla_homogeneidad_cuantiles.csv", encoding="utf-8-sig")
    try:
        df_resumen.to_excel("tabla_homogeneidad_cuantiles.xlsx", sheet_name="Homogeneidad")
    except Exception as e:
        print("Aviso: no se pudo guardar Excel (¿falta openpyxl?). Error:", e)

    fig, ax = plt.subplots(figsize=(len(df_resumen.columns)*1.2,
                                    len(df_resumen)*0.4 + 1.5))
    ax.axis("off")

    table = ax.table(
        cellText=df_resumen.values,
        rowLabels=df_resumen.index,
        colLabels=df_resumen.columns,
        loc="center",
        cellLoc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.1, 1.3)

    plt.tight_layout()
    plt.savefig("tabla_homogeneidad_cuantiles.png", dpi=300)
    plt.close()

    print("Archivos generados:")
    print("  - tabla_homogeneidad_cuantiles.csv")
    print("  - tabla_homogeneidad_cuantiles.xlsx")
    print("  - tabla_homogeneidad_cuantiles.png\n")

    # --- 6) Resultado del test -----------------------------------------
    print("=== Dócima de homogeneidad (chi-cuadrado con cuantiles) ===")
    print(f"X^2 calculado               = {chi2_stat:.3f}")
    print(f"Grados de libertad          = {gl}")
    print(f"X^2 crítico (1-alfa)        = {chi2_crit:.3f}  (alfa = {ALFA:.2f})")
    print(f"p-valor                     = {p_valor:.4f}\n")

    min_E = E.min()
    num_E_lt5 = (E < 5).sum()
    print(f"Frecuencia esperada mínima  = {min_E:.2f}")
    print(f"Nº de celdas con E_ij < 5   = {num_E_lt5}\n")

    if chi2_stat > chi2_crit:
        print("Conclusión:")
        print("  Como X^2 calculado > X^2 crítico, se RECHAZA H0.")
        print("  → El diámetro de los tomates NO se comporta de forma homogénea")
        print("    entre los productores.")
    else:
        print("Conclusión:")
        print("  Como X^2 calculado <= X^2 crítico, NO se rechaza H0.")
        print("  → No hay evidencia estadística suficiente, con este nivel de")
        print("    significación, para afirmar que los diámetros difieran entre productores.")

if __name__ == "__main__":
    main()
