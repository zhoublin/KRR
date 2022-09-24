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


# if __name__ == "__main__":
#     config = omegaconf.OmegaConf.load("configs/config.yaml")
#     parser = NLParser(config)
#     database = RDF(config)
#     serv = FOILearner(config)
#     qaSystem = QueryAnswerService(database, serv, parser, config)
#     gui = QAGui(qaSystem)
#     gui.query()

if __name__ == "__main__":
    # res = RDF.test()
    RDF.buildKDB()
    obj = RDF()
    query = ["None", "live_in", "None"]
    print(list(obj._query(query)))
    insert = ["jane", "is_wife_of", "mike"]
    obj._update(insert)

    # obj._initialize()
    obj._delete(["jane", "is_wife_of", "mike"])
    query = ["jane", "None", "mike"]
    print(obj._query(query))