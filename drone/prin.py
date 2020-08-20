# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:19:32 2020

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

###############################################################
#                          VARIABLES                          #
###############################################################

list_odd_node = []
list_nodes = []
list_edge = []
list_pair_edge = []
list_weight_new_pair = []
pair_return = []
eulerian_circuit = []

###############################################################
#                             GRAPH                           #
###############################################################

def display_part_of_graph(around):
    return ox.graph_from_address("14411 Pierrefonds Blvd, Pierrefonds, Quebec H9H 1Z2, Canada",dist = around, network_type="drive_service")
   
def set_undirected():
    number_node = graph.number_of_nodes()
    edges = [(u,v,w['length']) for u,v,w in graph.edges(data = True)]
    list_nodes = list(graph.nodes())
    return edges, number_node, list_nodes

###################################################### 
graph = ox.get_undirected(display_part_of_graph(150))#
ox.plot_graph(graph,show=True)
#nx.draw(graph, with_labels = True)                   #
######################################################

'''remplit la list avec les noeuds qui ont des degrees impairs'''
def filling_odd_list(list_odd_node):
    deg = nx.degree(graph)
    for node in graph.nodes():
        if deg[node] % 2 != 0:
            list_odd_node.append(node)
    return list_odd_node

###############################################################
#                         GENERATE PAIR                       #
###############################################################

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
    min = nx.dijkstra_path(graph,list_odd_nodes[0],list_odd_nodes[1])
    for i in range(len(list_pair_edge)):
        if nx.dijkstra_path(graph,list_pair_edge[i][0],list_pair_edge[i][1]) <= min:
            min = nx.dijkstra_path(graph,list_pair_edge[i][0],list_pair_edge[i][1])
    pair_return.append((min[0],min[-1],min))
    list_odd_nodes.remove(min[0])
    list_odd_nodes.remove(min[-1])
    if len(list_odd_nodes) != 0:
        remove_pair_in_list(list_pair_edge,min[0],min[-1])
        return choice_best_new_pair(list_pair_edge,list_odd_nodes)
    return pair_return

'''met en place le nouveau poids de chaque nouvelle pair'''
def set_up_dist(best_pair_list):
    tmp = []
    somme = 0.0
    for pair in best_pair_list:
        somme = 0.0
        tmp = []
        for j in range(len(pair[2]) - 1):
            info = graph.get_edge_data(pair[2][j],pair[2][j + 1])
            tmp.append(info[0]['length'])
        for i in range(len(tmp)):
            somme += tmp[i]
        pairx = list(pair)
        pairx.pop(-1)
        pairx.append(somme)
        pair = tuple(pairx)
        list_weight_new_pair.append(pair)
    return list_weight_new_pair
        
###############################################################
#                        FINAL FUNCTIONS                      #
###############################################################

'''donne la list finale de tous les edges'''
def final_list():
    deg = nx.degree(graph)
    edges, n, list_nodes = set_undirected()
    odd_nodes = filling_odd_list(list_odd_node)
    possible_pair = generate_pair_possible(odd_nodes)
    best_pair_list = choice_best_new_pair(possible_pair,odd_nodes)
    print("Nouvelles pairs construites:\n",best_pair_list)
    dist = set_up_dist(best_pair_list)
    print()
    print("Distance set up aux new pairs:\n",dist)
    graph.add_edges_from(dist)
    list_final = dist + edges
    return list_final,n,list_nodes
    edges, n = set_undirected()
    odd_nodes = filling_odd_list(list_odd_node)
    possible_pair = generate_pair_possible(odd_nodes)
    best_pair_list = choice_best_new_pair(possible_pair,odd_nodes)
    print("Nouvelles pairs construites:\n",best_pair_list)
    dist = set_up_dist(best_pair_list)
    print()
    print("Distance set up aux new pairs:\n",dist)
    print()
    print("edges:\n", len(edges))
    print(nx.is_eulerian(graph))
    graph.add_edges_from(dist)
    list_final = dist + edges
    return list_final

def find_eulerian_path():
    if nx.is_eulerian(graph) == True:
        eulerian_circuit = list(nx.eulerian_circuit(graph))
    return eulerian_circuit

def hier():
    list_final, n, list_nodes = final_list()
    curr_path = [list_nodes[0]]
    circuit = []
    
    while curr_path:
        curr_v = curr_path[-1]
    
###############################################################
#                             MAIN                            #
###############################################################


if __name__ == "__main__":
    hier()
    circuit = find_eulerian_path()
    print()
    print("Circuit eulerien:", circuit)
    print()
    
    