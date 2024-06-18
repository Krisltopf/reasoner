import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Documentation NetworkX:
# https://networkx.org/documentation/stable/reference/classes/digraph.html
class CSP:
    def __init__(self, n_nodes, consistent,calculus):
        self.n_nodes = n_nodes +1
        self.consistent = consistent
        self.calculus = calculus
        self.universal_relation = calculus.num_relations
        self.constraints = np.empty((n_nodes,n_nodes))
        self.constraints.fill(self.universal_relation)

        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(self.n_nodes-1))
        

    def plot_graph(self):
        nx.draw_circular(self.graph, with_labels = True)
        plt.show()

    def add_edge(self, out_node, in_node, label, constraint_list):
        self.graph.add_edge(out_node,in_node,label = label)

        internal_number = self.calculus.translate(constraint_list)
        self.constraints[out_node-1][in_node-1] = internal_number
        self.constraints[in_node-1][out_node-1] = self.calculus.converse(internal_number)