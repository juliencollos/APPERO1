# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:21:16 2020

@author: julien
"""
import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

pair_return = []
edge_list = [(3735398272, 7403380099, 14.988), (3735398272, 5272829472, 5.636), (5272829472, 2625939755, 67.029), (5272829472, 2625939755, 101.267), (7403380099, 1511544620, 58.423), (7403380099, 7403380101, 33.039), (7403380100, 7403380101, 47.11), (7403380100, 7403380101, 142.62199999999999), (7403380100, 1511544620, 61.469)]

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

'''supprime les pairs deja obetnue apres dijkstra'''
def remove_pair_in_list(list_pair_edge,a,b):
    tmp = list_pair_edge.copy()
    n = len(tmp)
    for i in range(n):
        if list_pair_edge[i][0] == a or list_pair_edge[i][1] == a or list_pair_edge[i][0] == b or list_pair_edge[i][1] == b:
            list_pair_edge.remove(list_pair_edge[i])
            return remove_pair_in_list(list_pair_edge,a,b)
        
'''genere la meilleure pair possible'''         
def choice_best_new_pair(list_pair_edge,list_odd_nodes,node,edge_list):
    min = dijkstra_path(list_odd_nodes[0],list_odd_nodes[1],node,edge_list)
    
    for i in range(len(list_pair_edge)):
        if dijkstra_path(list_pair_edge[i][0],list_pair_edge[i][1], node, edge_list) <= min:
            min = dijkstra_path(list_pair_edge[i][0],list_pair_edge[i][1], node, edge_list)
    pair_return.append((min[0],min[-1],min))
    list_odd_nodes.remove(min[0])
    list_odd_nodes.remove(min[-1])
    if len(list_odd_nodes) != 0:
        remove_pair_in_list(list_pair_edge,min[0],min[-1])
        return choice_best_new_pair(list_pair_edge,list_odd_nodes, node, edge_list)
    return pair_return


'''met en place le nouveau poids de chaque nouvelle pair'''
def set_up_dist(best_pair_list, edge_list):
    list_weight_new_pair = []
    tmp = []
    somme = 0.0
    for pair in best_pair_list:
        somme = 0.0
        tmp = []
        for j in range(len(pair[2]) - 1):
            info = get_weight(pair[2][j],pair[2][j + 1], edge_list)
            tmp.append(info)
        for i in range(len(tmp)):
            somme += tmp[i]
        pairx = list(pair)
        pairx.pop(-1)
        pairx.append(somme)
        pair = tuple(pairx)
        list_weight_new_pair.append(pair)
    return list_weight_new_pair

###############################################################
#                             MAIN                            #
###############################################################

def solve(is_oriented, num_vertices, edge_list):
    list_odd_nodes = odd_vertices(num_vertices,edge_list)
    
    node = get_node_list(edge_list)
    possible_pair = generate_pair_possible(list_odd_nodes)
    best_pair = choice_best_new_pair(possible_pair, list_odd_nodes, node, edge_list)
    dist = set_up_dist(best_pair, edge_list)
    
    
solve(True,7,edge_list)
