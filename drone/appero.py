# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:21:16 2020

@author: julien
"""
import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

###############################################################
#                       GLOBAL VARIABLE                       #
###############################################################


pair_return = []
balanced_node = []

    
#edge_list = [(3735398272, 7403380099, 14.988), (3735398272, 5272829472, 5.636), (5272829472, 2625939755, 67.029), (5272829472, 2625939755, 101.267), (7403380099, 1511544620, 58.423), (7403380099, 7403380101, 33.039), (7403380100, 7403380101, 47.11), (7403380100, 7403380101, 142.62199999999999), (7403380100, 1511544620, 61.469)]
edge_list = [(0,1,1), (0,2,1), (1,2,1), (2,3,1)]

###############################################################
#                       SUPPORT FUNCTIONS                     #
###############################################################

'''renvoie une liste des noeuds qui sont de degrees impairs'''
def odd_vertices(n, edge_list):
    count = 0
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
                count += 1
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
                count += 1
    list_odd_nodes = res + res2
    list_odd_nodesx = list(set(list_odd_nodes))
    return list_odd_nodesx, count

'''recupere tous les noeuds du graph dans une list'''
def get_node_list(edge_list):
    list_node = []
    visited = []
    for i in range(len(edge_list)):
        if edge_list[i][0] not in visited:
            list_node.append(edge_list[i][0])
        if edge_list[i][1] not in visited:
            list_node.append(edge_list[i][1])
    return list(set(list_node))

'''recuepre le poids d'une arrete'''            
def get_weight(a,b,edge_list):
    for edge in edge_list:
        if edge[0] == a and edge[1] == b:
            return edge[2]
        if edge[1] == a and edge[0] == b:
            return edge[2]
    return 0
   
'''recupere les voisins d'un sommet'''     
def get_neighbours(edge_list, u):
    list_neighbours = []
    for i in range(len(edge_list)):
        if u == edge_list[i][0]:
            list_neighbours.append(edge_list[i][1])
        if u == edge_list[i][1]:
            list_neighbours.append(edge_list[i][0])
    return list(set(list_neighbours))

'''reupere l'adj list'''
def get_adj_list(edge_list, list_node):
    adj_list = []
    
    for node in list_node:
        neighbours = get_neighbours(edge_list, node)
        adj_list.append(neighbours)
    return adj_list

'''regarde si le graph est eulerien'''
def is_eulerian(num_vertices, edge_list):
    _, count = odd_vertices(num_vertices, edge_list)
    if count == 2 or count == 0:
        return True
    return False

'''simple dfs'''
def dfs(vertice, visited, list_node, edge_list):
    visited[list_node.index(vertice)] = True
    
    neighbours = get_neighbours(edge_list, vertice)
    
    for i in neighbours:
        if visited[list_node.index(i)] == False:
            dfs(i, visited, list_node, edge_list)
    return visited

'''dfs qui compte le nombre de sommet accessible à partir
   d'un autre sommet
'''
def dfs_count(vertice, visited, list_node, edge_list):
    visited[list_node.index(vertice)] = True
    count = 1
    neighbours = get_neighbours(edge_list, vertice)
    
    for i in neighbours:
        if visited[list_node.index(i)] == False:
            count = count + dfs_count(i, visited, list_node, edge_list)
    return count
    
'''trasforme une arrete: (i,j) -> (j,i)'''
def reverse_edge(edge_list):
    reverse_edge_list = []
    for edge in edge_list:
        reverse_edge_list.append((edge[1],edge[0],edge[2]))
    return reverse_edge_list

''' supprime une arrete de la edge_list
'''
def remove_edge(a, b, edge_list):
    for edge in edge_list:
        if edge[0] == a and edge[1] == b:
            edge_list.remove(edge)
        if edge[1] == a and edge[0] == b:
            edge_list.remove(edge)
    return edge_list

###############################################################
#                            DIJKSTRA                         #
###############################################################

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
    _, prev = dijkstra(src, list_node, edge_list)
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

def create_new_edge_list(list_odd_nodes, node):
    possible_pair = generate_pair_possible(list_odd_nodes)
    best_pair = choice_best_new_pair(possible_pair, list_odd_nodes, node, edge_list)
    new_pair_with_theirs_dist = set_up_dist(best_pair, edge_list)
    new_edge_list = edge_list + new_pair_with_theirs_dist
    return new_edge_list

###############################################################
#                          HIERHOLZER                         #
###############################################################

def Hierholzer_algo(adj, edge_list, list_node):
    start = list_node[0]
    current_path = [start]
    circuit = []
    
    while current_path:
        current_v = current_path[-1]
        if adj[list_node.index(current_v)]:
            next_v = adj[list_node.index(current_v)].pop()
            current_path.append(next_v)
        else:
            circuit.append(current_path.pop())
    circuitx = circuit.copy()
    circuitx.reverse()
    return circuitx
            
def Hierholzer(edge_list, list_node):
    adj = get_adj_list(edge_list, list_node)
    return Hierholzer_algo(adj, edge_list, list_node)

###############################################################
#                           FLEURY                            #
###############################################################

def check_next_node(src, dest, edge_list, list_node):
    cpy_edge_list = edge_list.copy()
    
    neighbours = get_neighbours(edge_list, src)
    if len(neighbours) == 1:
        return True
    else:
        visited = [False] * len(list_node)
        count1 = dfs_count(src, visited, list_node, edge_list)
        remove_edge(src, dest, edge_list)
        visited = [False] * len(list_node)
        count2 = dfs_count(src, visited, list_node, edge_list)
        
        cpy_edge_list.append((src,dest,get_weight(src, dest, edge_list)))
        
        return False if count1 > count2 else True

def Fleury(src, edge_list, list_node):
    neighbours = get_neighbours(edge_list, src)
    
    for node in neighbours:
        if check_next_node(src, node, edge_list, list_node):
            print("%d-%d " %(src, node))
            remove_edge(src, node, edge_list)
            Fleury(node, edge_list, list_node)
    

###############################################################
#                     STRONGLY CONNECTED                      #
###############################################################

''' regarde les arcs sortants et entrants'''
def check_node_balanced(edge_list, list_node, next_node):
    count_entrant = 0
    count_sortant = 0

    for edge in edge_list:
        if edge[0] == list_node[next_node]:
            count_entrant += 1
        if edge[1] == list_node[next_node]:
            count_sortant += 1
            
    balanced_node.append((list_node[next_node], count_entrant, count_sortant))
        
    if next_node == len(list_node) - 1:
        return balanced_node
    return check_node_balanced(edge_list, list_node, next_node + 1)

''' regarde si le graph est fortement connexe
    Kosaraju's algorithm
'''
def is_strongly_connected(num_vertices, list_node, edge_list):
    visited = [False] * num_vertices
    dfs(list_node[0], visited, list_node, edge_list)
    
    for node in visited:
        if node == False:
            return False
        
    reverse = reverse_edge(edge_list)
    visited = [False] * num_vertices
    dfs(list_node[0], visited, list_node, reverse)
    
    for node in visited:
        if node == False:
            return False
    return True
        

###############################################################
#                             MAIN                            #
###############################################################
    
def solve_undirected(num_vertices, edge_list):
    list_odd_nodes, _ = odd_vertices(num_vertices,edge_list)
    node = get_node_list(edge_list)
    new_edge_list = create_new_edge_list(list_odd_nodes, node)
    Fleury(node[0], edge_list, node)
    
        
        
        
        
def solve_directed(num_vertices, edge_list):
    node = get_node_list(edge_list)
    a = check_node_balanced(edge_list, node, 0)
    print("Check entrant/sortant:\n", a)

def solve(is_oriented, num_vertices, edge_list):
    if is_oriented == False:
        solve_undirected(num_vertices, edge_list)
    else:
        solve_directed(num_vertices, edge_list)
    
solve(False,7,edge_list)
