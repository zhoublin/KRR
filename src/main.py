# -*- Coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 

import os
from knowledgedb import RDF
from algorithm import FOILearner
from QAservice import QueryAnswerService
from utils.parser import NLParser
from utils.gui import QAGui

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import matplotlib.pyplot as plt
import networkx as nx

def Initialize(problem):
    if problem == 'familyProblem':
        RDF.buildKDB_Family()
    elif problem == 'zebraProblem':
        RDF.buildKDB()
    elif problem == 'clanProblem':
        RDF.buildKDB_clan()

def visualization():
    obj = RDF()
    plt.figure(figsize=(50,60))
    G = rdflib_to_networkx_multidigraph(obj.graph)
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    plt.savefig('knowledgeGraph.jpg')
    plt.show()

if __name__ == "__main__":
    Initialize('clanProblem')
    visualization()
    learner = FOILearner()
    learner(['jane', 'daughter_of', '?a'])