from PIL import Image
import pytesseract
import re
from collections import defaultdict
from pprint import pprint
from a_star import Graph
import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt
import string

img_name = 'matrix2.png'
img_str = pytesseract.image_to_string(Image.open(img_name), config='digits').strip()

# Construir matriz a partir de la cadenas, solo digitos
adj_matrix = []
for line in img_str.splitlines():
    nums = line.split(' ')
    row = []
    for i in nums:
        row.append(int(re.sub("[^0-9]", "", i)))
    adj_matrix.append(row)

adj_matrix = [[0, 1, 3,7], [0, 0, 0, 5], [0, 0, 0, 12], [0, 0, 0, 0]]

adj_list = defaultdict(list)
edges = set()
node_names = list(string.ascii_uppercase)

# Construir lista de adyacencia dada la matriz de ady.
for i, v in enumerate(adj_matrix, 0):
    for j, u in enumerate(v, 0):
        if u != 0 and frozenset([i, j]) not in edges:
            edges.add(frozenset([i, j]))
            adj_list[node_names[i]].append((node_names[j], u))

path_found = Graph(adj_list).a_star_algorithm('A', node_names[len(adj_matrix)-1])

if path_found is not None:
    print('Path found: {}'.format(path_found))

    G = nx.from_numpy_matrix(np.array(adj_matrix), create_using=nx.DiGraph)
    
    node_labels = {}
    color_map = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = j = 0

    # Colorear nodos del camino encontrado
    for node in G.nodes():
        node_labels[node] = letters[i]
        
        if letters[i] in path_found:
            j += 1
            node_labels[node] += str(j)
            if path_found.index(letters[i]) == 0: # Nodo inicial
                color_map.append('g')
            elif path_found.index(letters[i]) == len(path_found) - 1: #Nodo final
                color_map.append('r')
            else: # Otro nodo del camino
                color_map.append('y')
            
        else:
            color_map.append('b')

        i += 1

    edge_labels = nx.get_edge_attributes(G, "weight")
    
    j = 0
    edge_colors = []
    for e in edge_labels:
        if j < len(path_found) - 1 and (e[0] == letters.index(path_found[j]) and e[1] == letters.index(path_found[j + 1])):
            edge_colors.append('r')
            j += 1
        else:
            edge_colors.append('#000000')
            
    layout = nx.spring_layout(G)

    nx.draw(G, layout, with_labels = False, node_color = color_map)
    
    nx.draw_networkx_edge_labels(G, pos = layout, edge_labels = edge_labels)
    nx.draw_networkx_edges(G, layout, edge_color=edge_colors)

    nx.draw_networkx_labels(G, layout, node_labels, font_size = 12, font_color = 'w')

    plt.show()
else:
    print('Path does not exist')



