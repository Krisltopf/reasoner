from itertools import product
from collections import deque

class RefinementSearch:

    def a_closure_v1(self, csp):
        is_refined = False
        print(csp.graph.nodes)
        while not is_refined:
            is_refined = True
            for i in range(csp.n_nodes-1):
                for j in range(csp.n_nodes-1):
                    for k in range(csp.n_nodes-1):
                        new_constraint = csp.calculus.cut(csp.constraints[i][j], 
                                                           csp.calculus.composition(csp.constraints[i][k], csp.constraints[k][j]))
                        if new_constraint != csp.constraints[i][j]:
                            csp.set_constraint(i, j, new_constraint)
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

                new_constraint_ik = csp.calculus.cut(csp.constraints[i][k], 
                                                           csp.calculus.composition(csp.constraints[i][j], csp.constraints[j][k]))
                if new_constraint_ik != csp.constraint[i][k]:
                            csp.set_constraint(i, k, new_constraint_ik)
                            queue.append((i,k))
                
                new_constraint_kj = csp.calculus.cut(csp.constraints[k][j], 
                                                           csp.calculus.composition(csp.constraints[k][i], csp.constraints[i][j]))
                if new_constraint_kj != csp.constraint[k][j]:
                            csp.set_constraint(k, j, new_constraint_kj)
                            queue.append((k,j))
        return csp

    def refinementV1():
        pass

#my_reasoner = Reasoner.