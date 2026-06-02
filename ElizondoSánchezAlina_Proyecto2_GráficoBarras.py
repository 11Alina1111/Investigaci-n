#Proyecto 2- Telemedicina
#Gráfico de barras
#Descripción: Describe el acceso con Internet fija según región de 
# planificación 2024
#Estudiante: Alina Elizondo Sánchez

#############################
## Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

## Datos
regiones = ['Costa Rica', 'Central', 'Chorotega', 'Pacífico Central','Brunca','Huetar Caribe','Huetar Norte']
counts = [73.7, 79.5, 67.8, 62.8, 61.8, 65.3, 67.6]
bar_colors = ['tab:orange'] * len(regiones)

## Ordenar de mayor a menor
regiones, counts = zip(*sorted(zip(regiones, counts), key = lambda x: x[1], reverse = True))

## Posiciones en el eje Y
y_pos = np.arange(len(regiones))

## Gráfico de barras horizontales
bars = ax.barh(y_pos, counts, color=bar_colors, align='center')

## Etiquetas de eje
ax.set_yticks(y_pos, labels=regiones, fontsize = 12)

ax.invert_yaxis()  # Para que la primera región quede arriba
ax.set_xlabel('Porcentaje', fontsize = 16)
ax.set_ylabel('Región de planificación', fontsize = 16)
ax.spines['top'].set_visible(False) #quitar borde superior
ax.spines['right'].set_visible(False) #quitar borde derecho
## Etiquetas en las barras (a la derecha de cada barra)
ax.bar_label(bars, labels=[f"{c}%" for c in counts], padding=3,  fontsize = 14)

##Mostrar
plt.show()
