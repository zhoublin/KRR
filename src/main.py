# -*- Coding: utf-8 -*-
# @Time    : 2022.9.27
# @Author  : zhoubolin
# @File    : main.py

import os
from knowledgedb import RDF
from algorithm import FOILearner

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import matplotlib.pyplot as plt
import networkx as nx
import argparse

# 初始化数据库
def Initialize(problem):
    if problem == 'familyProblem':
        RDF.buildKDB_Family()
    elif problem == 'zebraProblem':
        RDF.buildKDB()
    elif problem == 'clanProblem':
        RDF.buildKDB_clan()

# 简单的知识图谱可视化
def visualization():
    obj = RDF()
    plt.figure(figsize=(40,40))
    G = rdflib_to_networkx_multidigraph(obj.graph)
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    plt.savefig('knowledgeGraph.jpg')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Knowledge Graph Q&A System')
    parser.add_argument('--kngraph', dest='graphname', type=str, help='Knowledge Graph Question')
    parser.add_argument('--debug', dest='debug', type=bool)
    args = parser.parse_args()

    assert args.graphname in ['familyProblem', 'zebraProblem', 'clanProblem']
    Initialize(args.graphname)
    visualization()

    learner = FOILearner()
    if args.debug:
        learner(['?who', 'grandfather', 'sean'])
    else:
        print("\033[0;31mEnter a query consisting of a predicate and variables, with the \
            \nvariable beginning with '?' and ensure that all letters are lowercase. \
            \n(Type 'exit' to stop) \
            \nFor example: >>> jane daughter_of ?who\033[0m")
        query = input('>>> ')
        while query != 'exit':
            terms = query.split(' ')
            print(terms)
            # learner(['jane', 'daughter_of', '?a'])
            learner([terms[0], terms[1], terms[2]])
            query = input('>>> ')