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
    l.append((1,7))
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

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

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

###############################################################
#                             MAIN                            #
###############################################################

def principale(n,edges):
    is_edge_connected(n,edges)
    odd_nodes = odd_vertices(n,edges)
    o = create_edges_odd_impair(odd_nodes)
    ll = odd_vertices(n,o)
    return ll

print(principale(8,list_edges))
    