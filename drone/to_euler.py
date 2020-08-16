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
list_edges = [(1,2,1),(2,3,2),(3,4,3),(4,5,4),(5,7,5),(2,4,6),(2,6,7),(6,5,8)]
list_final_edges = []
pair_return = []
list_pair_edge = []
lines = ["1 2 2", "2 3 4" ,"3 4 5","4 5 4","5 7 7","2 4 3","2 6 6","6 5 8"]
H=nx.relabel_nodes(G,name_nodes)
H.add_nodes_from([1,2,3,4,5,6,7])
H.add_weighted_edges_from(list_edges)
list_edges_sans_poids = []
nx.draw(H, with_labels = True)


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



'''genere toute les pairs possibles'''
def generate_pair_possible(list_odd_nodes):
    for i in range(len(list_odd_nodes)):
        for j in range(i,len(list_odd_nodes)):
            if i != j or j != i:
                if (list_odd_nodes[i],list_odd_nodes[j]) not in list_pair_edge or (list_odd_nodes[j],list_odd_nodes[i]) not in list_pair_edge:
                    list_pair_edge.append((list_odd_nodes[i],list_odd_nodes[j]))
    return list_pair_edge

'''supprime les pairs deja obetnue apres dijkstra'''
def remove_pair_in_list(list_pair_edge,a,b):
    tmp = list_pair_edge.copy()
    n = len(tmp)
    for i in range(n):
        if list_pair_edge[i][0] == a or list_pair_edge[i][1] == a or list_pair_edge[i][0] == b or list_pair_edge[i][1] == b:
            list_pair_edge.remove(list_pair_edge[i])
            return remove_pair_in_list(list_pair_edge,a,b)
        
'''genere la meilleure pair possible'''         
def choice_best_new_pair(list_pair_edge,list_odd_nodes):
    min = nx.dijkstra_path(H,list_odd_nodes[0],list_odd_nodes[1])
    for i in range(len(list_pair_edge)):
        if nx.dijkstra_path(H,list_pair_edge[i][0],list_pair_edge[i][1]) <= min:
            min = nx.dijkstra_path(H,list_pair_edge[i][0],list_pair_edge[i][1])
    pair_return.append([min[0],min[-1]])
    list_odd_nodes.remove(min[0])
    list_odd_nodes.remove(min[-1])
    if len(list_odd_nodes) != 0:
        remove_pair_in_list(list_pair_edge,min[0],min[-1])
        return choice_best_new_pair(list_pair_edge,list_odd_nodes)
    return pair_return
            
    
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

'''convert tuple en list, on en a besoin pour notre list de edges'''           
def convert_tuple_to_list(tuple): 
    return list(tuple)

def convert_list_to_tuple(list): 
    return tuple(list)

'''convertis notre tupele de edge en list pour pouvoir aplliquer Hierholzer algorithm'''
def convert_edge_list(list_edges):
    for i in range(len(list_edges)):
        list_final_edges.append(convert_tuple_to_list(list_edges[i]))
    return list_final_edges

L = []
def convert_edge_tuple(tuples):
    for i in range(len(tuples)):
        L.append(convert_list_to_tuple(tuples[i]))
    return L
'''recupere juste le couple'''
def recupere_edges_sans_poids(list_edges):
    for i in range(len(list_edges)):
        list_edges_sans_poids.append((list_edges[i][0],list_edges[i][1]))
    return list_edges_sans_poids


###############################################################
#                             MAIN                            #
###############################################################
    

if __name__ == "__main__":
    n = 8
    edges = list_edges
    tmp = recupere_edges_sans_poids(edges)
    tmp1 = convert_edge_list(tmp)
    odd_nodes = odd_vertices(n,edges)
    olala = generate_pair_possible(odd_nodes)
    best_pair_list = choice_best_new_pair(olala,odd_nodes)
    best_pair_tuple = convert_edge_tuple(best_pair_list)
    result = edges + best_pair_tuple
    print(result)