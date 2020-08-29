# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:19:32 2020

@author: julie
"""

import networkx as nx
import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

###############################################################
#                          VARIABLES                          #
###############################################################

list_odd_node = []
list_nodes = []
list_edge = []
list_edges_sans_poids = []
list_pair_edge = []
list_weight_new_pair = []
pair_return = []
eulerian_circuit = []
graph = nx.classes.multigraph.MultiGraph

###############################################################
#                             GRAPH                           #
###############################################################
def set_graph(is_oriented):
    if is_oriented == False:
         graph = ox.get_undirected(display_part_of_graph(120))
         ox.plot_graph(graph,show=True,node_size = 60,save=True)
         nx.draw(graph, with_labels = True)
         print("Strongly connected: False")
    else:
        graph = display_part_of_graph(400)
        ox.plot_graph(graph,show=True,node_size = 60,save=True)
        nx.draw(graph, with_labels = True)
        print("Strongly connected:", nx.is_strongly_connected(graph))
    return graph
        
             

def display_part_of_graph(around):
    return ox.graph_from_address("14411 Pierrefonds Blvd, Pierrefonds, Quebec H9H 1Z2, Canada",dist = around, network_type="drive_service")
   
def set_undirected(graph):
    number_node = graph.number_of_nodes()
    edges = [(u,v,w['length']) for u,v,w in graph.edges(data = True)]
    list_nodes = list(graph.nodes())
    return edges, number_node, list_nodes

'''remplit la list avec les noeuds qui ont des degrees impairs'''
def filling_odd_list(list_odd_node,graph):
    deg = nx.degree(graph)
    print(deg)
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
def choice_best_new_pair(list_pair_edge,list_odd_nodes,graph):
    min = nx.dijkstra_path(graph,list_odd_nodes[0],list_odd_nodes[1])
    
    for i in range(len(list_pair_edge)):
        if nx.dijkstra_path(graph,list_pair_edge[i][0],list_pair_edge[i][1]) <= min:
            min = nx.dijkstra_path(graph,list_pair_edge[i][0],list_pair_edge[i][1])
            print("je suis min",list_pair_edge[i][0])
    pair_return.append((min[0],min[-1],min))
    list_odd_nodes.remove(min[0])
    list_odd_nodes.remove(min[-1])
    if len(list_odd_nodes) != 0:
        remove_pair_in_list(list_pair_edge,min[0],min[-1])
        return choice_best_new_pair(list_pair_edge,list_odd_nodes,graph)
    return pair_return



'''met en place le nouveau poids de chaque nouvelle pair'''
def set_up_dist(best_pair_list,graph):
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
#                      GENERATE DICT NODES                    #
###############################################################

'''recupere la liste des edges sans le poids
   afin de pouvoir creer mon dictionnaire plus tard
'''
def recupere_edges_sans_poids(list_edges):
    for i in range(len(list_edges)):
        list_edges_sans_poids.append((list_edges[i][0],list_edges[i][1]))
    return list_edges_sans_poids
        
def creation_list_for_my_dict(list_nodes, list_edges_sans_poids):
    list_stockage = []
    tmp = []
    for i in range(len(list_nodes)):
        tmp = []
        for j in range(len(list_edges_sans_poids)):
            if list_nodes[i] == list_edges_sans_poids[j][0]:
                if list_edges_sans_poids[j][1] not in tmp:
                    tmp.append(list_edges_sans_poids[j][1])
            if list_nodes[i] == list_edges_sans_poids[j][1]:
                if list_edges_sans_poids[j][0] not in tmp:
                    tmp.append(list_edges_sans_poids[j][0])
        list_stockage.append((list_nodes[i],tmp))
    return list_stockage


###############################################################
#                        FINAL FUNCTIONS                      #
###############################################################

def find_eulerian_path(graph):
    if nx.is_eulerian(graph) == True:
        eulerian_circuit = list(nx.eulerian_circuit(graph))
    return eulerian_circuit

def final_list(is_oriented):
    graph = set_graph(is_oriented)
    edges, n, list_nodes = set_undirected(graph)
    odd_nodes = filling_odd_list(list_odd_node,graph)
    possible_pair = generate_pair_possible(odd_nodes)
    best_pair_list = choice_best_new_pair(possible_pair,odd_nodes,graph)
    dist = set_up_dist(best_pair_list,graph)

    print(edges)
    graph.add_edges_from(dist)
    circuit = find_eulerian_path(graph)
    print()
    print("Circuit eulerien:", circuit)
    print()

 
###############################################################
#                             MAIN                            #
###############################################################

final_list(False)



    