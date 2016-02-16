
'''
Degree Distributions for Graphs
Algorithmic Thinking - Part 1
2016-Jan-26
Python 2.7
Chris
'''

'''
Project 1 - Degree distributions for graphs

Overview
For your first project, you will write Python code that creates dictionaries corresponding to some simple examples of graphs.
You will also implement two short functions that compute information about the distribution of the in-degrees for nodes in these graphs.
You will then use these functions in the Application component of Module 1 where you will analyze the degree distribution of a citation graph for a collection of physics papers.

Representing directed graphs
To gain a more tangible feel for how directed graphs are represented as dictionaries in Python,
you will create three specific graphs (defined as constants) and implement a function that returns dictionaries corresponding to a simple type of directed graphs.
If you are unclear on how to represent a directed graph as a dictionary,
we suggest that you review the class notes on graph basics.
For this part of the project, you should implement the following:

# see directedgraphs.png

    EX_GRAPH0, EX_GRAPH1, EX_GRAPH2 - Define three constants whose values are dictionaries corresponding to the three directed graphs shown below.
The graphs are numbered 0, 1, and 2, respectively, from left to right.

    Note that the label for each node should be represented as an integer.
You should use these graphs in testing your functions that compute degree distributions.

    make_complete_graph(num_nodes) - Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete directed graph with the specified number of nodes.
A complete graph contains all possible edges subject to the restriction that self-loops are not allowed.
The nodes of the graph should be numbered 0 to num_nodes - 1 when num_nodes is positive.
Otherwise, the function returns a dictionary corresponding to the empty graph.

Computing degree distributions

For the second part of this project, you will implement two functions that compute the distribution of the in-degrees of the nodes of a directed graph.

    compute_in_degrees(digraph) - Takes a directed graph digraph (represented as a dictionary) and computes the in-degrees for the nodes in the graph.
The function should return a dictionary with the same set of keys (nodes) as digraph whose corresponding values are the number of edges whose head matches a particular node.

    in_degree_distribution(digraph) - Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph.
The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph.
The value associated with each particular in-degree is the number of nodes with that in-degree.
In-degrees with no corresponding nodes in the graph are not included in the dictionary.

    Note that the values in the unnormalized distribution returned by this function are integers, not fractions.
This unnormalized distribution is easier to compute and can later be normalized to sum to one by simply dividing each value by the total number of nodes.
'''

import algo_load_graph

import random
import numpy as np
from matplotlib import pyplot as plt

# Three constants to represent directed graphs as dictionary
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), \
            4: set([1]), 5: set([2]), 6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]), \
            4: set([1]), 5: set([2]), 6: set([]), \
            7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

def dpa_algo(n, m):
    if n < 1 or m < 1 or m > n:
        pass
    m_graph = make_complete_graph(m)
    print m_graph
    print compute_in_degrees(m_graph)
    total_indeg = 0
    # sum the indegrees only
    for value in m_graph.itervalues():
        for val in value:
            total_indeg += val
    print total_indeg

def make_graph_prob(num_nodes, prob):
    graph_dict = {}
    if num_nodes > 0:
        for x_num in range(num_nodes):
            graph_set = []
            for a_num in range(num_nodes):
                if a_num != x_num:
                    p = random.random()
                    if p < prob:
                        graph_set.append(a_num)
            graph_dict[x_num] = set(graph_set)
    return graph_dict


def make_complete_graph(num_nodes):

    '''
    Takes the number of nodes num_nodes and returns a dictionary
    corresponding to a complete directed graph with the specified number of nodes.

    A complete graph contains all possible edges subject to the restriction that self-loops are not allowed.

    The nodes of the graph should be numbered 0 to num_nodes - 1 when num_nodes is positive.
    Otherwise, the function returns a dictionary corresponding to the empty graph.
    '''
    graph_dict = {}
    if num_nodes > 0:
        for x_num in range(num_nodes):
            graph_dict[x_num] = set(range(0, x_num) + range(x_num+1, num_nodes))

    return graph_dict

def compute_in_degrees(digraph):

    '''
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph.
    The function should return a dictionary with the same set of keys (nodes) as digraph
    whose corresponding values are the number of edges whose head matches a particular node.
    '''
    # dict keys = dict keys input
    # for value in each dict key, add +1 to count for that node
    # return
    graph_dict = {}
    for key, value in digraph.iteritems():
        if key not in graph_dict:
            graph_dict[key] = 0
        for item in value:
            graph_dict[item] = graph_dict.get(item, 0) + 1

    return graph_dict

def in_degree_distribution(digraph):

    '''
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution of the in-degrees of the graph.

    The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph.

    The value associated with each particular in-degree is the number of nodes with that in-degree.
    In-degrees with no corresponding nodes in the graph are not included in the dictionary.

    Note that the values in the unnormalized distribution returned by this function are integers, not fractions.
    This unnormalized distribution is easier to compute and can later be normalized
    to sum to one by simply dividing each value by the total number of nodes.
    '''

    deg_dict = compute_in_degrees(digraph)
    graph_dict = {}

    for _, value in deg_dict.iteritems():
        graph_dict[value] = graph_dict.get(value, 0) + 1

    return graph_dict

    # key = number of indegrees (e.g 0,1,2,3,4)
    # value = number of times those indegrees appear

def testing():

    '''
    My testing function
    '''

    print 'Probability possible nodes'
    for dum_x in range(-1, 6):
        print dum_x, make_graph_prob(dum_x, 0.5)
    print '\n'
    #make_graph_prob(10000, 0.5) #check probability is working
    print 'Full possible nodes'
    for dum_x in range(-1, 6):
        print dum_x, make_complete_graph(dum_x)

    print '\n'
    print 'in degrees for node'
    print compute_in_degrees(EX_GRAPH0)
    print compute_in_degrees(EX_GRAPH1)
    print compute_in_degrees(EX_GRAPH2)

    print '\n'
    print 'unnormalised distribution of in-degrees of graph'
    print in_degree_distribution(EX_GRAPH0)
    print in_degree_distribution(EX_GRAPH1)
    print in_degree_distribution(EX_GRAPH2)

    print average_out_degrees(EX_GRAPH2)

def average_out_degrees(digraph):
    count = 0
    for node in digraph.values():
        count += len(node)
    count /= float(len(digraph))
    return count
