from reasoner import Calculus, CSP
from itertools import combinations
from collections import deque
import numpy as np

class RefinementSearch:
    
    def __init__(self, calculus):
        self.set_calculus(calculus)

    def set_calculus(self, calculus):
        self.calculus = calculus
    
    def set_csp(self, csp):
        self.csp = csp

    def a_closure_v1(self, csp):
        is_refined = False
        print(csp.graph.nodes)
        while not is_refined:
            is_refined = True
            for i in range(csp.n_nodes):
                for j in range(csp.n_nodes):
                    for k in range(csp.n_nodes):
                        new_constraint = self.calculus.cut(csp.constraints[i][j], 
                                                           self.calculus.composisition(csp.constraints[i][k], csp.constraints[k][j]))
                        if new_constraint != csp.constraint[i][j]:
                            csp.constraints[i][j] = new_constraint
                            is_refined = False
        return csp
    
    def a_closure_v2(self, csp):
        queue = deque(csp.constraints.flatten())
        while len(queue) != 0:
            

    def refinementV1():
        pass

#my_reasoner = Reasoner.