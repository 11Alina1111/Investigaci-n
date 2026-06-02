import numpy as np
import pandas as pd

# Datos del CiteScore
citescores = [1.7, 5.2, 3.4, 1.0, 0.5, 5.4, 0.4, 8.9, 8.4, 2.7]

# Cálculos estadísticos
media = np.mean(citescores)
mediana = np.median(citescores)
rango = np.max(citescores) - np.min(citescores)
desviacion_estandar = np.std(citescores, ddof=1) # ddof=1 para muestra

# Mostrar resultados
print(f"Media: {media :.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Rango: {rango :.2f}")
print(f"Desviación estándar: {desviacion_estandar :.2f}")