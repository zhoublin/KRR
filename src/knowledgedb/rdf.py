# -*- Coding: utf-8 -*-
# @Time    : 2022.9.25
# @Author  : zhoubolin
# @File    : rdf.py

import os
import json
from telnetlib import SE
import rdflib
from rdflib import RDF, Namespace, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS

class RDF(object):
    def __init__(self):
        self.graph = rdflib.Graph()
        self.graph.parse(f'{os.getcwd()}/knowledgedb/initDB.rdf', format='xml')
        with open(f"{os.getcwd()}/knowledgedb/nameSpace.json") as f:
            self.domain = json.load(f)

    # 删除知识
    def _delete(self, knowledge: list):
        assert knowledge.count(None) == 0

        knowledge = list(map(lambda a: str.lower(a), knowledge))
        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        knldge = tuple([URIRef(namesPerson[kn]) for kn in knowledge])
        self.graph.remove(knldge)

        for it in knowledge:
            for key in self.domain:
                if it in self.domain[key]:
                    self.domain[key].remove(it)
        with open(f"{os.getcwd()}/knowledgedb/nameSpace.json", 'w') as f:
            json.dump(self.domain, f)
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

    # 增加知识
    def _update(self, knowledge: list):
        '''
        knowledge: [
            (v1, is, which_Class)
            (v2, is, which_Class)
            (v1, predicate, v2)
        ]
        '''
        assert len(knowledge) == 3

        knowledge = [list(map(lambda a: str.lower(a), kn)) for kn in knowledge]
        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        for i, know in enumerate(knowledge):
            knldge = tuple([URIRef(namesPerson[kn]) for kn in know])
            self.graph.add(knldge)
            if i < 2:
                if know[2] in self.domain:
                    self.domain[know[2]].append(know[0])
                else:    
                    self.domain[know[2]] = [know[0]]
            else:
                self.domain["predicate"].append(know[1])

        with open(f"{os.getcwd()}/knowledgedb/nameSpace.json", 'w') as f:
            json.dump(self.domain, f)
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

    # 单谓词查询
    def _query(self, query: list):
        '''
        query: ['none'/entity, predicate, 'none'/entity]
        '''
        query = list(map(lambda a: str.lower(a), query))

        # 生成SPARQL查询语句
        variable = ['?'+chr(0x61+i) if query[i] == "none" else "nmPerson:"+query[i] for i in range(len(query))]
        var = [v for v in variable if v[0] == '?']
        _query = "SELECT {} WHERE {{{}.}}".format(
                            " ".join(var),
                            " ".join(variable))
        # print('Query:', _query)
        result = list(self.graph.query(_query))

        # 去除URIRef前缀
        extr_res = []
        for item in result:
            res = tuple([str(it).strip().split('#')[-1] for it in item])
            if len(res) == len(set(res)):
                extr_res.append(res)
        return extr_res

    # 获取待推导谓词对应的正例集和负例集
    def _question(self, ques: str):
        '''
        ques: predicate to be deduced
        '''
        self.neg = []
        self.pos = self._query(['None', ques, 'None'])
        for p in [pred for pred in self.domain["predicate"] if pred != ques]:
            self.neg += self._query(['None', p, 'None'])
        return self.pos, self.neg

    # 多谓词查询
    def __call__(self, query: list[list]):
        '''
        query: [list, list, ...]
        list: [var1/entity1, predicate, var2/entity2]
        # note: 1. Format of var should be ?chr
        '''
        query = [list(map(lambda a: str.lower(a), q)) for q in query]

        var = []
        for que in query:
            for q in que:
                if q[0]=='?' and q not in var:
                    var.append(q)
        variable = [" ".join(["nmPerson:"+q if q[0]!='?' else q for q in que]) for que in query]
        
        # 生成SPARQL查询语句
        _query = "SELECT {} WHERE {{{}.}}".format(
                            " ".join(var),
                            ". ".join(variable))
        result = list(self.graph.query(_query))

        extr_res = []
        for item in result:
            res = tuple([str(it).strip().split('#')[-1] for it in item])
            if len(res) == len(set(res)):
                extr_res.append(res)
        return extr_res

    @staticmethod
    def buildKDB_Family():
        import rdflib
        from rdflib import RDF, Namespace, URIRef, Literal
        from rdflib.namespace import OWL, RDF, RDFS
        graph = rdflib.Graph()

        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        # entity
        James = URIRef(namesPerson["james"])
        David = URIRef(namesPerson["david"])
        Ann = URIRef(namesPerson["ann"])
        Mike = URIRef(namesPerson["mike"])
        # predicates
        Mother = URIRef(namesPerson["mother"])
        Father = URIRef(namesPerson["father"])
        Couple = URIRef(namesPerson["couple"])
        Sibling = URIRef(namesPerson["sibling"])

        # graph.add((James, Couple, David))
        graph.add((James, Mother, Ann))
        graph.add((James, Mother, Mike))
        graph.add((David, Couple, James))
        graph.add((David, Father, Mike))
        graph.add((Ann, Sibling, Mike))
        # graph.add((Mike, Sibling, Ann))

        graph.bind("nmPerson", namesPerson)

        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

        os.system(f"cp {os.getcwd()}/configs/familyProblem.json {os.getcwd()}/knowledgedb/nameSpace.json")
    
    @staticmethod
    def buildKDB_clan():
        import rdflib
        from rdflib import RDF, Namespace, URIRef, Literal
        from rdflib.namespace import OWL, RDF, RDFS
        graph = rdflib.Graph()

        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        # entity
        Frank = URIRef(namesPerson["frank"])
        Rebecca = URIRef(namesPerson["rebecca"])
        Abe = URIRef(namesPerson["abe"])
        Alan = URIRef(namesPerson["alan"])
        Joan = URIRef(namesPerson["joan"])
        Sean = URIRef(namesPerson["sean"])
        Jan = URIRef(namesPerson["jan"])
        Jane = URIRef(namesPerson["jane"])

        # predicates
        Mother = URIRef(namesPerson["mother"])
        Father = URIRef(namesPerson["father"])
        Husband = URIRef(namesPerson["husband"])
        Wife = URIRef(namesPerson["wife"])
        Sibling = URIRef(namesPerson["sibling"])

        Son_of = URIRef(namesPerson["son_of"])
        Daughter_of = URIRef(namesPerson["daughter_of"])
        Grandfather = URIRef(namesPerson["grandfather"])
        # Grandson = URIRef(namesPerson["grandson"])
        Grandmother = URIRef(namesPerson["grandmother"])
        # Granddaughter = URIRef(namesPerson["granddaughter"])

        graph.add((Frank, Husband, Rebecca))
        graph.add((Frank, Father, Alan))
        graph.add((Frank, Father, Abe))
        graph.add((Rebecca, Wife, Frank))
        graph.add((Rebecca, Mother, Abe))
        graph.add((Abe, Sibling, Alan))
        graph.add((Alan, Sibling, Abe))
        graph.add((Alan, Husband, Joan))
        # graph.add((Joan, Wife, Alan))
        graph.add((Joan, Father, Sean))
        graph.add((Sean, Father, Jane))
        graph.add((Jan, Mother, Jane))

        graph.add((Alan, Daughter_of, Frank))
        # graph.add((Alan, Daughter_of, Rebecca))
        graph.add((Abe, Son_of, Rebecca))
        graph.add((Sean, Son_of, Joan))
        graph.add((Jane, Daughter_of, Jan))

        graph.add((Frank, Grandfather, Sean))

        graph.add((Rebecca, Grandmother, Sean))
        graph.add((Rebecca, Grandmother, Jan))

        graph.add((Alan, Grandmother, Jane))
        graph.add((Joan, Grandfather, Jane))

        graph.bind("nmPerson", namesPerson)

        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

        os.system(f"cp {os.getcwd()}/configs/clanProblem.json {os.getcwd()}/knowledgedb/nameSpace.json")

    @staticmethod
    def buildKDB():
        import rdflib
        from rdflib import RDF, Namespace, URIRef, Literal
        from rdflib.namespace import OWL, RDF, RDFS
        graph = rdflib.Graph()

        # 构造链接数据工具的命名空间
        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")

        # 创建节点并添加到图
        Person = URIRef(namesPerson["person"])
        British = URIRef(namesPerson["british"])
        Spaniard = URIRef(namesPerson["spaniard"])
        Japanese = URIRef(namesPerson["japanese"])
        Italian = URIRef(namesPerson["italian"])
        Norwegian = URIRef(namesPerson["norwegian"])

        person_in_1stHouse = URIRef(namesPerson["person_in_1sthouse"])
        person_in_2ndHouse = URIRef(namesPerson["person_in_2ndhouse"])
        person_in_middleHouse = URIRef(namesPerson["person_in_middlehouse"])
        person_in_4thHouse = URIRef(namesPerson["person_in_4thhouse"])
        person_in_5thHouse = URIRef(namesPerson["person_in_5thhouse"])

        person_drink_Milk = URIRef(namesPerson["person_drink_milk"])
        person_drink_Tea = URIRef(namesPerson["person_drink_tea"])
        person_drink_Orange_juice = URIRef(namesPerson["person_drink_orange_juice"])
        person_drink_Coffee = URIRef(namesPerson["person_drink_coffee"])
        person_drink_Water = URIRef(namesPerson["person_drink_water"])

        person_has_Dog = URIRef(namesPerson["person_have_dog"])
        person_has_Horse = URIRef(namesPerson["person_have_horse"])
        person_has_Snail = URIRef(namesPerson["person_have_snail"])
        person_has_Fox = URIRef(namesPerson["person_have_fox"])
        person_has_Zebra = URIRef(namesPerson["person_have_zebra"])

        person_job_Photographer = URIRef(namesPerson["person_job_photographer"])
        person_job_Diplomat = URIRef(namesPerson["person_job_diplomat"])
        person_job_Violinist = URIRef(namesPerson["person_job_violinist"])
        person_job_Doctor = URIRef(namesPerson["person_job_doctor"])
        person_job_Painter = URIRef(namesPerson["person_job_painter"])
        ### ===========================================
        House = URIRef(namesPerson["house"])
        Location = URIRef(namesPerson["location"])
        First = URIRef(namesPerson["1st"])
        Second = URIRef(namesPerson["2nd"])
        Middle = URIRef(namesPerson["middle"])
        Fourth = URIRef(namesPerson["4th"])
        Fifth = URIRef(namesPerson["5th"])
        FirstHouse = URIRef(namesPerson["1sthouse"])
        SecondHouse = URIRef(namesPerson["2ndhouse"])
        MiddleHouse = URIRef(namesPerson["middlehouse"])
        FourthHouse = URIRef(namesPerson["4thhouse"])
        FifthHouse = URIRef(namesPerson["5thhouse"])

        RedHouse = URIRef(namesPerson["redhouse"])
        GreenHouse = URIRef(namesPerson["greenhouse"])
        WhiteHouse = URIRef(namesPerson["whitehouse"])
        YellowHouse = URIRef(namesPerson["yellowhouse"])
        BlueHouse = URIRef(namesPerson["bluehouse"])

        British_House = URIRef(namesPerson["british_house"])
        Spaniard_House = URIRef(namesPerson["spaniard_house"])
        Japanese_House = URIRef(namesPerson["japanese_house"])
        Italian_House = URIRef(namesPerson["italian_house"])
        Norwegian_House = URIRef(namesPerson["norwegian_house"])

        person_drink_Milk_House = URIRef(namesPerson["person_drink_milk_house"])
        person_drink_Tea_House = URIRef(namesPerson["person_drink_tea_house"])
        person_drink_Orange_juice_House = URIRef(namesPerson["person_drink_orange_juice_house"])
        person_drink_Coffee_House = URIRef(namesPerson["person_drink_coffee_house"])
        person_drink_Water_House = URIRef(namesPerson["person_drink_water_house"])
        person_has_Dog_House = URIRef(namesPerson["person_has_dog_house"])
        person_has_Horse_House = URIRef(namesPerson["person_has_horse_house"])
        person_has_Snail_House = URIRef(namesPerson["person_has_snail_house"])
        person_has_Fox_House = URIRef(namesPerson["person_has_fox_house"])
        person_has_Zebra_House = URIRef(namesPerson["person_has_zebra_house"])
        person_job_Photographer_House = URIRef(namesPerson["person_job_photographer_house"])
        person_job_Diplomat_House = URIRef(namesPerson["person_job_diplomat_house"])
        person_job_Violinist_House = URIRef(namesPerson["person_job_violinist_house"])
        person_job_Doctor_House = URIRef(namesPerson["person_job_doctor_house"])
        person_job_Painter_House = URIRef(namesPerson["person_job_painter_house"])

        ### ===========================================
        Drink = URIRef(namesPerson["drink"])
        Milk = URIRef(namesPerson["milk"])
        Tea = URIRef(namesPerson["tea"])
        Orange_juice = URIRef(namesPerson["orange_juice"])
        Coffee = URIRef(namesPerson["coffee"])
        Water = URIRef(namesPerson["water"])

        Pet = URIRef(namesPerson["pet"])
        Dog = URIRef(namesPerson["dog"])
        Horse = URIRef(namesPerson["horse"])
        Snail = URIRef(namesPerson["snail"])
        Fox = URIRef(namesPerson["fox"])
        Zebra = URIRef(namesPerson["zebra"])

        Job = URIRef(namesPerson["job"])
        Photographer = URIRef(namesPerson["photographer"])
        Diplomat = URIRef(namesPerson["diplomat"])
        Violinist = URIRef(namesPerson["violinist"])
        Doctor = URIRef(namesPerson["doctor"])
        Painter = URIRef(namesPerson["painter"])

        # predicate
        In = URIRef(namesPerson["in"])  # house -> loc
        live_in = URIRef(namesPerson["live_in"])
        has_pet = URIRef(namesPerson["has_pet"])
        like_drink = URIRef(namesPerson["like_drink"])
        has_job = URIRef(namesPerson["has_job"])
        RightsideOf = URIRef(namesPerson["right_side_of"])
        LeftsideOf = URIRef(namesPerson["left_side_of"])
        liveNextto = URIRef(namesPerson["livenextto"])  # person -> person  
        Nextto = URIRef(namesPerson["next_to"])    # person -> house
        

        graph.add((FirstHouse, In, First))
        graph.add((SecondHouse, In, Second))
        graph.add((MiddleHouse, In, Middle))
        graph.add((FourthHouse, In, Fourth))
        graph.add((FifthHouse, In, Fifth))

        graph.add((FirstHouse, LeftsideOf, SecondHouse))
        graph.add((SecondHouse, LeftsideOf, MiddleHouse))
        graph.add((MiddleHouse, LeftsideOf, FourthHouse))
        graph.add((FourthHouse, LeftsideOf, FifthHouse))

        graph.add((SecondHouse, RightsideOf, FirstHouse))
        graph.add((MiddleHouse, RightsideOf, SecondHouse))
        graph.add((FourthHouse, RightsideOf, MiddleHouse))
        graph.add((FifthHouse, RightsideOf, FourthHouse))
        #---------------------------------------
        # 英国人住在红色的房子里
        graph.add((British, live_in, RedHouse))
        # 西班牙人养了一条狗  
        graph.add((Spaniard, has_pet, Dog))
        # 日本人是一个油漆工
        graph.add((Japanese, has_job, Painter))
        # 意大利人喜欢喝茶      
        graph.add((Italian, like_drink, Tea))
        # 挪威人住在左边的第一个房子里      
        graph.add((Norwegian, live_in, FirstHouse))
        # 绿房子在白房子的右边    
        graph.add((GreenHouse, RightsideOf, WhiteHouse))  
        # 摄影师养了一只蜗牛        
        graph.add((person_job_Photographer, has_pet, Snail))
        # 外交官住在黄房子里        
        graph.add((person_job_Diplomat, live_in, YellowHouse))
        # 中间那个房子的人喜欢喝牛奶   
        graph.add((person_in_middleHouse, like_drink, Milk))     
        # 喜欢喝咖啡的人住在绿房子里        
        graph.add((person_drink_Coffee, live_in, GreenHouse))
        # 挪威人住在蓝色的房子旁边   
        graph.add((Norwegian, Nextto, BlueHouse))   
        # 小提琴家喜欢喝橘子汁
        graph.add((person_job_Violinist, like_drink, Orange_juice))
        # 养狐狸的人所住的房子与医生的房子相邻
        graph.add((person_has_Fox, liveNextto, person_job_Doctor))
        # 养马的人所住的房子与外交官的房子相邻
        graph.add((person_has_Horse, liveNextto, person_job_Diplomat))

        #### ------------ Additional
        graph.add((person_job_Painter, Nextto, WhiteHouse))
        graph.add((person_has_Horse, live_in, SecondHouse))
        graph.add((person_drink_Tea_House, LeftsideOf, Middle))
        graph.add((person_job_Diplomat, has_pet, Fox))
        graph.add((person_job_Violinist, live_in, WhiteHouse))
        graph.add((Spaniard, Nextto, RedHouse))
        graph.add((person_job_Photographer, liveNextto, person_has_Dog))
        graph.add((person_drink_Water, live_in, YellowHouse))
        graph.add((Italian_House, RightsideOf, FirstHouse))
        graph.add((RedHouse, In, Middle))
        graph.add((person_drink_Orange_juice, In, Fourth))
        graph.add((person_has_Zebra, In, Fifth))

        ### ------------- Others                        
        graph.add((Italian, live_in, Italian_House))
        graph.add((British, live_in, British_House))
        graph.add((Spaniard, live_in, Spaniard_House))
        graph.add((Japanese, live_in, Japanese_House))
        graph.add((Norwegian, live_in, Norwegian_House))


        graph.add((person_in_1stHouse, live_in, FirstHouse))
        graph.add((person_in_2ndHouse, live_in, SecondHouse))
        graph.add((person_in_4thHouse, live_in, FourthHouse))
        graph.add((person_in_middleHouse, live_in, MiddleHouse))
        graph.add((person_in_5thHouse, live_in, FifthHouse))

        graph.add((person_drink_Milk, like_drink, Milk))
        graph.add((person_drink_Coffee, like_drink, Coffee))
        graph.add((person_drink_Tea, like_drink, Tea))
        graph.add((person_drink_Water, like_drink, Water))
        graph.add((person_drink_Orange_juice, like_drink, Orange_juice))

        graph.add((person_has_Fox, has_pet, Fox))
        graph.add((person_has_Horse, has_pet, Horse))
        graph.add((person_has_Snail, has_pet, Snail))
        graph.add((person_has_Dog, has_pet, Dog))
        graph.add((person_has_Zebra, has_pet, Zebra))

        graph.add((person_job_Doctor, has_job, Doctor))
        graph.add((person_job_Diplomat, has_job, Diplomat))
        graph.add((person_job_Violinist, has_job, Violinist))
        graph.add((person_job_Photographer, has_job, Photographer)) 
        graph.add((person_job_Painter, has_job, Painter))                       

        graph.add((person_drink_Tea, live_in, person_drink_Tea_House))   
        graph.add((person_drink_Milk, live_in, person_drink_Milk_House))
        graph.add((person_drink_Orange_juice, live_in, person_drink_Orange_juice_House))
        graph.add((person_drink_Coffee, live_in, person_drink_Coffee_House))
        graph.add((person_drink_Water, live_in, person_drink_Water_House))
        graph.add((person_has_Dog, live_in, person_has_Dog_House))
        graph.add((person_has_Horse, live_in, person_has_Horse_House))
        graph.add((person_has_Snail, live_in, person_has_Snail_House))
        graph.add((person_has_Fox, live_in, person_has_Fox_House))
        graph.add((person_has_Zebra, live_in, person_has_Zebra_House))
        graph.add((person_job_Photographer, live_in, person_job_Photographer_House))
        graph.add((person_job_Diplomat, live_in, person_job_Diplomat_House))
        graph.add((person_job_Violinist, live_in, person_job_Violinist_House))
        graph.add((person_job_Doctor, live_in, person_job_Doctor_House))
        graph.add((person_job_Painter, live_in, person_job_Painter_House))
        # 绑定命名空间
        graph.bind("owl", OWL)
        graph.bind("nmPerson", namesPerson)

        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

        os.system(f"cp {os.getcwd()}/configs/zebraProblem.json {os.getcwd()}/knowledgedb/nameSpace.json")
        