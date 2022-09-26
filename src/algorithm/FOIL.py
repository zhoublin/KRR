# -*- Coding: utf-8 -*-
# @ Time    : 
# @ Author  : 
# @ File    : 

import copy
from functools import total_ordering
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

    def _format(self, querylist, Todeduce):
        allVar = self._getAllvar(querylist)
        ret = '(∀ ' + ')(∀ '.join([var[1:] for var in allVar]) + ') '
        tmp = []
        for q in querylist[::-1]:   #
            tmp.append(q[1] + '(' + q[0][1:] + ',' + q[2][1:] + ')')
        ret += ' ∧ '.join(tmp)
        ret += ' → ' + Todeduce[1] + '(' + Todeduce[0][1:] + ',' + Todeduce[2][1:] + ')'
        return ret
    
    def _format_VarAssign(self, allVar, result, Todeduce):
        pass

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
            if query[0][0] == '?' and query[0] not in varList:
                varList.append(query[0])
            if query[2][0] == '?' and query[2] not in varList:
                varList.append(query[2])
        return varList

    def _replaceAllvar(self, repVar, repValue, queryList):
        curt = copy.deepcopy(queryList)
        for i in range(len(curt)):
            for j in range(len(curt[i])):
                if curt[i][j] == repVar:
                    curt[i][j] = repValue
        return curt

    def _cntWithValue(self, cset, Query, var, value):
        '''
        var: variables
        value
        '''
        cnt = 0
        tmp = copy.deepcopy(Query)
        for val in value:
            tag = 0
            for i, v in enumerate(var):
                if Query[0] == v:
                    tmp[0] = val[i]
                    tag += 1
                elif Query[2] == v:
                    tmp[2] = val[i]
                    tag += 1
                if tag == 2: break
            if tag == 2:
                curt = tuple([tmp[0], tmp[2]])
                if curt in cset:
                    cnt += 1
                break
            elif tag:
                if tmp[0][0] != '?':
                    cnt += [c[0] for c in cset].count(tmp[0])
                if tmp[2][0] != '?':
                    cnt += [c[1] for c in cset].count(tmp[2])
                break
        return cnt
    
    def _delteWithValue(self, neg, Todeduce, AllVar, result):
        tmp = copy.deepcopy(Todeduce)
        update_neg = []
        for val in result:
            tag = 0
            for i,var in enumerate(AllVar):
                if tmp[0] == var:
                    tmp[0] = val[i]
                    tag += 1
                if tmp[2] == var:
                    tmp[2] = val[i]
                    tag += 1
                if tag == 2: break
            if tag == 2:
                curt = tuple([tmp[0], tmp[2]])
                if curt in neg:
                    update_neg.append(curt)
            elif tag:
                if tmp[0][0] != '?':
                    update_neg = [c for c in neg if tmp[0] == c[0]]
                if tmp[2][0] != '?':
                    update_neg = [c for c in neg if tmp[2] == c[1]]
        return update_neg

    def __call__(self, question):
        if question[1][0] == '?':
            res = self.database([question])
            if len(res) > 0:
                return res
        if question[1] not in self.domain['predicate']:
            print("[Error] Can not deduce (inexistent predicate)")
            return
        self._deduce(question)
        

    def _deduce(self, PRED):
        '''
        pred: A tuple (a, p, b) to be deduced.
        a, p, b = '?var'/entity
        '''
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
        print(ClassforPred)
        pos, neg = self.database._question(predicate)
        self.domain['predicate'].remove(predicate)

        Todeduce = ['?'+ClassforPred[predicate][0]+'_x', 
                    predicate, 
                    '?'+ClassforPred[predicate][1]+'_y']

        variables = {'_x', '_y', '_z'}

        QueryList = []
        while len(neg):
            print()
            print('initPos', pos)
            print('initNeg', neg)
            print('pos num:', len(pos))
            print('neg num:', len(neg))
            print('QueryList:', QueryList)
            index = 0
            deduceMap = pd.DataFrame([], columns=['Predicate','Variable','Positive','Negative','InfoGain'], dtype=object)
            for pred in self.domain['predicate']:
                # print("\nPredicate:", pred)
                for i in variables:
                    for order in [1, -1]:
                        lClass, rClass = ClassforPred[pred]
                        prefix = list(variables - {i})[::order]
                        l_var, r_var = '?'+lClass+prefix[0], '?'+rClass+prefix[1]
                        cquery = [[l_var, pred, r_var]] + QueryList
                        qres = self.database(cquery)
                        AllVar = self._getAllvar(cquery)
                        posNum = self._cntWithValue(pos, Todeduce, AllVar, qres)
                        negNum = self._cntWithValue(neg, Todeduce, AllVar, qres)
                        # print('Posnum, Negnum:', posNum, negNum)
                        if posNum == 0:
                            InfoGain = NA
                        else:
                            InfoGain = posNum*(np.log2(1.0*posNum/(posNum+negNum)) - np.log2(1.0*len(pos)/(len(pos)+len(neg))))
                        deduceMap.loc[index] = [pred, [l_var, r_var], posNum, negNum, InfoGain]
                        index += 1
                # print(deduceMap)

            print(deduceMap)
            max_infoGain = deduceMap.loc[deduceMap["InfoGain"].idxmax()]
            queryTmp = max_infoGain.Variable
            queryTmp.insert(1, max_infoGain.Predicate)
            QueryList.append(queryTmp)
            AllVar = self._getAllvar(QueryList)
            result = self.database(QueryList)
            print(self._format(QueryList, Todeduce))
            print(result)
            neg = self._delteWithValue(neg, Todeduce, AllVar, result)
        print("\n===Deduce finished===")
        print('Question:', PRED)
        print(self._format(QueryList, Todeduce))
        if PRED[0][0] != '?':
            QueryList = self._replaceAllvar(Todeduce[0], PRED[0], QueryList)
        if PRED[2][0] != '?':
            QueryList = self._replaceAllvar(Todeduce[2], PRED[2], QueryList)
        print(self.database(QueryList))
        # for i in range(len(Todeduce)):
        #     if PRED[i][0] != '?':
        #         Todeduce[i] = 
        # print(self._format_VarAssign(self._getAllvar(QueryList), self.database(QueryList), ))