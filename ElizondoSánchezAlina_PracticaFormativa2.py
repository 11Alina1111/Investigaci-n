#PRÁCTICA FORMATIVA UNIDAD 4: ELABORACIÓN DE UN DIAGRAMA DE 
#DISPERSIÓN POR MEDIO DE PYTHON

##Estudiante:Alina Elizondo Sánchez
##Descripción de práctica: Creación de un diagrama de dispersión.
##Tomando en cuenta  datos ficticios, para representar la relación 
##entre las variables “Actividad física” y “Edad” de muestra ficticia 
##de 200 personas. 

##Objetivo: Visualizar cómo varía el tiempo semanal dedicada la actividad física según la edad y el género.

#___________________________________________________________
###Librerías
import pandas as pd
import numpy as np
#____________________________________________________

#___________________________________________________________
###Semilla para reproducibilidad
####Permite que cada cierto tiempo se repitan los resultados.
####En este caso en cada intervalo de 42 ocasiones
####El 200 indica el número de la muestra
np.random.seed(42)
n = 200
#____________________________________________________

#____________________________________________________
# Simular edades
# Igual que la línea anterior, simulamos 200 observaciones para la variable "edad" y definimos que cree valores 
# aleatorios entre los 18 y 79 años. Nota: el 80 no se incluye, si queremos incluirlo, debemos definir "81".
edades = np.random.randint(18, 80, size=n) 
#____________________________________________________
# Simular género (50% masculino, 50% femenino)
# Asignamos aleatoriamente el valor "masculino" o "femenino" con una proporción de 0.5, es decir el 50%.
generos = np.random.choice(['Masculino', 'Femenino'], size=n)

#_______________________________________________________________
#Simular minutos de actividad física con ligera diferencia por género
#Definición de parámetros de la simulación para forzar aleatoridad en la simulación de la actividad física
#semanal, de esta forma nuestros datos simulados serán más "reales".
#1)Se tiene como base "180 - edad" para
#indicar que entre más jóven la persona tienda a hacer más ejercicio
#2)Añadir "ruido aleatorio" con una distribución normal (media 0, desviación 20) esto sirve para que al visaulizar los datos se parezcan más a datos 
#reales y no se vea muy artificial.
#3)Definir np.maximun(0,...) para que no hayan valores negativos
actividad = np.maximum(0, 180 - edades + np.random.normal(0, 20, size=n))

#____________________________________________________
# Ajuste: supongamos que mujeres reportan ligeramente más actividad, entonces debemos indicar los siguiente:
actividad += np.where(generos == 'Femenino', 10, 0) # Esto ajusta los datos a favor de las mujeres.

#____________________________________________________
# Crear DataFrame
# Se crea una tabla con tres columnas: Edad, Género y Minutos de Actividad.
# Este es nuestra matriz básica para los datos.
df = pd.DataFrame({
    'Edad': edades,
    'Género': generos,
    'Minutos_Actividad': actividad
})

#____________________________________________________
#Importación de librería para crear gráficos.
import matplotlib.pyplot as plt

#____________________________________________________
#Personalización del gráfico
# Aplicación del estilo 
# Definición del tamaño del diagrama (pulgadas)
# La proporción 10, 6 es estándar; podemos modificarlo, pero la mayoría de las veces es un buen tamaño.
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))

# Aplicamos colores suaves para identificar el género
colores = {'Masculino': "#0189F8", 'Femenino': "#D4FD06"}

# Definir los parámetros de dispersión por género
# Primero, iteramos por cada género para que filtre el subconjunto correspondiente ("masculino" o "femenino").
# Segundo, dibuja los puntos para el diagrama ("scatter") con color y transparencia ("alpha").
# Tercer, añade las etiquetas para la leyenda. 
for genero in df['Género'].unique():
    subset = df[df['Género'] == genero]
    plt.scatter(subset['Edad'], subset['Minutos_Actividad'],
                alpha=0.6, label=genero, color=colores[genero])

# Inserta la línea de tendencia global
# Se calcula una regresión líneal entre las variabels "edad" y "minutos de actividad".
z = np.polyfit(df['Edad'], df['Minutos_Actividad'], 1) # Ajusta la regresión lineal (grado 1).
p = np.poly1d(z) # Crea una función polinómica a partir de los coeficientes.
plt.plot(df['Edad'], p(df['Edad']), color='white', linewidth=2, label='Tendencia global') # Dibuja la línea.

#____________________________________________________
#Elementos de estilo del gráfico
plt.title('Actividad física semanal según edad y género', fontsize=18,fontweight='bold') #Título de gráfico
plt.xlabel('Edad (años)', fontsize=15) #Eje x
plt.ylabel('Minutos de actividad física por semana', fontsize=14) #Eje y 
plt.legend(fontsize= 14) #leyenda del gráfico
plt.grid(False) #Permite activar (TRUE) o desactivar (FALSE) las líneas cuadrículas
plt.tight_layout() #márgenes y espaciado gráfico
plt.show() #Muestra gráfico en pantalla