from itertools import product
from collections import deque
from copy import copy
import numpy as np
import sys

from csp import CSP
#pypi

class RefinementSearch:

    def a_closure_v1(self, csp: CSP):
        is_refined = False
        while not is_refined:
            is_refined = True
            for i in range(csp.n_nodes):
                for j in range(csp.n_nodes):
                    for k in range(csp.n_nodes):
                        new_constraint = csp.calculus.cut(csp.constraints[i][j], 
                                                           csp.calculus.composition(csp.constraints[i][k], csp.constraints[k][j]))
                        if new_constraint != csp.constraints[i][j]:
                            csp.set_constraint(i, j, new_constraint)
                            is_refined = False
                        if new_constraint == 0 or csp.constraints[i][j] == 0:
                            csp.constraints = np.zeros_like(csp.constraints)
                            return csp, False
        return csp, True
    
    def a_closure_v2(self, csp: CSP, queue = []):
        if len(queue) == 0:  
            edges = product(range(csp.n_nodes), range(csp.n_nodes))
            queue = deque(edges) #TODO tightness priority queue

        while len(queue) != 0:
            i, j = queue.pop()
            if(i == j):
                continue
            for k in range(csp.n_nodes):
                if k == i or k == j:
                    continue

                new_constraint_ik = csp.calculus.cut(csp.constraints[i][k], 
                                                           csp.calculus.composition(csp.constraints[i][j], csp.constraints[j][k]))
                if new_constraint_ik != csp.constraints[i][k]:
                            csp.set_constraint(i, k, new_constraint_ik)
                            queue.append((i,k))
                
                new_constraint_kj = csp.calculus.cut(csp.constraints[k][j], 
                                                           csp.calculus.composition(csp.constraints[k][i], csp.constraints[i][j]))
                if new_constraint_kj != csp.constraints[k][j]:
                            csp.set_constraint(k, j, new_constraint_kj)
                            queue.append((k,j))
                
                if new_constraint_ik == 0 or new_constraint_kj == 0 or csp.constraints[k][j] == 0 or csp.constraints[i][k] == 0:
                     csp.constraints = np.zeros_like(csp.constraints)
                     return csp, False
        return csp, True

    def refinementV1(self, csp: CSP, depth = 0):
        
        csp, consistent = self.a_closure_v1(csp) #änderungen undo!!!
        if not consistent:
             return False
        complex_relations = csp.find_complex_relations()
        if len(complex_relations) == 0:
             return True
        
        #print(depth, len(complex_relations))

        for i,j in complex_relations:
            base_relations = csp.calculus.get_base_relations(csp.constraints[i][j])
            for b in base_relations:
                    old_constraints = copy(csp.constraints)
                    csp.constraints[i][j] = b
                    refinement = self.refinementV1(csp, depth+1)
                    if refinement:
                        return True
                    csp.constraints = old_constraints
            if depth == 0 and j >= 4:
                 return False
        
        return False
    
    def refinementV1_5(self, csp: CSP):
         return self.refinementRecV1_5(csp)

    def refinementRecV1_5(self, csp: CSP, queue = []):
         csp, consistent = self.a_closure_v2(csp, queue)
         if 0 in csp.constraints:
             return False
         complex_relations = csp.find_complex_relations()
         if len(complex_relations) == 0:
             return True
         
         for i,j in complex_relations:
            old_constraint = csp.constraints[i][j]
            if i != j and np.log2(old_constraint) % 1 != 0:
                base_relations = csp.calculus.get_base_relations(old_constraint)
                for b in base_relations:
                        csp.constraints[i][j] = b
                        if self.refinementRecV1_5(csp, deque([(i,j)])):
                            return True
                csp.constraints[i][j] = old_constraint
        
         return False

    def refinementV2(self, csp: CSP):
        csp, consistent = self.a_closure_v2(csp) #änderungen undo!!!
        if not consistent:
            return False
        complex_relations = csp.find_complex_relations()

        # check for tractable subsets
        isTractable = True
        for i,j in complex_relations:
             if not csp.calculus.tractable_subset[csp.constraints[i][j]]:
                  isTractable = False
                  break  
        if isTractable:
             return True
             

        while not isTractable:
            i,j = self.getNextRelation()
            tractableRelations = self.split(csp.constraints[i][j])
            old_constraints = csp.constraints.copy()
            for relation in tractableRelations:
                 csp.set_constraint(i, j, relation)
                 csp, consistent = self.a_closure_v2(csp)
                 if not consistent:
                      csp.constraints = old_constraints

        return True
    
    def split(self, relation):
         pass
    
    def getNextRelation(self, complex_relations):
         return complex_relations.pop()