# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 11:04:45 2020

@author: julie
"""


import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from networkx import *
from math import inf
ox.config(use_cache=True, log_console=True)
ox.__version__

G=nx.Graph()
name_nodes = {1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7"}
list_edges = [(1,2),(2,3),(3,4),(4,5),(5,7),(2,4),(2,6),(6,5),(1,4),(5,7)]
lines = ["1 2 2", "2 3 4" ,"3 4 5","4 5 4","5 7 7","2 4 3","2 6 6","6 5 8"]
H=nx.relabel_nodes(G,name_nodes)
H.add_nodes_from([1,2,3,4,5,6,7])
H.add_edges_from(list_edges)

print("Nodes of graph: ")
print(H.nodes())
#print("Edges of graph: ")
#print(H.edges(data = True))
nx.draw(H, with_labels = True)
g = nx.parse_edgelist(lines, nodetype = int, data=(('weight',float),))
#print(g.nodes())
#print(g.edges(data = True))

visited = []
list_tmp = []
list_edges_parser = []
deg = nx.degree(g)

print("Degree des noeuds: ")
print(deg)
print(deg[4])

def dfs(graph,node):
    global visited
    global count
    global list_edges_visited
    global list_tmp
    global list_edges
    
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            if n not in visited:
                list_tmp.append((node, n,))
                print(node, " -> ", n, "\n")
                dfs(graph,n)
                
def compararaison(edges_tmp, edges_init):
    for i in range(len(edges_init)):
        comparaison1 = edges_init[i]
        a = edges_init[i][1]
        b = edges_init[i][0]
        comparaison2 = (a,b)
        if comparaison1 in edges_tmp or comparaison2 in edges_tmp:
            print("dedans")
        else:
            list_edges_parser.append(comparaison1)
            
def nombre_de_noeuds_impair():
    compteur_noeud_impair = 0
    for i in range(len(deg) + 1):
        if i % 2 != 0:
            compteur_noeud_impair = compteur_noeud_impair + 1
    print(compteur_noeud_impair)
    

dfs(H,1)
print(list_tmp)
compararaison(list_tmp, list_edges)
print(list_edges_parser)
nombre_de_noeuds_impair()
