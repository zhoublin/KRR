# -*- Coding: utf-8 -*-
# @Time    : 2022.9.21
# @Author  : zhoublin
# @File    : parser.py

import os
import rdflib
import re
import spacy
import pandas as pd
import bs4
import requests
from spacy import displacy

class NLParser(object):
    def __init__(self, config) -> None:
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')

    def __call__(self, sent: str):
        doc = self.nlp(sent)