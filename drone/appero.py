# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:21:16 2020

@author: julie
"""
import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

edge_list = [(3735398272, 7403380099, 14.988), (3735398272, 5272829472, 5.636), (5272829472, 2625939755, 67.029), (5272829472, 2625939755, 101.267), (7403380099, 1511544620, 58.423), (7403380099, 7403380101, 33.039), (7403380100, 7403380101, 47.11), (7403380100, 7403380101, 142.62199999999999), (7403380100, 1511544620, 61.469)]
#edge_list = [(0, 1, -1), (0, 2, 4), (1, 2, 3), (1, 3, 2), (1, 4, 2), (3, 2, 5),(3, 1, 1),(4, 3, -3) ]
###############################################################
#                       SUPPORT FUNCTIONS                     #
###############################################################

'''renvoie une liste des noeuds qui sont de degrees impairs'''
def odd_vertices(n, edge_list):
    res = []
    res2 = []
    somme = 0
    somme2 = 0
    visited = []
    visited2 = []
    '''regarde pour le premier element du couple'''
    for i in range(0, len(edge_list)):
        somme = 0
        if edge_list[i][0] not in visited:
            for j in range(len(edge_list)):
                if edge_list[i][0] == edge_list[j][0] or edge_list[i][0] == edge_list[j][1]:
                    somme += 1
            visited.append(edge_list[i][0])
            if somme % 2 != 0:
                    res.append(edge_list[i][0])
    '''regarde pour le deuxieme element du couple'''
    for i in range(0, len(edge_list)):
        somme2 = 0
        if edge_list[i][1] not in visited2:
            for j in range(len(edge_list)):
                if edge_list[i][1] == edge_list[j][0] or edge_list[i][1] == edge_list[j][1]:
                    somme2 += 1
            visited2.append(edge_list[i][1])
            if somme2 % 2 != 0:
                    res2.append(edge_list[i][1])
    list_odd_nodes = res + res2
    list_odd_nodesx = list(set(list_odd_nodes))
    return list_odd_nodesx

def get_node_list(edge_list):
    list_node = []
    visited = []
    for i in range(len(edge_list)):
        if edge_list[i][0] not in visited:
            list_node.append(edge_list[i][0])
        if edge_list[i][1] not in visited:
            list_node.append(edge_list[i][1])
    return list(set(list_node))
            

###############################################################
#                            DIJKSTRA                         #
###############################################################

def get_weight(a,b,edge_list):
    for edge in edge_list:
        if edge[0] == a and edge[1] == b:
            return edge[2]
        if edge[1] == a and edge[0] == b:
            return edge[2]
    return 0
        
def get_neighbours(edge_list, u):
    list_neighbours = []
    for i in range(len(edge_list)):
        if u == edge_list[i][0]:
            list_neighbours.append(edge_list[i][1])
        if u == edge_list[i][1]:
            list_neighbours.append(edge_list[i][0])
            
    return list(set(list_neighbours))
    

def dijkstra(src, list_node, edge_list):
    dist = dict()
    previous = dict()
    
    for vertex in list_node:
        dist[vertex] = float("inf")
        previous[vertex] = None
    dist[src] = 0
    
    Q = set(list_node)
    
    while len(Q) > 0:
        u = min(Q, key=lambda vertex: dist[vertex])
        Q.discard(u)
        
        if dist[u] == float('inf'):
            break
        neighbours = get_neighbours(edge_list, u)
        
        for node in neighbours:
            weigth = get_weight(u,node,edge_list)
            alt = float(dist[u]) + weigth
            if alt < dist[node]:
                dist[node] = alt
                previous[node] = u
    return dist, previous

def dijkstra_path(src, target, list_node, edge_list):
    dist, prev = dijkstra(src, list_node, edge_list)
    path = []
    
    debut = target
    while debut != src:
        path.append(debut)
        debut = prev[debut]
    path.append(src)
    pathx = path.copy()
    pathx.reverse()
    return pathx

###############################################################
#                         GENERATE PAIR                       #
###############################################################

'''genere toutes les paires possibles'''
def generate_pair_possible(list_odd_nodes):
    list_pair_edge = []
    for i in range(len(list_odd_nodes)):
        for j in range(i,len(list_odd_nodes)):
            if i != j or j != i:
                if (list_odd_nodes[i],list_odd_nodes[j]) not in list_pair_edge or (list_odd_nodes[j],list_odd_nodes[i]) not in list_pair_edge:
                    list_pair_edge.append((list_odd_nodes[i],list_odd_nodes[j]))
    return list_pair_edge


###############################################################
#                             MAIN                            #
###############################################################

def solve(is_oriented, num_vertices, edge_list):
    list_odd_nodes = odd_vertices(num_vertices,edge_list)
    possible_pair = generate_pair_possible(list_odd_nodes)
    node = get_node_list(edge_list)
    print("List odd node:\n", list_odd_nodes)
    print("Possible pair:\n", possible_pair)
    print("Dijktra:\n", dijkstra_path(list_odd_nodes[0],list_odd_nodes[2],node,edge_list))
solve(True,7,edge_list)
