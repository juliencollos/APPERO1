# -*- coding: utf-8 -*-
"""
@author: julien collos, hicham sekkat, theo dolphin
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
list_edges = [(1,2),(2,3),(3,4),(4,5),(5,7),(2,4),(2,6),(6,5)]
list_final_edges = []
lines = ["1 2 2", "2 3 4" ,"3 4 5","4 5 4","5 7 7","2 4 3","2 6 6","6 5 8"]
H=nx.relabel_nodes(G,name_nodes)
H.add_nodes_from([1,2,3,4,5,6,7])
H.add_edges_from(list_edges)


'''renvoie une liste des noeuds qui sont de degrees impairs'''
def odd_vertices(n, edges):
    L = [0] * n
    res = []
    for i in range(0, len(edges)):
        L[edges[i][0]] += 1
        L[edges[i][1]] += 1
    for i in range(n):
        if (L[i] % 2 == 1):
            res.append(i)
    return res

'''creer des edges entre les noeuds impairs'''
def create_edges_odd_impair(list_odd_nodes):
    l = list_edges.copy()
    for i in range(0,len(l) - 1,2):
        if i > len(list_odd_nodes) - 1 or i + 1 > len(list_odd_nodes) - 1:
            return l
        l.append((list_odd_nodes[i], list_odd_nodes[i + 1]))
    return l
        
def parcours(i, vect, adj, n):
    vect[i] = True
    for j in range(n):
        if vect[j] == True:
            continue
        if adj[i][j] != 0 or adj[j][i] != 0:
            parcours(j, vect, adj, n)
        else:
            continue

def is_connected(n, edges):
    if n == 0:
        return True
    if n == 1:
        return True

    vect = [False] * n
    adj = [[0] * n for i in range(n)]

    for (i ,j) in edges:
        adj[i][j] = 1;

    parcours(0, vect, adj, n)

    for node in vect:
        if (node == False):
            return False
    return True

'''verifie si tous les edges sont bien connectes entre eux'''
def is_edge_connected(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    succ = [[] for a in range(n)]
    for (a,b) in edges:
        succ[a].append(b)
        succ[b].append(a)
    tmp = [False] * n
    init = edges[0][0]
    tmp[init] = True
    tmp1 = [init]
    while tmp1:
        s = tmp1.pop()
        for d in succ[s]:
            if tmp[d]:
                continue
            tmp[d] = True
            tmp1.append(d)
    for a in range(n):
        if succ[a] and not tmp[a]:
            return False
    return True
'''regarde si le graph est eulerien'''
def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)
'''on regarde si on trouve un graphe eulerien'''
def is_eulerian_cycle(m, edges, cycle):
    if (len(edges) == 0 and len(cycle) == 0):
        return True
    if (len(edges) == 0 or len(cycle) == 0):
        return False
    cycle.append(cycle[0])
    verif = 1
    for i in range(len(cycle) - 1):
        for j in edges:
            if (j[0] == cycle[i] and j[1] == cycle[i + 1]):
                edges.remove(j)
                verif = 0
                break
            if (j[1] == cycle[i] and j[0] == cycle[i + 1]):
                edges.remove(j)
                verif = 0
                break
        if (verif == 1):
            return False
        verif = 1
    if (len(edges) == 0):
        return True
    return False
'''methode de : Hierholzer algorithm'''
def printCircuit(list_edges): 
    if len(list_edges) == 0: 
        return
    curr_path = [0] 
    circuit = [] 
   
    while curr_path: 
        curr_v = curr_path[-1] 
        if list_edges[curr_v]: 
            next_v = list_edges[curr_v].pop() 
            curr_path.append(next_v) 
        else: 
            circuit.append(curr_path.pop()) 
    for i in range(len(circuit) - 1, -1, -1): 
        print(circuit[i], end = "") 
        if i: 
            print(" -> ", end = "")

'''convert tuple en list, on en a besoin pour notre list de edges'''           
def convert_tuple_to_list(tuple): 
    return list(tuple)
'''convertis notre tupele de edge en list pour pouvoir aplliquer Hierholzer algorithm'''
def convert_edge_list(list_edges):
    for i in range(len(list_edges)):
        list_final_edges.append(convert_tuple_to_list(list_edges[i]))
    return list_final_edges

###############################################################
#                             MAIN                            #
###############################################################
    
if __name__ == "__main__":
    n = 8
    edges = list_edges
    is_edge_connected(n,edges)
    odd_nodes = odd_vertices(n,edges)
    new_list_edges = create_edges_odd_impair(odd_nodes)
    final = convert_edge_list(new_list_edges)
    printCircuit(final)

