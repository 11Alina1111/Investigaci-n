# Universidad Estatal a Distancia
# Carrera de Sistemas de Información en Salud
# 2025-5-03574 Investigación en Sistemas de Información en Salud I
# Práctica Formativa. Elaboración de un gráfico de bosque o "forest plot" por medio de Python
# Programador: Lic. Iván M. Rodríguez Soriano
#Estudiante: Alina Elizondo Sánchez
# Objetivo: Demostrar, por medio de la elaboración de un gráfico de bosque o “forest plot”, el conocimiento y dominio del lenguaje Python para la visualización de datos e información estadística.

# Elaboración de gráfico de bosque o "forest plot" utilizando datos simulados. Se van a comparar el efecto de 10 intervenciones tecnológicas sobre un desenlace clínico (mejora en adherencia al tratamiento) y se utilizan como medidas los odds ratios (OR) con intervalos.

#1) Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#2) Semillero
np.random.seed(42) #semillero
intervenciones = [
    "App móvil", "Recordatorios SMS", "Telemedicina", "Chatbot", "Portal paciente",
    "Wearables", "Educación digital", "Videollamadas", "Monitoreo remoto", "Gamificación"
]

#3) Generación de los OR y los errores estándar:
# Vamos a simular 10 valores OR utilizando una distribución normal, los parámettros son:
   # loc=1.2 -> media de la distribución (el valor esperado del OR).
   # scale=0.4 -> desviación estandar (la variabilidad).
   # size=10 -> cantidad de estudios simulados.
   # np.round(..., 2): -> redondeo de decimales.
# Adicionalmente, se calculan los intervalos de confianza o IC:
   # IC_inf es el intervalo de confianza inferior o límite inferior para cada OR.
   # IC_sup es el intervalo de confianza superior o límite superior para cada OR.   
OR = np.round(np.random.normal(loc=1.2, scale=0.4, size=10), 2)
errores = np.round(np.random.uniform(0.1, 0.3, size=10), 2)
IC_inf = np.round(OR - errores, 2)
IC_sup = np.round(OR + errores, 2)

#4) Creación del DataFrame utilizando los datos simulados:
# Primero vamos a definir la estructura del DataFrame utilizando pandas.
# El contenido de las llaves {} define las columnas y sus respectivos valores.

df = pd.DataFrame({
    'Intervención': intervenciones, #definición del contenido desde la lista de intervenciones
    'OR': OR,#valores simulados para cada intervención.
    'IC_inf': IC_inf,#limites inferiores
    'IC_sup': IC_sup #Limites superiores
}).sort_values(by='OR') #ordena el dataframe de mayor a menor

#5 Creación del gráfico de bosque: matplotlib.
# Vamos a definir la figura "fig" y el eje "ax" dond se dibujará el gráfico.
# Ahora trabajaremos directamente en la visualización del gráfico:
   # ax.errobar(...) dibuja los puntos con las barras de error horizontales, esto representa los IC.
   # df['OR'] define los valores de los OR simulados en el eje X.
   # df['Intervención'] define los nombres de los recursos tecnológicos como valores en el eje Y.
   # xerr=[...] define el error horizontal (IC) como el resultado del siguiente cálculo:
      # del OR - IC_inf, para el lado izquierdo.
      # IC_sup - OR, para el lado derecho.
   # fmt='o' define el estilo del marcador, en este caso un círculo para cada punto.
   # color='darkblue' define el color del punto central que representa la estimación puntual.
   # color='lightblue' define el colro de las barras de error (IC).
   # capsize=5 define el tamaño de las "alas" al final de las barras de error. 
fig, ax = plt.subplots(figsize=(9, 6)) #tamaño del gráfico en pulgadas
fig.patch.set_facecolor("#4227F5") #Fondo
ax.set_facecolor("#07CCEA") #Fondo donde está el gráfico
ax.errorbar(df['OR'], df['Intervención'], 
            xerr=[df['OR'] - df['IC_inf'], df['IC_sup'] - df['OR']],
            fmt='*', color='orange', ecolor='green', capsize=9, markersize = 16)#markersize= define el tamaño de marcador *

#6 Insertar la línea de referencia (OR = 1.0):
# Vamos a insertar en el gráfico una línea de referencia visual.
# ax.axvline(x=1.0,...) dibuja una línea vertical en el valo X = 1.0 del eje horizontal.
# Un OR = 1.0 representa la ausencia de efecto, para la interpretación debe considerar que:
   # OR > 1 indica que el efecto de la intervención es positivo.
   # OR < 1 indica que el efecto de la intervención es negativo.
   # OR = 1 indica que no hay diferencia significativa entre la intervención y el control.
# color= define el color de la línea
# linestyle= definición estilo de la línea 
# label='Sin efecto' asigna una etiqueta para incluir en la leyenda del gráfico.

ax.axvline(x=1.0, color='red', linestyle=':', label='Línea de referencia (OR = 1.0)')

#7 Insertar las etiquetas y otra configuración de estilo
# Elementos del gráfico 

ax.set_xlabel('Odds Ratio (con IC 95%)') #etiqueta al eje horizontal
ax.set_title('Efecto de Intervenciones en Salud Digital sobre Adherencia') #Título
ax.legend() #leyenda de gráfico
plt.tight_layout() #márgenes y espaciado gráfico
plt.show() #renderizar y mostrar resultado
