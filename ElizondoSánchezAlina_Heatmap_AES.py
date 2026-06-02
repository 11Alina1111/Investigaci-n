#=======================================================
#Gráfico en heatmap
#Estudiante: Alina Elizondo Sánchez
#=======================================================
import numpy as np
import matplotlib.pyplot as plt

##Datos de los paises y sus porcentajes
paises = ["Argentina", "Bahamas", "Barbados", "Belice",
          "Bolivia", "Brasil", "Chile","Colombia",
          "Costa Rica", "República Dominicana", "Ecuador", "El Salvador",
          "Guatemala", "Guyana", "Haití", "Honduras",
          "Jamaica", "México", "Nicaragua", "Panamá",
          "Paraguay", "Perú", "Suriname", "Trinidad y Tobago",
          "Uruguay", "Venezuela"]

porcentaje = ["34,55%", "17.79%", "25.68%", "20.27%",
              "12.97%", "32.21%", "32.48%", "54.96%",
              "23.87%", "25.41%", "22.52%", "22.34%",
              "9.95%", "4.68%", "2.70%", "10.50%",
              "24.32%", "26.58%", "25.00%", "53.15%",
              "36.89%", "56.67%", "2.70%", "15.99%",
              "44.86%","15.54%"]
#***************************************************************
##Conversión 
porcentajes = [float(p.replace("%", "").replace(",", ".")) for p in porcentaje]

##Ordenar de mayor a menor
orden = np.argsort(-np.array(porcentajes))
paises_ordenados = [paises[i] for i in orden]
porcentajes_ordenados = [porcentajes[i] for i in orden]
porcentaje_texto = [porcentaje[i] for i in orden]
#***************************************************************

## Heatmap
harvest = np.array(porcentajes_ordenados).reshape(-1, 1)

fig, ax = plt.subplots(figsize=(8, len(paises)*0.4))
im = ax.imshow(harvest, cmap="YlOrRd", aspect="auto")
#***************************************************************

##Etiquetas
ax.set_yticks(np.arange(len(paises_ordenados)), labels=paises_ordenados, fontsize = 12, fontweight= 'bold')
ax.set_xticks([])
ax.set_xlabel("")

##Texto centrado para cada celda
for i in range(len(paises_ordenados)):
    color_texto = "white" if porcentajes_ordenados[i] > np.mean(porcentajes_ordenados) else "black"
    ax.text(0, i, porcentaje_texto[i], ha="center", va="center", color=color_texto, fontsize=10,fontweight='bold')
#***************************************************************

##Barra de color
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("Porcentaje (%)", rotation=-90, va="center", fontsize=12, fontweight ='bold')
fig.tight_layout()

#***************************************************************
##Mostrar gráfico
plt.show()