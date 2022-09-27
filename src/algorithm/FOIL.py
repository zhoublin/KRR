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
    
    # predicate(entity,variable), 获取谓词中entity所属类
    def _getClass(self, entity):
        for d in self.domain:
            if entity in self.domain[d]:
                return d
        return None

    # 格式化输出
    def _format(self, querylist, Todeduce):
        tode = copy.deepcopy(Todeduce)
        allVar = self._getAllvar(querylist)
        ret = '(∀ ' + ')(∀ '.join([var[1:] if var[0]=='?' else var for var in allVar]) + ') '
        tmp = []
        for q in querylist[::-1]:   #
            q = (q[0][1:] if q[0][0]=='?' else q[0], q[1], q[2][1:] if q[2][0]=='?' else q[2])
            tmp.append(q[1] + '(' + q[0] + ',' + q[2] + ')')
        ret += ' ∧ '.join(tmp)
        tode = [tode[0][1:] if tode[0][0]=='?' else tode[0], tode[1], tode[2][1:] if tode[2][0]=='?' else tode[2]]
        ret += ' → ' + tode[1] + '(' + tode[0] + ',' + tode[2] + ')'
        return ret
    
    # def _getClassFromVaridx(self, string):
    #     classIdx = string[1:].split('_')[0]
    #     for _class in self.ClassIndex:
    #         if classIdx == self.ClassIndex[_class]:
    #             return _class
    #     return None

    # def _getVarindx(self, classIndex, entityIndx):
    #     return "v{}_{}".format(classIndex, entityIndx)

    # 获取查询中的所有变量
    def _getAllvar(self, queryList):
        varList = []
        for query in queryList:
            if query[0][0] == '?' and query[0] not in varList:
                varList.append(query[0])
            if query[2][0] == '?' and query[2] not in varList:
                varList.append(query[2])
        return varList

    # 将对应变量替换为给定值
    def _replaceAllvar(self, repVar, repValue, queryList):
        curt = copy.deepcopy(queryList)
        record = -1
        for i in range(len(curt)):
            for j in range(len(curt[i])):
                if curt[i][j] == repVar:
                    curt[i][j] = repValue
                    record = j
        return curt, record

    # 计算集合cset中var取值为value的样本数
    def _cntWithValue(self, cset, Query, var, value):
        '''
        var: variables
        value
        '''
        cnt = 0
        for val in value:
            tmp = copy.deepcopy(Query)
            index1, index2 = -1, -1
            record = -1
            for i,v in enumerate(var):
                if v == tmp[0]:
                    tmp, index1 = self._replaceAllvar(v, val[i], [tmp])
                    tmp = tmp[0]
                    record = i
                if v == tmp[2]:
                    tmp, index2 = self._replaceAllvar(v, val[i], [tmp])
                    tmp = tmp[0]
                    record = i
            if index1 != -1 and index2 != -1:
                if (tmp[0], tmp[2]) in cset:
                    cnt += 1
            elif index1 != -1:
                tmp_set = []
                for i in range(len(var)):
                    if i != record:
                        tmp_set += [(tmp[0], val[i]) for val in value]
                tmp_set = set(cset) - set(tmp_set)
                cnt += [c[0] for c in tmp_set].count(tmp[0])
            elif index2 != -1:
                tmp_set = []
                for i in range(len(var)):
                    if i != record:
                        tmp_set += [(val[i], tmp[2]) for val in value]
                tmp_set = set(cset) - set(tmp_set)
                cnt += [c[1] for c in tmp_set].count(tmp[2])
        return cnt
    
    # 删除集合中变量var取值为value的样本
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
        
    # FOIL算法推导过程
    def _deduce(self, PRED):
        '''
        pred: A tuple (a, p, b) to be deduced.
        a, p, b = '?var'/entity
        '''
        predicate = PRED[1]

        # 获取所有谓词的两个变量所属类
        ClassforPred = {}
        for pred in self.domain['predicate']:
            res = self.database([['?a', pred, '?b']])
            for cl in self.domain:
                if res[0][0] in self.domain[cl]:
                    lclass = cl
                if res[0][1] in self.domain[cl]:
                    rclass = cl
            ClassforPred[pred] = (lclass, rclass)
        print(ClassforPred)

        # 获取正例和负例集合
        pos, neg = self.database._question(predicate)
        curt_domain = copy.deepcopy(self.domain)
        curt_domain['predicate'].remove(predicate)

        # 生成待推导谓词
        Todeduce = ['?'+ClassforPred[predicate][0]+'_x', 
                    predicate, 
                    '?'+ClassforPred[predicate][1]+'_y']

        variables = {'_x', '_y', '_z'}
        print(Todeduce)

        QueryList = []
        while len(neg):
            '''
            负例集为空时停止
            '''
            print()
            print('initPos', pos)
            print('initNeg', neg)
            print('pos num:', len(pos))
            print('neg num:', len(neg))
            print('QueryList:', QueryList)
            index = 0
            deduceMap = pd.DataFrame([], columns=['Predicate','Variable','Positive','Negative','InfoGain'], dtype=object)
            for pred in curt_domain['predicate']:
                # print("\nPredicate:", pred)
                for i in variables:
                    for order in [1, -1]:
                        # 为谓词pred生成变量
                        lClass, rClass = ClassforPred[pred]
                        prefix = list(variables - {i})[::order]
                        l_var, r_var = '?'+lClass+prefix[0], '?'+rClass+prefix[1]
                        
                        if [l_var, pred, r_var] in QueryList:
                            continue
                        # 在背景知识集中查询
                        cquery = [[l_var, pred, r_var]] + QueryList
                        qres = self.database(cquery)
                        AllVar = self._getAllvar(cquery)

                        # 根据查询结果获取正例和负例数
                        posNum = self._cntWithValue(pos, Todeduce, AllVar, qres)
                        negNum = self._cntWithValue(neg, Todeduce, AllVar, qres)

                        # 计算信息增益
                        if posNum == 0:
                            InfoGain = NA
                        else:
                            InfoGain = posNum*(np.log2(1.0*posNum/(posNum+negNum)) - np.log2(1.0*len(pos)/(len(pos)+len(neg))))
                        
                        # 添加项
                        deduceMap.loc[index] = [pred, [l_var, r_var], posNum, negNum, InfoGain]
                        index += 1

            print("\033[0;35m{}\033[0m".format(deduceMap))
            # 使用具有最大信息增益的谓词
            max_infoGain = deduceMap.loc[deduceMap["InfoGain"].idxmax()]
            queryTmp = max_infoGain.Variable
            queryTmp.insert(1, max_infoGain.Predicate)
            QueryList.append(queryTmp)
            AllVar = self._getAllvar(QueryList)
            result = self.database(QueryList)
            print(self._format(QueryList, Todeduce))
            print(result)

            # 删除不满足约束的负例
            neg = self._delteWithValue(neg, Todeduce, AllVar, result)
        print("\n===Deduce finished===")
        print('Question:', PRED)
        print(self._format(QueryList, Todeduce))
        # if PRED[0][0] != '?':
        #     QueryList, _ = self._replaceAllvar(Todeduce[0], PRED[0], QueryList)
        # if PRED[2][0] != '?':
        #     QueryList, _ = self._replaceAllvar(Todeduce[2], PRED[2], QueryList)
        # print(QueryList)
        result = []
        for val in self.database(QueryList):
            solution = {}
            for i, var in enumerate(self._getAllvar(QueryList)):
                solution[var] = val[i]
            result.append(solution)
        return result

    def __call__(self, question):
        if question[1][0] == '?':
            res = self.database([question])
            if len(res) > 0:
                return res
        if question[1] not in self.domain['predicate']:
            print("[Error] Can not deduce (inexistent predicate)")
            return

        for res in self._deduce(question):
            print("\033[0;34m{}\033[0m".format(res))
        res = self.database._query([q if q[0]!='?' else 'none' for q in question])
        if len(res) == 1:
            print("Knowledge In database:")
            print("\033[0;34m{}\033[0m".format(self.database._query([q if q[0]!='?' else 'none' for q in question])))