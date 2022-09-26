# -*- Coding: utf-8 -*-
# @ Time    : 
# @ Author  : 
# @ File    : 

import copy
from platform import machine
from statistics import variance
from knowledgedb import RDF
import numpy as np
import pandas as pd

NA = -float('inf')

class FOILearner(object):
    def __init__(self) -> None:
        self.database = RDF()
        self.domain = copy.deepcopy(self.database.domain)
        # self.domain["predicate"].remove("is")
    
    def _getClass(self, entity):
        for d in self.domain:
            if entity in self.domain[d]:
                return d
        return None

    def _getClassFromVaridx(self, string):
        classIdx = string[1:].split('_')[0]
        for _class in self.ClassIndex:
            if classIdx == self.ClassIndex[_class]:
                return _class
        return None

    def _getVarindx(self, classIndex, entityIndx):
        return "v{}_{}".format(classIndex, entityIndx)

    def _getAllvar(self, queryList):
        varList = []
        for query in queryList:
            if query[0][0] == '?':
                varList.append(query[0])
            if query[1][0] == '?':
                varList.append(query[1])
        return list(set(varList))

    def _replaceAllvar(self, repVar, repValue, queryList):
        curt = copy.deepcopy(queryList)
        for i in range(len(curt)):
            for j in range(len(curt[i])):
                if curt[i][j] == repVar:
                    curt[i][j] = repValue
        return curt

    def _cntWithValue(self, cset, place1=None, val1=None, place2=None, val2=None):
        cnt = 0
        for t in cset:
            if place1 is not None and place2 is not None:
                if t[place1] == val1 and t[place2] == val2:
                    cnt += 1
            elif place1 is not None:
                if t[place1] == val1:
                    cnt += 1
            elif place2 is not None:
                if t[place2] == val2:
                    cnt += 1
        return cnt
    
    def _delteWithValue(self, cset, place1=None, val1=None, place2=None, val2=None):
        curtSet = copy.deepcopy(cset)
        for t in cset:
            if place1 is not None and place2 is not None:
                if t[place1] != val1 and t[place2] != val2:
                    curtSet.remove(t)
            elif place1 is not None:
                if t[place1] != val1:
                    curtSet.remove(t)
            elif place2 is not None:
                if t[place2] != val2:
                    curtSet.remove(t)
        return curtSet

    def _deduce(self, PRED):
        '''
        pred: A tuple (a, p, b) to be deduced.
        a, p, b = '?var'/entity
        '''
        if PRED[1][0] == '?':
            return self.database(PRED)

        predicate = PRED[1]
        EveryclassDim = {}
        ClassIndex = set()
        ClassforPred = {}
        for pred in self.domain['predicate']:
            res = self.database([['?a', pred, '?b']])
            for cl in self.domain:
                if res[0][0] in self.domain[cl]:
                    EveryclassDim[cl] = len(self.domain[cl])
                    ClassIndex.add(cl)
                    lclass = cl
                if res[0][1] in self.domain[cl]:
                    EveryclassDim[cl] = len(self.domain[cl])
                    ClassIndex.add(cl)
                    rclass = cl
            ClassforPred[pred] = (lclass, rclass)
        self.ClassIndex = {Class:i for i,Class in enumerate(list(ClassIndex))}

        pos, neg = self.database._question(predicate)
        print('initPos', pos)
        print('initNeg', neg)
        self.domain['predicate'].remove(predicate)

        Todeduce = ['?'+ClassforPred[predicate][0], 
                    predicate, 
                    '?'+ClassforPred[predicate][1]]
        # Todeduce = ['?x', 
        #             predicate, 
        #             '?y']
        QueryList = []

        # variables = {'?x', '?y', '?z'}

        while len(neg):
            index = 0
            deduceMap = pd.DataFrame([], columns=['Predicate','Variable','Positive','Negative','InfoGain'], dtype=object)
            for pred in self.domain['predicate']:
                print("\nPredicate:", pred)
                lClass, rClass = ClassforPred[pred]
                l_var = '?'+lClass
                r_var = '?'+rClass
                cquery = [[l_var, pred, r_var]]
                qres = self.database(cquery)
                print("Query:", cquery)
                print("Result:", qres)
                posNum, negNum = 0, 0
                for res in qres:
                    if l_var == Todeduce[0] and r_var == Todeduce[1]:
                        posNum += self._cntWithValue(pos, 0, res[0], 1, res[1])
                        negNum += self._cntWithValue(neg, 0, res[0], 1, res[1])
                    if l_var == Todeduce[0]:
                        posNum += self._cntWithValue(pos, 0, res[0])
                        negNum += self._cntWithValue(neg, 0, res[0])
                    if r_var == Todeduce[1]:
                        posNum += self._cntWithValue(pos, 1, res[1])
                        negNum += self._cntWithValue(neg, 1, res[1])
                print('Posnum, Negnum:', posNum, negNum)
                if posNum == 0:
                    InfoGain = NA
                else:
                    InfoGain = posNum*(np.log2(1.0*posNum/(posNum+negNum)) - np.log2(1.0*len(pos)/(len(pos)+len(neg))))
                deduceMap.loc[index] = [pred, [l_var, r_var], posNum, negNum, InfoGain]
                index += 1
                print(deduceMap)

            # print(deduceMap)
            max_infoGain = deduceMap.loc[deduceMap["InfoGain"].idxmax()]
            queryTmp = max_infoGain.Variable
            queryTmp.insert(1, max_infoGain.Predicate)
            QueryList.append(queryTmp)
            AllVar = self._getAllvar(QueryList)
            result = self.database(QueryList)
            new_neg = []
            for res in result:
                plc, val = [], []
                for idx in range(len(AllVar)):
                    if AllVar[idx] == Todeduce[0]:
                        plc.append(0)
                        val.append(res[idx])
                    if AllVar[idx] == Todeduce[1]:
                        plc.append(1)
                        val.append(res[idx])
                if len(plc) == 2:
                    new_neg += self._delteWithValue(neg, plc[0], val[0], plc[1], val[1])
                elif len(plc) == 1:
                    new_neg += self._delteWithValue(neg, plc[0], val[0])
            neg = new_neg
            print('New neg:', neg)
        print("\n===Deduce finished===")
        print(PRED)
        if PRED[0][0] != '?':
            QueryList = self._replaceAllvar(Todeduce[0], PRED[0], QueryList)
        if PRED[2][0] != '?':
            QueryList = self._replaceAllvar(Todeduce[2], PRED[2], QueryList)
        print(self.database(QueryList))