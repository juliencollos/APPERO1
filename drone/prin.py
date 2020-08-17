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


list_odd_node = []
list_edge = []
list_pair_edge = []
pair_return = []


###############################################################
#                             GRAPH                           #
###############################################################

def display_part_of_graph(around):
    return ox.graph_from_address("14411 Pierrefonds Blvd, Pierrefonds, Quebec H9H 1Z2, Canada",dist = around, network_type="drive_service")
   
def set_undirected(around):
    number_node = graph.number_of_nodes()
    edges = [(u,v,w['length']) for u,v,w in graph.edges(data = True)]
    return edges, number_node

###################################################### 
graph = ox.get_undirected(display_part_of_graph(500))#
ox.plot_graph(graph)                                 #
######################################################

def filling_odd_list(list_odd_node):
    deg = nx.degree(graph)
    for node in graph.nodes():
        if deg[node] % 2 != 0:
            list_odd_node.append(node)
    return list_odd_node

###############################################################
#                             PAIR                            #
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
    pair_return.append((min[0],min[-1],min))#donne en poids le chemin de Dijsktra
    list_odd_nodes.remove(min[0])
    list_odd_nodes.remove(min[-1])
    if len(list_odd_nodes) != 0:
        remove_pair_in_list(list_pair_edge,min[0],min[-1])
        return choice_best_new_pair(list_pair_edge,list_odd_nodes)
    return pair_return


###############################################################
#                        LIST FINAL EDGE                      #
###############################################################

def final_list(around):
    edges, n = set_undirected(around)
    odd_nodes = filling_odd_list(list_odd_node)
    possible_pair = generate_pair_possible(odd_nodes)
    best_pair_list = choice_best_new_pair(possible_pair,odd_nodes)
    return best_pair_list + edges 

###############################################################
#                             MAIN                            #
###############################################################

if __name__ == "__main__":
    final_list(500)

    