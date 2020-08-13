# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:14:28 2020

@author: julie
"""

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