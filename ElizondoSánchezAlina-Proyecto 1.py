#Importar librerías
import networkx as nx
from pyvis.network import Network

# 1. Cargar y leer el archivo RIS.

archivo = "Investigación.ris"                          # Definimos una variables "archivo" e indicaresmo la ruta del archivo RIS. IMPORTANTE: NO CAMBIAR EL NOMBRE NI SU UBICACIÓN DE ALMACENAMIENTO.
with open(archivo, "r", encoding = "utf-8") as f:                   # Indicamos que se abra el archivo en modo lectura, "r", usando la codificación utf-8.
    contenido = f.read()                                            # Bloque with garantiza que el archivo se cierre automáticamente despúes de leerlo.                                                      # Utilizamos la variables "f" para representar el archivo RIS.                                                                # Utilizamos contenido = f.read() para que Python lea todo el contenido y lo guarde como una cadena de texto dentro de la variable "contenido"

# 2. Separar los registros y extraer las palabras claves (KW) del archivo.

registros = contenido.strip().split("ER  -")                        # Como todo el contenido es una cadena de texto, debemos dividirlo en registros individuales y para eso utilizaremos el delimitador "ER -".
temas_por_articulo = []                                             # Crea una lista vacía en donde se almacenarán los conjuntos de palabras clave (KW) de cada artículo. 
                                                                    # De esta forma se evita la duplicidad de elementos dentro de los registros.
for registro in registros:                                          # Repite la operación previa split("ER -") para cada registro, donde "registro" representa un bloque de texto con metadados de un artículo.
    lineas = registro.strip().split("\n")                           # Hace dos cosas: 1. Elimina los espacios en blanco al rededor del registro y 2. Divide el registro en líneas individuales para analizarlas una por una.
    palabras_clave = []                                             # Crea una lista vacía en donde se almacenarán las plabras clave de cada artículo.

    for linea in lineas:                                            # Indica a Python que recorra línea por línea cada registro.
        if linea.startswith("KW  - "):                              # Primera condición si. Aquí se indica que si encuentra en la línea una plabra clave ejecute la siguiente acción:
            kw = linea.replace("KW  - ", "").strip()                # elimina el prefijo "KW -" y limpia los espacios adicionales.
            if kw:                                                  # Segunda condición si. Aquí se indica que si KW NO esta vacía, es decir, si hay información en ese campo, ejecute la siguiente acción:
                palabras_clave.append(kw.lower())                   # agrega la información (la palabra clave) a la lista en minúscula. 
                                                                    # Esto se hace para normalizar y evistar duplicados como por ejemplo "Science" vs "science".
    if palabras_clave:                                              # Tercera condición si. Aquí se indica que si se encontraron palabras claves, se ejecute la siguiente acción:
        temas_por_articulo.append(set(palabras_clave))              # se conviertan en un conjunto ("set") para eliminar duplicados dentro de un mismo artículo y se agregue al "conjunto temas_por_articulo".


# 3. Construir la red de coocurrencias, es decir, la frecuencia conjunta de las unidades temáticas.

G = nx.Graph()                                                      # Crea un gráfico no dirigido sobre al cual vamos a ingresar ciertos parámetros.
for conjunto in temas_por_articulo:                                 # Recorre cada conjunto de palabras clave extraídas de un artículo.
    for tema1 in conjunto:                                          # Itera sobre cada tema dentro del conjunto, esto será el primer nodo de la conexión.
        for tema2 in conjunto:                                      # Itera nuevamente sobre el mismo conjunto para comparar tema1 con tema2, este será el segundo nodo de la conexión.
            if tema1 != tema2:                                      # Primera condición si. Básicamente es una condición para evitar que un nodo se conecte consigo mismo (autoconexión).
                if G.has_edge(tema1, tema2):                        # Segunda condición si. Verifica si ya existe una conexión entre esos dos temas en el gráfico y evita duplicar enlaces.
                    G[tema1][tema2]["weight"] += 1                  # Si el enlace ya existe, incrementa su peso en 1, este peso se utiliza para configurar el grosor del enlace.
                else:                                               # Ingresamos una excepción, es decir, se las condiciones anteriores no se cumple, se debe ejercuar la siguiente acción:
                    G.add_edge(tema1, tema2, weight=1)              # si no existe el enlace, lo crea con peso inicial 1 (que se indicó anteriormente).


# 4. Ajustes de atributos en los nodos y enlaces

for nodo in G.nodes():                                              # Recorre todos los nodos del gráfico G, donde cada nodo representa un tema extraido de los artículos.
    grado = G.degree(nodo)                                          # Se calcula el grado del nodo, es decir, cuántos enlaces tiene con otros nodos.
    G.nodes[nodo]["size"] = 10 + grado * 2                          # Asigna un valor al atributo "size" del nodo donde "10 + grado *2" el tamaño base mínimo (10) y el incremento proporcional a la conectividad (grado *2). Este atributo es utilizado por Pyvis para determinar el tamaño visual del nodo en el mapa.

for u, v, datos in G.edges(data=True):                              # Recorre todos los enlaces del gráfico G, donde "u" y "v" son los dos nodos conectados y "datos" es un diccionario con los atributos del enlace (p. e. "weight").
    peso = datos["weight"]                                          # Esta línea extrae el peso del enlace. El peso representa cuántas veces los temas u y v han coocurrido en artículos.
    datos["title"] = f"Coocurrencias: {peso}"                       # Por este método se añade un atributo "title" al enlace. Este texto se mostrará como un tooltip al pasar el cursor sobre la visualización interactiva.
    datos["width"] = 1 + peso                                       # Por este método se ajusta el grosor del enlace en función del peso. La fórmula "1 + peso" asegura que todos los enlaces sean visibles (mínimo grosor 1) y que los más frecuentes se vean más gruesos.


# 5. Crear visualización interactiva con Pyvis

net = Network(height="1500px",                                      # Crea un objeto "Network" de Pyvis con las siguientes características: height = "1200px" es la altura del mapa.
              width="50%",                                         # Indica que la visualización ocupe todo el ancho posible.
              notebook=False,                                       # Indica que no se está trbajando dentro de un Jupyter Notebook (oto lenguaje de programación común para Pyvis).
              bgcolor="#ffffff",                                    # Define el color de fondo, en este caso blanco.
              font_color="black")                                   # Define el color de la letra, en este caso negro.
net.barnes_hut()                                                    # Aplica el algoritmo Bernes-Hut para distribuir los nodos en el espacio. Simula las fuerzas físicas (atracción y repulsión) para evitar que los nodos se amontonen.
net.from_nx(G)                                                      # Esta función importa el gráfico G creado con NetworkX al objeto "net" de Pyvis. También convierte los nodos, enlaces y atributos en elementos interactivos para la visualización.

# 6. Personalización de los nodos

for nodo in net.nodes:                                              # Recorre todos los nodos del objeto "net" que representan la red visual en Pyvis. Cada nodo es un diccionario con los atributos "id", "size", "color", etc.
    nodo["title"] = f"Tema: {nodo['id']}"                           # Asigna un título emergente (tooltip) al nodo, "id" contiene el nombre del tema (p. e. "gaia" o "modernity").
    nodo["color"] = "#00F900"                                       # Define el color de fondo del nodo, en este caso verde claro.
    nodo["shape"] = "dot"                                           # Define la forma del nodo, en este caso como un punto circular "dot".


# 7. Resaltar los temas destacados

temas_destacados = {                                                # Crea un diccionario donde cada "clave" es el nombre de un tema (en minúsculas). Cada valor es otro diccionario con atributos visuales y semánticos.
    "access": {"color": "#FF0F0F", "tag": "access"},     # Este fragmento contine y define los atributos de cada tema destacado:  
    "health": {"color": "#0018F0", "tag": "health"},                    # como su nombre ("actor-network theory"),
    "health services": {"color": "#03F0F8", "tag": "health services"},          # el color ("color"),
    "telehealth": {"color": "#F5DD27", "tag": "telehealth"},  
    "chronic deseases": {"color": "#F8058F", "tag": "chronic deseases"},      # y su etiqueta ("tag") abreviada reconocible del enfoque teórico.
    "medical informatics applications": {"color": "#F4F805", "tag": "medical informatics applications"},
    "patient satisfaction": {"color": "#4A05F8", "tag": "patient satisfaction"}, # El propósito de este fragmento de código es definir los temas claves con colores y etiquetas.

}                                                                  
for nodo in net.nodes:                                              # Recorre todos los nodos del objeto "net", que representa la red visual generada con Pyvis.
    tema = nodo["id"].lower()                                       # Extrae el identificador del nodo (el nombre del tema) y lo convierte a minúsculas. Esto garantiza la comparación con temas_destacados.
    if tema in temas_destacados:                                    # Verifica si el tema actual está en el diccionario "temas_destacados". Si lo está, se le aplican atributos visuales y semánticos especiales.
        tag = temas_destacados[tema]["tag"]                         # Extrae la etiqueda "tag" asociada al tema destacado (p. e. "ANT" para "actor-network theory").
        nodo["color"] = temas_destacados[tema]["color"]             # Asigna el color especial definido para este tema. Sobrescribe el color de base previamente asignado.
        nodo["size"] += 250                                         # Aumenta significamente el tamaño del nodo. Esto lo hace visualmente prominente en la red.
        nodo["title"] += f"\n Tema destacado: {nodo['id']}\n Tag: {tag}"    # Añade información adicional al tooltip del nodo: indica que es un tema destacado, y muestra su etiqueta corta.
        nodo["group"] = tag                                         # Asigna el nodo a un grupo temático basado en su etiqueta. Pyvis puede usar esto para aplicar estilos o filtros por grupo.
        nodo["label"] = f"{nodo['id']} ({tag})"
        nodo["font"]={"size" :50}                                                         # Modifica la etiqueta visible del nodo en gráfico. Añade la abreviatura entre paréntesis.

#Destacar un tema de forma arbitraria
nodo_principal = "access"
for nodo in net.nodes:
    if nodo["id"].lower() == nodo_principal:
        nodo["color"] = "F54927" 
        nodo["size"] += 65 
        nodo["shape"] = "star" 
        nodo["title"] += "\n nodo_principal"
        nodo["label"] = f"{nodo['id']} (Nodo principal)"
        nodo["font"] = {"size": 60, "color": "F5CC27"}
        
# 8. Exportar visualización del gráfio a un archivo HTML

net.write_html("mapa_red_temática_telemedicina.html")                     # Genera un archivo HTML con la visualización de la red temática. El archivo se guarda con el nombre "mapa_red_temática_telemedicina.html" en el directorio actual.
print("Mapa generado: abre 'mapa_red_temática_telemedicina.html' en tu navegador.")   # Muestra un mensaje en la consola para indicar que el archivo fue creado exitosamente. También sugiere al usuario abrir el archivo en su navegador para explorar la red.



