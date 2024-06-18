from reasoner import Calculus, CSP
from itertools import product
from collections import deque
import numpy as np

class RefinementSearch:
    
    def __init__(self, calculus):
        self.set_calculus(calculus)

    def set_calculus(self, calculus):
        self.calculus = calculus
    
    def set_csp(self, csp):
        self.csp = csp

    def set_constraint(self, csp, out_node, in_node, constraint):
        csp.constraints[out_node][in_node] = constraint
        csp.constraints[in_node][out_node] = self.calculus.converse(constraint)

    def a_closure_v1(self, csp):
        is_refined = False
        print(csp.graph.nodes)
        while not is_refined:
            is_refined = True
            for i in range(csp.n_nodes):
                for j in range(csp.n_nodes):
                    for k in range(csp.n_nodes):
                        new_constraint = csp.calculus.cut(csp.constraints[i][j], 
                                                           csp.calculus.composisition(csp.constraints[i][k], csp.constraints[k][j]))
                        if new_constraint != csp.constraint[i][j]:
                            self.set_constraint(csp, i, j, new_constraint)
                            is_refined = False
        return csp
    
    def a_closure_v2(self, csp):
        edges = product(range(csp.n_nodes), repeat=1)
        queue = deque(edges)
        while len(queue) != 0:
            i, j = queue.pop()
            if(i == j):
                continue
            for k in range(csp.n_nodes):
                if k == i or k == j:
                    continue

                new_constraint_ik = self.calculus.cut(csp.constraints[i][k], 
                                                           self.calculus.composisition(csp.constraints[i][j], csp.constraints[j][k]))
                if new_constraint_ik != csp.constraint[i][k]:
                            self.set_constraint(csp, i, k, new_constraint_ik)
                            queue.append((i,k))
                
                new_constraint_kj = self.calculus.cut(csp.constraints[k][j], 
                                                           self.calculus.composisition(csp.constraints[k][i], csp.constraints[i][j]))
                if new_constraint_kj != csp.constraint[k][j]:
                            self.set_constraint(csp, k, j, new_constraint_kj)
                            queue.append((k,j))
        return csp

    def refinementV1():
        pass

#my_reasoner = Reasoner.