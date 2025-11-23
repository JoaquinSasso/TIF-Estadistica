"""
Muestra los 10 tomates con menor diámetro.

Requisitos:
- Archivo "tomates_calidad.csv" en la misma carpeta.
- Columnas: al menos "id_tomate" y "diametro_mm".
"""

import pandas as pd

def main():
    # Leer el CSV
    df = pd.read_csv("tomates_calidad_regenerado.csv")

    # Ordenar por diámetro ascendente
    df_ordenado = df.sort_values(by="diametro_mm", ascending=True)

    # Tomar los 10 más chicos
    top10 = df_ordenado.head(10)

    # Mostrar algunas columnas útiles
    columnas = [col for col in [
        "id_tomate",
        "diametro_mm",
        "peso_g",
        "lote_proveedor",
        "categoria_calidad",
        "defecto"
    ] if col in top10.columns]

    print("=== 10 tomates con menor diámetro ===")
    print(top10[columnas].to_string(index=False))

if __name__ == "__main__":
    main()
