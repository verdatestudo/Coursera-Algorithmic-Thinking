
'''
Degree Distributions for Graphs
Algorithmic Thinking - Part 2 Application
(original code from Part 1)
2016-Feb-13
Python 2.7
Chris
'''

import random

def make_ugraph_prob(num_nodes, prob):
    '''
    Make an undirected graph with 'num_nodes' and probability 'prob' of edge occuring
    '''
    if num_nodes < 1:
        return None

    graph_dict = {}
    for node in range(num_nodes):
        graph_dict[node] = set([])
    for x_node in range(num_nodes):
        for a_node in range(num_nodes):
            if a_node > x_node: # and x_node not in graph_dict[a_node]:
                # because this is undirected, we only want to generate an edge once
                # for example if node 1 did not connect to node 4
                # then must not check whether node 4 should connect to node 1
                p = random.random()
                if p < prob:
                    # as undirected we add the edge to both nodes
                    graph_dict[x_node].add(a_node)
                    graph_dict[a_node].add(x_node)
    return graph_dict
