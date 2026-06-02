#Ejemplo práctico taller #3
#Escalas de Likert
#Descripción: 
#Estudiante: Alina Elizondo Sánchez
#############################
#Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#1.	Simular los datos de estudiantes con respuestas tipo 
# escala de Likert de 1 a 5 sobre los temas indicados en el caso
np.random.seed(60)# todos los valores que haga este en el rango de 0 a 60( más aleatoridad equilibrada)

#Se crea un dataframe con pandas como tabla estructurada
df = pd.DataFrame({ 
    ##lista de 50 indicadores tipo "E1", "E2". Donde np.random.randint(1, 6, 55) genera 55 valores aleatorios entre 1 y 5.
    ##Es decir el 1 y 6 significan propiamente la escala de Likert ( Muy desacuerdo, desacuerdo....)
    "Estudiante": [f"E{i+1}" for i in range(55)],# Sumar un 1 a cada estudiante. El 55 es por los 55 estudiantes entrevistados
    "Confía en la tecnología": np.random.randint(1, 6, 55),
    "Prefiere atención presencial": np.random.randint(1, 6, 55),
    "Usa apps de salud": np.random.randint(1, 6, 55),
    "Le preocupa la privacidad": np.random.randint(1, 6, 55),
    "Recomendaría apps de salud": np.random.randint(1, 6, 55)
})

##2. Cuenta de likerts con lambda
## df.iloc[:, 1:] selecciona todas las columnas menos la primera, por ser de valor no numérico.
## apply(...) aplica una función específica a cada columna por medio del método "lambda":
## x.value_counts() cuenta cuántas veces aparece cada valor.
## sort_index() ordena los resultados por valor de 1 a 5.
## .T transpone las filas y las columnas.
## .fillna(0) rellena con ceros cualquier celda vacía, útil si algún ítem no recibió respuesta.

likert_counts = df.iloc[:, 1:].apply(lambda x: x.value_counts().sort_index()).T.fillna(0)

#Gráfico divergente( tiene valores negativos y positivos)
#Se crea mediante pandas
#Dataframe que almacena las frecuencias
# -likert_counts extrae los conteos de respuestas 1 y 2 desde likert_counts, los multiplica por -1 para que reflejen desacuerdo o
# actitud negativa y se grafiquen a la izquierda del eje central.
divergent = pd.DataFrame()
divergent["Muy en desacuerdo"] = -likert_counts[1]
divergent["En desacuerdo"] = -likert_counts[2]
##Asigna la frecuencia neutral
divergent["Neutral"] = likert_counts[3]
## Asigna las frecuencias de las respuestas positivas
##al lado derecho
divergent["De acuerdo"] = likert_counts[4]
divergent["Muy de acuerdo"] = likert_counts[5]

#3. Creación del gráfico divergente
## kind="barh" crea un gráfico de barras horizontales.
## staked=True aplica las respuestas para cada ítem.
## colormap="coolwarm" aplica una paleta de colores de tonos fríos (negativos) a cálidos (positivos).
## figsize=(10,6) define el tamaño (en pulgadas) del gráfico.
## plt.axvline(0, color='black', linewidth=0.8) dibuja una línea vertical en el eje X en la posición 0.
divergent.plot(kind="barh", stacked=True, colormap="ocean", figsize=(10, 7))
plt.axvline(0, color='black', linewidth=0.8)

#4. Estilos para el gráfico
## plt.rcParams.update({'font.size': 16}) cambiar tamaño de letra
## plt.title() añade un título descriptivo al gráfico.
## fontweight='bold') #aplicar negrita 
## plt.xlabel() añade un título al eje X.
## plt.ylabel() añade un título al eje Y.
## plt.ylegend() añade una leyenda al gráfico.
##plt.xticks(fontsize = 14) Aumentar el tamaño de los
##plt.yticks(fontsize = 14) ejes "x" y "y"
## plt.tight_layout() ajusta los márgenes. *Es mejor no modificarlo.
## plt.show() muestra el gráfico en la pantalla.
plt.rcParams.update({'font.size': 16})
plt.title("Gráfico divergente de respuestas Likert",fontweight='bold')
plt.xlabel("Frecuencia (negativa a positiva)",fontsize= 14 )
plt.ylabel("Ítems", fontsize= 14)
plt.legend(title="Respuesta", bbox_to_anchor=(1.05, 1), loc='upper left',)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.tight_layout()
plt.show()
