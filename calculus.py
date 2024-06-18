import numpy as np
import math
import re
import cProfile, io, pstats
from pstats import SortKey


class Calculus:
    def __init__(self):
        self.algebra_symbols = [0, 1]
        
        # init relations
        self.base_relations = ['<','=','>'] #1,2,4 
        self.num_relations = pow(2, len(self.base_relations))-1
        
        # init converse table
        self.converses = np.array([4,2,1])
        self.fill_converse_table(self.converses)
        
        # init composition table
        self.compositions = np.array([[1,1,7],[1,2,4],[7,4,4]])
        #self.fill_composition_table(self.compositions)

        self.csps = []

    def fill_converse_table(self, converses):
        self.converse_lookup = np.zeros(self.num_relations, dtype=int)
        
        for i in range(len(converses)):
            self.converse_lookup[2**i] = converses[i]
            
        for relation in range(self.num_relations):
            converse = 0
            indeces = relation
            for i in range(len(self.base_relations)):
                if indeces % 2 == 1:
                    converse = converse | self.converse_lookup[2**i]
                indeces = indeces // 2
                    
            self.converse_lookup[relation] = converse
            
    def fill_composition_table(self, compositions):

        self.composition_lookup = np.zeros((self.num_relations, self.num_relations), dtype=int)
        
        for i in range(len(compositions)):
            for j in range(len(compositions)):
                self.composition_lookup[2**i][2**j] = compositions[i][j]
        
        for relation1 in range(self.num_relations):
            if relation1 % 100 == 0:
                print("Check Relation Number: ", relation1, "/", self.num_relations)
            for relation2 in range(self.num_relations):
                composition = 0
                r1 = relation1
                for i in range(len(self.base_relations)):
                    if r1 % 2 == 1:
                        r2 = relation2
                        for j in range(len(self.base_relations)):
                            if r2 % 2 == 1:
                                composition = composition | self.composition_lookup[2**i][2**j]
                            r2 = r2 // 2
                    r1 = r1 // 2
                
                self.composition_lookup[relation1][relation2] = composition

        np.save("compositions.npy", self.composition_lookup)
    
    # nicht fertig!!!
    def parse_expression(self, input):
        expression = ''.join(input.split())
        
        algebra_symbols_re = '|'.join(self.algebra_symbols)
        base_relations_re = '|'.join(self.base_relations)
        arguments = re.split(algebra_symbols_re, expression)
        seperator = (re.search(algebra_symbols_re, expression)).group()
        
        for i, argument in enumerate(arguments):
            clean_argument = re.sub('[^' + base_relations_re + ']*', '', argument)
            arguments[i] = self.translate(list(clean_argument))
           
        print(arguments)   
        
        result = []
        
        if seperator == self.algebra_symbols[0]:
            result = self.complement(arguments[0])
            
        elif seperator == self.algebra_symbols[1]:
            result = self.complement(arguments[0])
            
        return result
    
    def parse_file(self, file_name, compositions_generated = False):
        file = open(file_name, "r")
        content = file.read()
        sections = content.split("\n\n")

        # set base relations
        relations = sections[0].split("\n")
        relations = relations[1]
        self.base_relations = relations.split(" ")
        self.num_relations = pow(2, len(self.base_relations))-1

        # set table of converses
        converses = sections[1].split("\n")
        converses = converses[1:]
        self.converses = np.zeros(len(self.base_relations), dtype=int)
        for i, converse in enumerate(converses):
            result = list(filter(None, converse.split(" ")))
            self.converses[i] = self.translate(result[1:])
        self.fill_converse_table(self.converses)

        # set table of compositions
        if compositions_generated:
            self.composition_lookup = np.load("./compositions.npy")
            return
            
        compositions = sections[2].split("\n")
        compositions = compositions[1:]
        self.compositions = np.zeros((len(self.base_relations), len(self.base_relations)), dtype=int)
        for i, composition in enumerate(compositions):
            x = i // len(self.base_relations)
            y = i % len(self.base_relations)
            result = composition.replace("(", "")
            result = result.replace(")", "")
            result = list(filter(None, result.split(" ")))
            result = result[2:]
            self.compositions[x][y] = self.translate(result)

        self.fill_composition_table(self.compositions)


    def parse_csps(self, file_name):
        file = open(file_name, "r")
        content = file.read()
        graphs = content.split('.')
        graphs = list(filter(lambda x: x!='',graphs))

        for graph in graphs:
            edges = graph.split('\n')
            edges = list(filter(lambda x: x!='',edges))
            n_nodes = int(edges[0].split(' ')[0])
            consistent = edges[0].split(' ')[4] != 'NOT'
            csp = CSP(n_nodes,consistent)

            for edge in edges[1:]:
                edge = edge[:-1].split('(')
                out_node = int(edge[0].split(' ')[0])
                in_node = int(edge[0].split(' ')[1])
                label = edge[1]
                constraint = self.translate(edge[1].split(' '))
                #constraint = edge[1].split(' ')
                csp.add_edge(out_node,in_node,label,constraint)
                
            self.csps.append(csp)
        
    # translates a list of base relation strings into the internal number representation
    def translate(self, symbols):
        if isinstance(symbols, str):
            symbols = [symbols]
        relations = 0
        for symbol in symbols:
            relations = relations | pow(2, self.base_relations.index(symbol))
        return relations
    
    def translate_inv(self, symbol_bin):
        indeces = symbol_bin & self.num_relations
        relations = []
        for i in range(len(self.base_relations)):
            if indeces % 2 == 1:
                relations.append(self.base_relations[i])
            indeces = indeces // 2
        return relations

    def complement(self, relation):
        return ~relation & (self.num_relations)

    def cut(self, relation1, relation2):
        return relation1 & relation2
    
    def union(self, relation1, relation2):
        return relation1 | relation2
    
    def converse(self, relation):
        return self.converse_lookup[relation]
    
    def composition(self, relation1, relation2):
        return self.composition_lookup[relation1][relation2]