from calculus import Calculus
from csp import CSP
from aclosure import RefinementSearch
import sys

def parse_csps(file_name, calculus):
    csp_list = []
    file = open(file_name, "r")
    content = file.read()
    graphs = content.split('.')
    graphs = list(filter(lambda x: x!='',graphs))

    for graph in graphs:
        edges = graph.split('\n')
        edges = list(filter(lambda x: x!='',edges))
        n_nodes = int(edges[0].split(' ')[0])
        consistent = edges[0].split(' ')[4] != 'NOT'
        csp = CSP(n_nodes,consistent, calculus)

        for edge in edges[1:]:
            edge = edge[:-1].split('(')
            out_node = int(edge[0].split(' ')[0])
            in_node = int(edge[0].split(' ')[1])
            label = edge[1]
            constraint_list = edge[1].split(' ')
            csp.add_edge(out_node,in_node,label,constraint_list)
                
        csp_list.append(csp)
    return csp_list

my_reasoner = Calculus()
my_reasoner.parse_file("allen.txt", compositions_generated=True)
csp_list = parse_csps("cspTest.txt", my_reasoner)
refinement_search = RefinementSearch()

print(csp_list[0].constraints)
print(refinement_search.refinementV1(csp_list[1]))
print(csp_list[0].constraints)
