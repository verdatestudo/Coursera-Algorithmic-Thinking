
'''
Algorithmic Thinking Week 2 - Network Attack
2016-Feb-13
Python 2.7
Chris
'''

'''
Overview
Graph exploration (that is, "visiting" the nodes and edges of a graph) is a powerful and necessary tool to
elucidate properties of graphs and quantify statistics on them. For example, by exploring a graph,
we can compute its degree distribution, pairwise distances among nodes, its connected components,
and centrality measures of its nodes and edges. As we saw in the Homework and Project,
breadth-first search can be used to compute the connected components of a graph.

In this Application, we will analyze the connectivity of a computer network as it undergoes a cyber-attack.
In particular, we will simulate an attack on this network in which an increasing number of servers are disabled.
In computational terms, we will model the network by an undirected graph and repeatedly delete nodes from this graph.
We will then measure the resilience of the graph in terms of the size of the largest remaining
connected component as a function of the number of nodes deleted.

In this Application, you will compute the resilience of several types of undirected graphs.
We suggest that you begin by collecting and writing code to create the following three types of graphs:

An example computer network - The text representation for the example network is here.
You may use this provided code to load the file as an undirected graph (with 1239 nodes and 3047 edges).
Note that this provided code also includes several useful helper functions that you should review.

ER graphs - If you have not already implemented the pseudo-code for creating undirected ER graphs, you will need to implement this code.
You may wish to modify your implementation of make_complete_graph from Project 1 to add edges randomly
(again, keep in mind that in Project 1 the graphs were directed, and here we are dealing with undirected graphs).

UPA graphs - In Application 1, you implemented pseudo-code that created DPA graphs.
These graphs were directed (The D in DPA stands for directed).
In this Application, you will modify this code to generate undirected UPA graphs.
The UPA version should add an undirected edge to the UPA graph whenever you added a directed edge in the DPA algorithm.
Note that since the degree of the newly added node is no longer zero, its chances of being selected in subsequent trials increases.
In particular, you should either modify the DPATrial class to account for this change or use our provided UPATrial class.
'''

import pickle
import random
import math
import time
import matplotlib.pyplot as plt

import project2_bfs as project2
import degree_graphs_app2 as deggraph
import alg_application2_provided as app2_prov
import upa_trial as upa

def convert_txt_to_dict(filename):
    '''
    Code to convert the text file containing network data into a dictionary
    '''

    print 'Converting network file to dictionary ...'

    computer_network_dict = {}
    with open(filename) as word_file:
        for line in word_file:
            line = [line.strip() for line in line.split()]
            line = [int(x) for x in line]
            if len(line) == 0:
                computer_network_dict[line[0]] = [line[1:]]
            else:
                computer_network_dict[line[0]] = line[1:]

    print 'Network with %d nodes' %(len(computer_network_dict))
    print 'Network with %d edges' %(sum(len(val) for val in computer_network_dict.itervalues()) / 2)
    print 'Conversion complete'
    return computer_network_dict

def random_order(ugraph):
    '''
    Next, you should write a function random_order that takes a graph and returns
    a list of the nodes in the graph in some random order.
    '''

    nodes_list = [key for key in ugraph.keys()]
    random.shuffle(nodes_list)
    return nodes_list

def create_UPA_graph(n, m):
    '''
    Create UPA graph using n nodes and m starting nodes
    '''

    graph = make_complete_graph(m)
    upa_trial = upa.UPATrial(m)
    for node in range(m, n):
        graph[node] = set([])
    for node in range(m, n):
        for x_node in upa_trial.run_trial(m):
            graph[node].add(x_node)
            graph[x_node].add(node)
    return graph

def make_complete_graph(num_nodes):
    """returns a complete graph"""

    graph = {}
    edges = set(range(num_nodes))
    for node in range(num_nodes):
        graph[node] = edges.difference(set([node]))
    return graph

def question_one():
    '''
    Question 1 (5 pts)
    To begin our analysis, we will examine the resilience of the computer network under an attack in which servers are chosen at random.
    We will then compare the resilience of the network to the resilience of ER and UPA graphs of similar size.

    To begin, you should determine the probability p such that the ER graph computed using this edge probability has approximately the same number of edges as the computer network.
    (Your choice for p should be consistent with considering each edge in the undirected graph exactly once, not twice.)
    Likewise, you should compute an integer m such that the number of edges in the UPA graph is close to the number of edges in the computer network.
    Remember that all three graphs being analyzed in this Application should have the same number of nodes and approximately the same number of edges.

    Next, you should write a function random_order that takes a graph and returns a list of the nodes in the graph in some random order.
    Then, for each of the three graphs (computer network, ER, UPA), compute a random attack order using random_order and use this attack order
    in compute_resilience to compute the resilience of the graph.

    Once you have computed the resilience for all three graphs, plot the results as three curves combined in a single standard plot (not log/log).
    Use a line plot for each curve. The horizontal axis for your single plot be the the number of nodes removed (ranging from zero to the number of nodes in the graph)
    while the vertical axis should be the size of the largest connect component in the graphs resulting from the node removal.
    For this question (and others) involving multiple curves in a single plot, please include a legend in your plot that distinguishes the three curves.
    The text labels in this legend should include the values for p and m that you used in computing the ER and UPA graphs, respectively.
    Both matplotlib and simpleplot support these capabilities (matplotlib example and simpleplot example).

    Note that three graphs in this problem are large enough that using CodeSkulptor to calculate compute_resilience for these graphs will take on the order of 3-5 minutes per graph.
    When using CodeSkulptor, we suggest that you compute resilience for each graph separately and save the results (or use desktop Python for this part of the computation).
    You can then plot the result of all three calculations using simpleplot.

    Once you are satisfied with your plot, upload your plot in the box below using "Attach a file" button (the button is disabled under the 'html' edit mode;
    you must be under the 'Rich' edit mode for the button to be enabled). Your plot will be assessed based on the answers to the following three questions:

    Does the plot follow the formatting guidelines for plots?
    Does the plot include a legend? Does this legend indicate the values for p and m used in ER and UPA, respectively?
    Do the three curves in the plot have the correct shapes?
    '''
    # for ER and UPA graph need ~1239 nodes and ~3047 edges to match example network

    # for ER graph (n-1)p = average edge of node
    # so 1238p = 2.46 (3047/1239) ... and p = ~0.00199
    # this looks like it generates 3047 edges, but as it's undirected there are only really half that number.
    # so double and we get p = 0.00397

    # for UPA graph, simply choose M value which is close to average edge of node - either 2 or 3.

    # generate our two random networks and
    # print some statements to check our random networks are close to the example network
    computer_network_nodes_length = len(computer_network_dict)
    computer_network_edges = sum(len(val) for val in computer_network_dict.itervalues()) / 2

    er_prob = (computer_network_edges / float(computer_network_nodes_length)) / (float(computer_network_nodes_length) - 1) * 2

    print '\n', 'Example network total nodes: ', len(computer_network_dict)
    print 'Computer network undirected edges: ', sum(len(val) for val in computer_network_dict.itervalues()) / 2, '\n'
    print 'Probability for er_graph',  er_prob, '\n'

    er_graph = deggraph.make_ugraph_prob(len(computer_network_dict), er_prob)

    print 'ER network total nodes: ', len(er_graph)
    print 'ER network undirected edges: ', sum(len(val) for val in er_graph.itervalues()) / 2, '\n'

    m_value_upa = int(math.ceil(computer_network_edges / float(computer_network_nodes_length)))

    print 'M value for UPA graph (total nodes divided by edges): ', m_value_upa, '\n'

    upa_graph = create_UPA_graph(len(computer_network_dict), m_value_upa)

    print 'UPA network total nodes: ', len(upa_graph)
    print 'UPA network undirected edges: ', sum(len(val) for val in upa_graph.itervalues()) / 2, '\n'

    # now compute resilience of all three networks based on a random attack

    computer_network = project2.compute_resilience(computer_network_dict, random_order(computer_network_dict))
    er_network = project2.compute_resilience(er_graph, random_order(er_graph))
    upa_network = project2.compute_resilience(upa_graph, random_order(upa_graph))

    # now plot these results - see question1.png for results.

    plt.plot(computer_network, lw=2, label='Example computer network')
    plt.plot(er_network, lw=2, label='ER network - p = 0.00397')
    plt.plot(upa_network, lw=2, label='UPA network - m = 3')
    plt.legend(loc='upper right')
    plt.title('Different networks resilience versus a random attack')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Largest connected component size')

    plt.show()

    # return the two random networks to be used again in question 4
    return er_graph, upa_graph


def question_two():
    '''
    Question 2 (1 pt)
    Consider removing a significant fraction of the nodes in each graph using random_order.
    We will say that a graph is resilient under this type of attack if the size of its largest connected component
    is roughly (within ~25%) equal to the number of nodes remaining, after the removal of each node during the attack.

    Examine the shape of the three curves from your plot in Question 1.
    Which of the three graphs are resilient under random attacks as the first 20 percent of their nodes are removed?
    Note that there is no need to compare the three curves against each other in your answer to this question.
    '''

    '''
    Answer:

    Removing the first 20 percent of nodes is roughly 250 nodes on the x-axis of the previous graph.
    This leaves a network with ~990 nodes, and the largest connected component (y-axis) must be at least 25 percent of this (~740).
    Looking at the graph all three networks appear to be above this level - the EP and UPA network decreases in a linear fashion,
    and although the example network declines at a faster rate, it is still comfortably above the target number required to be considered resilient
    '''
    pass

def question_three():
    '''
    Question 3 (3 pts)
    In the next three problems, we will consider attack orders in which the nodes being removed are chosen based on the structure of the graph.
    A simple rule for these targeted attacks is to always remove a node of maximum (highest) degree from the graph.
    The function targeted_order(ugraph) in the provided code takes an undirected graph ugraph and iteratively does the following:

    Computes a node of the maximum degree in ugraph.
    If multiple nodes have the maximum degree, it chooses any of them (arbitrarily).
    Removes that node (and its incident edges) from ugraph.

    Observe that targeted_order continuously updates ugraph and always computes a node of maximum degree with respect to this updated graph.
    The output of targeted_order is a sequence of nodes that can be used as input to compute_resilience.

    As you examine the code for targeted_order, you feel that the provided implementation of targeted_order is not as efficient as possible.
    In particular, much work is being repeated during the location of nodes with the maximum degree.
    In this question, we will consider an alternative method (which we will refer to as fast_targeted_order) for computing the same targeted attack order.
    Here is a pseudo-code description of the method:

    In Python, this method creates a list degree_sets whose kth element is the set of nodes of degree k.
    The method then iterates through the list degree_sets in order of decreasing degree. When it encounter a non-empty set, the nodes in this set must be of maximum degree.
    The method then repeatedly chooses a node from this set, deletes that node from the graph, and updates degree_sets appropriately.

    For this question, your task is to implement fast_targeted_order and then analyze the running time of these two methods on UPA graphs of size n with m=5.
    Your analysis should be both mathematical and empirical and include the following:

    Determine big-O bounds of the worst-case running times of targeted_order and fast_targeted_order as a function of the number of nodes n in the UPA graph.
    Compute a plot comparing the running times of these methods on UPA graphs of increasing size.

    Since the number of edges in these UPA graphs is always less than 5n (due to the choice of m=5), your big-O bounds for both functions should be expressions in n.
    You should also assume that the all of the set operations used in fast_targeted_order are O(1).

    Next, run these two functions on a sequence of UPA graphs with n in range(10, 1000, 10) and m=5 and use the time module (or your favorite Python timing utility)
    to compute the running times of these functions.
    Then, plot these running times (vertical axis) as a function of the number of nodes n (horizontal axis) using a standard plot (not log/log).
    Your plot should consist of two curves showing the results of your timings.
    Remember to format your plot appropriately and include a legend.
    The title of your plot should indicate the implementation of Python (desktop Python vs. CodeSkulptor) used to generate the timing results.

    Your answer to this question will be assessed according to the following three items:

    What are tight upper bounds on the worst-case running times of targeted_order and fast_targeted_order? Use big-O notation to express your answers (which should be very simple).
    Does the plot follow the formatting guidelines for plots? Does the plot include a legend? Does the title include the implementation of Python used to compute the timings?
    Are the shapes of the timing curves in the plot correct?
    '''

    # see FastTargetedOrderFig.png for pseudo-code
    # see alg_application2_provided for provided targeted_order code
    # and my implementation of fast_targeted_order

    # see question3.png for graph results

    '''
    Answer to upper bounds on the worst-case running times:
    Fast_targeted_order : O(n)
    Targeted_order: O(n^2)
    '''

    m = 5 # given by question

    # produce timing for Fast_targeted_order
    x_values = []
    y_values = []

    for n in xrange(10, 1000, 10):
        graph = create_UPA_graph(n, m)
        start_time = time.clock()
        app2_prov.fast_targeted_order(graph)
        finish_time = time.clock()
        run_time = (finish_time - start_time) * 1000 # convert to ms
        x_values.append(n)
        y_values.append(run_time)

    plt.plot(x_values, y_values, lw=2, label='fast_targeted_order (UPA)')

    # produce timing for targeted_order
    x_values = []
    y_values = []

    for n in xrange(10, 1000, 10):
        graph = create_UPA_graph(n, m)
        start_time = time.clock()
        app2_prov.targeted_order(graph)
        finish_time = time.clock()
        run_time = (finish_time - start_time) * 1000 # convert to ms
        x_values.append(n)
        y_values.append(run_time)

    plt.plot(x_values, y_values, lw=2, label='targeted_order (UPA)')

    plt.legend(loc='upper left')
    plt.title('Execution time (ms) for different UPA graph sizes (m = 5) (Desktop Python implementation)')
    plt.xlabel('Number of nodes')
    plt.ylabel('Running time (ms)')

    plt.show()

    pass

def question_four():
    '''
    Question 4 (5 pts)
    To continue our analysis of the computer network, we will examine its resilience under an attack in which servers are chosen based on their connectivity.
    We will again compare the resilience of the network to the resilience of ER and UPA graphs of similar size.

    Using targeted_order (or fast_targeted_order), your task is to compute a targeted attack order for each of the three graphs (computer network, ER, UPA) from Question 1.
    Then, for each of these three graphs, compute the resilience of the graph using compute_resilience.
    Finally, plot the computed resiliences as three curves (line plots) in a single standard plot.
    As in Question 1, please include a legend in your plot that distinguishes the three plots.
    The text labels in this legend should include the values for p and m that you used in computing the ER and UPA graphs, respectively.

    Your plot will be assessed based on the answers to the following three questions:

    Does the plot follow the formatting guidelines for plots?
    Does the plot include a legend? Does this legend indicate the values for p and m used in ER and UPA, respectively?
    Do the three curves in the plot have the correct shape?
    '''

    ###
    computer_network_nodes_length = len(computer_network_dict)
    computer_network_edges = sum(len(val) for val in computer_network_dict.itervalues()) / 2

    er_prob = (computer_network_edges / float(computer_network_nodes_length)) / (float(computer_network_nodes_length) - 1) * 2

    print '\n', 'Example network total nodes: ', len(computer_network_dict)
    print 'Computer network undirected edges: ', sum(len(val) for val in computer_network_dict.itervalues()) / 2, '\n'
    print 'Probability for er_graph',  er_prob, '\n'

    er_graph = deggraph.make_ugraph_prob(len(computer_network_dict), er_prob)

    print 'ER network total nodes: ', len(er_graph)
    print 'ER network undirected edges: ', sum(len(val) for val in er_graph.itervalues()) / 2, '\n'

    m_value_upa = int(math.ceil(computer_network_edges / float(computer_network_nodes_length)))

    print 'M value for UPA graph (total nodes divided by edges): ', m_value_upa, '\n'

    upa_graph = create_UPA_graph(len(computer_network_dict), m_value_upa)

    print 'UPA network total nodes: ', len(upa_graph)
    print 'UPA network undirected edges: ', sum(len(val) for val in upa_graph.itervalues()) / 2, '\n'
    ###

    computer_network_target = app2_prov.fast_targeted_order(computer_network_dict)
    er_target = app2_prov.fast_targeted_order(er_graph)
    upa_target = app2_prov.fast_targeted_order(upa_graph)

    computer_network = project2.compute_resilience(computer_network_dict, computer_network_target)
    er_network = project2.compute_resilience(er_graph, er_target)
    upa_network = project2.compute_resilience(upa_graph, upa_target)

    # see question4.png for graph results

    plt.plot(computer_network, lw=2, label='Example computer network')
    plt.plot(er_network, lw=2, label='ER network - p = 0.00397')
    plt.plot(upa_network, lw=2, label='UPA network - m = 3')
    plt.legend(loc='upper right')
    plt.title('Different networks resilience versus targeted attack')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Largest connected component size')

    plt.show()

    pass

def question_five():
    '''
    Question 5 (1 pt)
    Now, consider removing a significant fraction of the nodes in each graph using targeted_order.
    Examine the shape of the three curves from your plot in Question 4.
    Which of the three graphs are resilient under targeted attacks as the first 20 percent of their nodes are removed?
    Again, note that there is no need to compare the three curves against each other in your answer to this question.
    '''

    '''
    Answer:
    As in question 2, we are looking at the y-axis value at x = ~250, and to be considered resilient this y value should be ~740 or larger.

    Clearly the example network does not meet this criteria - based on the curve it suffers an immediate and rapid decline,
    and after the first 20 percent of nodes are removed the network is almost totally disconnected.
    The ER network is still resilient - up to this point of the graph it appears to be a linear decline,
    removing the first 20 percent of nodes does little damage to the connectivity of the network.
    Later (at around 350 removed nodes) the slope of the graph significantly steepens and connectivity begins to fail.
    The UPA network is just about resilient on this graph, the largest component size seems to be between 750 and 800 after the first 20 percent of nodes are removed.
    However it is already in decline and suffers an even sharper decline shorter after, in this graph after 300 nodes (25%) are removed,
    the network has lost the majority of it's connectivity.
    '''
    pass

def question_six():
    '''
    Question 6 (1 pt extra credit)
    An increasing number of people with malevolent intent are interested in disrupting computer networks.
    If you found one of the two random graphs to be more resilient under targeted attacks than the computer network,
    do you think network designers should always ensure that networks' topologies follow that random model?
    Think about the considerations that one might have to take into account when designing networks and provide a short explanation for your answer.
    '''

    '''
    Answer:
    The ER network is clearly more resilient than the UPA network.
    That would suggest that the more balanced the number of connections between different nodes, the less vulnerable the network is to a targeted attack.
    So to improve network resilience designers could pay attention to this, perhaps by reducing connections on the most-used nodes and increasing connections onto lesser-used nodes.

    However, in reality an ER network may not be practical for many reasons.
    For example a client-server model will be more vulnerable than an ER model to a targeted attack, but it provides many advantages in practice.
    It is less expensive - you can purchase a few relatively expensive, high-performance servers and many cheaper clients,
    as opposed to an ER model which would require all nodes to be of similar performance.
    Other security concerns are also an issue - with a few highly-important servers, you can protect them via passwords and physical security such as keypad locked doors.
    If every node was equally valuable, securing the system in this way would be very difficult.

    So in conclusion, although this data is useful and can help influence network designers decision-making,
    it would not be practical to always follow a random model such as the ER network example.
    '''
    pass

# use alg_application2_provided.py to download computer network data
# use pickle to save and then load here
#with open('comp_network_pickledump', 'rb') as f:
#    computer_network_dict = pickle.load(f) # this is our example network
#

# or use this, my converter
#computer_network_dict = convert_txt_to_dict('alg_rf7.txt')

#question_one()
#question_four()
