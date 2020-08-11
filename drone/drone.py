# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np
import matplotlib.pyplot as plt
from networkx import *
ox.config(use_cache=True, log_console=True)
ox.__version__



graph = ox.graph_from_place("Montreal, QC, Canada",  network_type="drive_service")

fig,_ = ox.plot_graph(graph, node_zorder=4, node_color='w', bgcolor='k')
print(graph)
'''nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True,
        node_geometry=True,
        fill_edge_geometry=True)
'''

nodes, gdf_edges = ox.graph_to_gdfs(graph, nodes=True)

# list of lats and lngs
lngs = gdf_edges.head().centroid.map(lambda x: x.coords[0][0])
lats = gdf_edges.head().centroid.map(lambda x: x.coords[0][1])

print(nodes, "\n")
print(gdf_edges, "\n")
print(lngs, "\n")
print(lats, "\n")
# the lat, lng at the spatial center of the graph
lng, lat = gdf_edges.unary_union.centroid.coords[0]
center_point = lat, lng

node_id = list(graph.nodes())[0]
node2 = list(graph.nodes())[7]


#print(node_id, "\n")
#print(nodes)

print(graph.nodes[304699073])
print(node2)
#graph.nodes[node_id]['y']

#shortestPath = nx.shortest_path(G, source= list(G.nodes())[10], target=list(G.nodes())[0], weight="10")
#node_colors = ["blue" if n in shortestPath else "red" for n in G.nodes()]
#pos = nx.spring_layout(G)
#nx.draw_networkx_nodes(G, pos=pos)
#nx.draw_networkx_edges(G, pos=pos)



'''route = nx.shortest_path(graph,
                         node_id,
                         node2,
                         weight='length')
ox.plot_graph_route(graph, route, fig_height=100, fig_width=10)

#construction d'un graph
G = Graph()
G.add_nodes_from([0,1,2,3,4])
G.add_edges_from([(0,1),(1,0),(1,2),(2,1),(2,3),(3,2),(3,4),(4,3),(1,3)])
draw(G)
plt.show()'''

visited = []

def dfs(graph,node):
    global visited
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n)


dfs(graph, node_id)
print(visited, "\n")


""" Détermine le prochain sommet marqué """
def SommetSuivant(T, S_marques) :
    L = T[-1]
    n = len(L)
    min = False
    for i in range(n):
        if not(i in S_marques):
            if L[i]:
                if not(min) or L[i][0] < min:
                    min = L[i][0]
                    marque = i
    return marque


""" Ajoute une ligne supplémentaire au tableau """
def ajout_ligne(T,S_marques,Graphe):
    L = T[-1]
    n = len(L)
    Lnew = L.copy()
    # sommet dont on va étudier les voisins
    S = S_marques[-1]
    # la longueur du chemin associé
    long = L[S][0]
    for j in range(n) :
        if j not in S_marques:
            poids = Graphe[S][j]
            if poids :
                if not(L[j]):
                    Lnew[j] = [long + poids, S]
                else :
                    if long + poids < L[j][0]:
                        Lnew[j] = [long + poids, S]
    T.append(Lnew)
    S_marques.append(SommetSuivant(T, S_marques))
    return T, S_marques


""" Calcule le tableau de l’algorithme de Dijkstra """
def calcule_tableau(Graphe, depart):
    n = len(Graphe)
    T=[[False] *n]
    T[0][depart] = [depart, 0]

    S_marques = [depart]
    while len(S_marques) < n:
        T, S_marques = ajout_ligne(T, S_marques, Graphe)
    return T

""" Détermine le plus court chemin entre depart et arrivee dans
le Graphe"""
def plus_court_chemin(Graphe, depart, arrivee):
    n = len(Graphe)
    T = calcule_tableau(Graphe,depart)
    fin = [arrivee]
    while fin[-1] != depart :
        fin.append(T[-1][fin[-1]][1])
    fin.reverse()
    return fin

Graphe = [[ 0, 2, 5, False, 3, False, False ],
[ 2, 0, 2, 1, False, False, 8 ],
[ 5, 2, 0, 1, 4, 2, False ],
[ False, 1, 1, 0, False, False, 5 ],
[ 3, False, 4, False, 0, False, False ],
[ False, False, 2, False, False, 0, 1 ],
[ False, 8, False, 5, False, 1, False ]]
print(len(Graphe))



