import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#PARTE 1

libros = [
    {"nombre": "Ciencia Ficción", "género": "Ficción", "autor": "Autor A", "año": 2020, "color": "#FF5733"},
    {"nombre": "Fantasía", "género": "Ficción", "autor": "Autor B", "año": 2018, "color": "#33FF57"},
    {"nombre": "Historia", "género": "No Ficción", "autor": "Autor C", "año": 2015, "color": "#3357FF"},
    {"nombre": "Biografía", "género": "No Ficción", "autor": "Autor D", "año": 2019, "color": "#FF33A1"},
    {"nombre": "Misterio", "género": "Ficción", "autor": "Autor A", "año": 2021, "color": "#A133FF"}
]

# Función para calcular la similitud de color en formato HEX
def color_similarity(color1, color2):
    rgb1 = np.array([int(color1[i:i+2], 16) for i in (1, 3, 5)])
    rgb2 = np.array([int(color2[i:i+2], 16) for i in (1, 3, 5)])
    return 1 - (np.linalg.norm(rgb1 - rgb2) / np.sqrt(3 * (255 ** 2)))

# Calcular la similitud entre libros
def calcular_similitud(libro1, libro2):
    peso_género = 0.3
    peso_autor = 0.2
    peso_año = 0.2
    peso_color = 0.3
    
    similitud_género = 1 if libro1["género"] == libro2["género"] else 0
    similitud_autor = 1 if libro1["autor"] == libro2["autor"] else 0
    similitud_año = 1 - abs(libro1["año"] - libro2["año"]) / max(libro1["año"], libro2["año"])
    similitud_color = color_similarity(libro1["color"], libro2["color"])
    
    return (peso_género * similitud_género) + (peso_autor * similitud_autor) + (peso_año * similitud_año) + (peso_color * similitud_color)

# Crear grafo de similitud
G = nx.Graph()
for libro in libros:
    G.add_node(libro["nombre"])

for i in range(len(libros)):
    for j in range(i + 1, len(libros)):
        similitud = calcular_similitud(libros[i], libros[j])
        if similitud > 0:  
            G.add_edge(libros[i]["nombre"], libros[j]["nombre"], weight=similitud)

# Dibujar el grafo
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
edges = G.edges(data=True)
weights = [edge[2]['weight'] * 10 for edge in edges] 

nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, edge_color="gray", width=weights)
plt.title("Similitud entre categorías de libros")
plt.show()

# Función para encontrar categorías similares
def categorias_similares(nombre_categoria, top_n=3):
    similitudes = []
    for libro in libros:
        if libro["nombre"] != nombre_categoria:
            similitud = calcular_similitud(next(l for l in libros if l["nombre"] == nombre_categoria), libro)
            similitudes.append((libro["nombre"], similitud))
    similitudes.sort(key=lambda x: x[1], reverse=True)
    return similitudes[:top_n]
