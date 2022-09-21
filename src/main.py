# -*- Coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 

import omegaconf

from knowledgedb import RDF
from algorithm import FOILearner
from QAservice import QueryAnswerService
from utils.parser import NLParser
from utils.gui import QAGui


if __name__ == "__main__":
    config = omegaconf.OmegaConf.load("configs/config.yaml")
    parser = NLParser(config)
    database = RDF(config)
    serv = FOILearner(config)
    qaSystem = QueryAnswerService(database, serv, parser, config)
    gui = QAGui(qaSystem)
    gui.query()