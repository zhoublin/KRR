# -*- Coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 

class QueryAnswerService(object):
    def __init__(self, db, serv, parser, config):
        self.database = db
        self.service = serv
        self.parser = parser
        self.config = config

    def query(self, q: str):
        pass
    
    def addKnowledge(self, sent: str):
        pass


