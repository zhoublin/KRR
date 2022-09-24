# -*- Coding: utf-8 -*-
# @Time    : 2022.9.24
# @Author  : zhoublin
# @File    : rdf.py

import os
import json
import rdflib
from rdflib import RDF, Namespace, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS

class RDF(object):
    def __init__(self):
        self.graph = rdflib.Graph()
        self.graph.parse(f'{os.getcwd()}/knowledgedb/initDB.rdf', format='xml')
        with open(f"{os.getcwd()}/knowledgedb/nameSpace.json") as f:
            self.domain = json.load(f)

    def _initialize(self):
        print(os.system(f"cp {os.getcwd()}/configs/nameSpace_bk.json {os.getcwd()}/knowledgedb/nameSpace.json"))

    def _delete(self, knowledge: list):
        assert knowledge.count(None) == 0

        knowledge = list(map(lambda a: str.lower(a), knowledge))
        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        knldge = tuple([URIRef(namesPerson[kn]) for kn in knowledge])
        self.graph.remove(knldge)

        for it in knowledge:
            self.domain.pop(it)
        with open(f"{os.getcwd()}/knowledgedb/nameSpace.json", 'w') as f:
            json.dump(self.domain, f)
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

    def _update(self, knowledge: list):
        assert knowledge.count(None) == 0

        knowledge = list(map(lambda a: str.lower(a), knowledge))
        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        knldge = tuple([URIRef(namesPerson[kn]) for kn in knowledge])
        self.graph.add(knldge)

        self.domain.update({it:True for it in knowledge})
        with open(f"{os.getcwd()}/knowledgedb/nameSpace.json", 'w') as f:
            json.dump(self.domain, f)
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        self.graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")

    def _query(self, query: list):
        query = list(map(lambda a: str.lower(a), query))

        variable = ['?'+chr(0x61+i) if query[i] == "none" else "nmPerson:"+query[i] for i in range(len(query))]
        var = [v for v in variable if v[0] == '?']
        _query = "SELECT {} WHERE {{{}.}}".format(
                            " ".join(var),
                            " ".join(variable))
        print(_query)
        result = list(self.graph.query(_query))

        extr_res = []
        for item in result:
            extr_res.append(tuple([str(it).strip().split('#')[-1] for it in item]))
        return extr_res


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

        liveNextto = URIRef(namesPerson["liveNextto"])

        person_in_1stHouseHouse = URIRef(namesPerson["person_in_1stHouseHouse"])
        person_in_2ndHouseHouse = URIRef(namesPerson["person_in_2ndHouseHouse"])
        person_in_middleHouseHouse = URIRef(namesPerson["person_in_middleHouseHouse"])
        person_in_4thHouseHouse = URIRef(namesPerson["person_in_4thHouseHouse"])
        person_in_5thHouseHouse = URIRef(namesPerson["person_in_5thHouseHouse"])

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
        RightsideOf = URIRef(namesPerson["right_side_of"])
        LeftsideOf = URIRef(namesPerson["left_side_of"])
        Nextto = URIRef(namesPerson["next_to"])
        At = URIRef(namesPerson["at"])
        First = URIRef(namesPerson["1stHouse"])
        Second = URIRef(namesPerson["2ndHouse"])
        middleHouse = URIRef(namesPerson["middleHouse"])
        Fourth = URIRef(namesPerson["4thHouse"])
        Fifth = URIRef(namesPerson["5thHouse"])
        RedHouse = URIRef(namesPerson["redHouse"])
        GreenHouse = URIRef(namesPerson["greenHouse"])
        WhiteHouse = URIRef(namesPerson["whiteHouse"])
        YellowHouse = URIRef(namesPerson["yellowHouse"])
        BlueHouse = URIRef(namesPerson["blueHouse"])

        British_House = URIRef(namesPerson["british_House"])
        Spaniard_House = URIRef(namesPerson["spaniard_House"])
        Japanese_House = URIRef(namesPerson["japanese_House"])
        Italian_House = URIRef(namesPerson["italian_House"])
        Norwegian_House = URIRef(namesPerson["norwegian_House"])

        person_in_1stHouseHouse_House = URIRef(namesPerson["person_in_1stHouseHouse_House"])
        person_in_2ndHouseHouse_House = URIRef(namesPerson["person_in_2ndHouseHouse_House"])
        person_in_middleHouseHouse_House = URIRef(namesPerson["person_in_middleHouseHouse_House"])
        person_in_4thHouseHouse_House = URIRef(namesPerson["person_in_4thHouseHouse_House"])
        person_in_5thHouseHouse_House = URIRef(namesPerson["person_in_5thHouseHouse_House"])
        person_drink_Milk_House = URIRef(namesPerson["person_drink_Milk_House"])
        person_drink_Tea_House = URIRef(namesPerson["person_drink_Tea_House"])
        person_drink_Orange_juice_House = URIRef(namesPerson["person_drink_Orange_juice_House"])
        person_drink_Coffee_House = URIRef(namesPerson["person_drink_Coffee_House"])
        person_drink_Water_House = URIRef(namesPerson["person_drink_Water_House"])
        person_has_Dog_House = URIRef(namesPerson["person_has_Dog_House"])
        person_has_Horse_House = URIRef(namesPerson["person_has_Horse_House"])
        person_has_Snail_House = URIRef(namesPerson["person_has_Snail_House"])
        person_has_Fox_House = URIRef(namesPerson["person_has_Fox_House"])
        person_has_Zebra_House = URIRef(namesPerson["person_has_Zebra_House"])
        person_job_Photographer_House = URIRef(namesPerson["person_job_Photographer_House"])
        person_job_Diplomat_House = URIRef(namesPerson["person_job_Diplomat_House"])
        person_job_Violinist_House = URIRef(namesPerson["person_job_Violinist_House"])
        person_job_Doctor_House = URIRef(namesPerson["person_job_Doctor_House"])
        person_job_Painter_House = URIRef(namesPerson["person_job_Painter_House"])
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

        Is = URIRef(namesPerson["is"])

        # Person:
        live_in = URIRef(namesPerson["live_in"])
        has_pet = URIRef(namesPerson["has_pet"])
        like_drink = URIRef(namesPerson["like_drink"])
        has_job = URIRef(namesPerson["has_job"])
        # House:

        # 将OWL数据添加到图
        graph.add((Person, RDF.type, OWL.Class))
        graph.add((Person, RDFS.subClassOf, OWL.Thing))
        graph.add((Person, RDFS.label, Literal("The person type")))
        graph.add((Person, RDFS.comment, Literal("The class of all person")))
        graph.add((British, Is, Person))
        graph.add((Spaniard, Is, Person))
        graph.add((Japanese, Is, Person))
        graph.add((Italian, Is, Person))
        graph.add((Norwegian, Is, Person))
        graph.add((person_in_1stHouseHouse, Is, Person))
        graph.add((person_in_2ndHouseHouse, Is, Person))
        graph.add((person_in_middleHouseHouse, Is, Person))
        graph.add((person_in_4thHouseHouse, Is, Person))
        graph.add((person_in_5thHouseHouse, Is, Person))
        graph.add((person_drink_Milk, Is, Person))
        graph.add((person_drink_Tea, Is, Person))
        graph.add((person_drink_Orange_juice, Is, Person))
        graph.add((person_drink_Coffee, Is, Person))
        graph.add((person_drink_Water, Is, Person))
        graph.add((person_has_Dog, Is, Person))
        graph.add((person_has_Horse, Is, Person))
        graph.add((person_has_Snail, Is, Person))
        graph.add((person_has_Fox, Is, Person))
        graph.add((person_has_Zebra, Is, Person))
        graph.add((person_job_Photographer, Is, Person))
        graph.add((person_job_Diplomat, Is, Person))
        graph.add((person_job_Violinist, Is, Person))
        graph.add((person_job_Doctor, Is, Person))
        graph.add((person_job_Painter, Is, Person))

        graph.add((Drink, RDF.type, OWL.Class))
        graph.add((Drink, RDFS.subClassOf, OWL.Thing))
        graph.add((Drink, RDFS.label, Literal("The drink type")))
        graph.add((Drink, RDFS.comment, Literal("The class of all drink type")))
        graph.add((Milk, Is, Drink))
        graph.add((Tea, Is, Drink))
        graph.add((Orange_juice, Is, Drink))
        graph.add((Coffee, Is, Drink))
        graph.add((Water, Is, Drink))

        graph.add((House, RDF.type, OWL.Class))
        graph.add((House, RDFS.subClassOf, OWL.Thing))
        graph.add((House, RDFS.label, Literal("The House type")))
        graph.add((House, RDFS.comment, Literal("The class of all house")))
        graph.add((RedHouse, Is, House))
        graph.add((GreenHouse, Is, House))
        graph.add((WhiteHouse, Is, House))
        graph.add((YellowHouse, Is, House))
        graph.add((BlueHouse, Is, House))
        graph.add((First, Is, House))
        graph.add((Second, Is, House))
        graph.add((middleHouse, Is, House))
        graph.add((Fourth, Is, House))
        graph.add((Fifth, Is, House))

        graph.add((British_House, Is, House))
        graph.add((Spaniard_House, Is, House))
        graph.add((Japanese_House, Is, House))
        graph.add((Italian_House, Is, House))
        graph.add((Norwegian_House, Is, House))

        graph.add((person_in_1stHouseHouse_House, Is, House))
        graph.add((person_in_2ndHouseHouse_House, Is, House))
        graph.add((person_in_middleHouseHouse_House, Is, House))
        graph.add((person_in_4thHouseHouse_House, Is, House))
        graph.add((person_in_5thHouseHouse_House, Is, House))
        graph.add((person_drink_Milk_House, Is, House))
        graph.add((person_drink_Tea_House, Is, House))
        graph.add((person_drink_Orange_juice_House, Is, House))
        graph.add((person_drink_Coffee_House, Is, House))
        graph.add((person_drink_Water_House, Is, House))
        graph.add((person_has_Dog_House, Is, House))
        graph.add((person_has_Horse_House, Is, House))
        graph.add((person_has_Snail_House, Is, House))
        graph.add((person_has_Fox_House, Is, House))
        graph.add((person_has_Zebra_House, Is, House))
        graph.add((person_job_Photographer_House, Is, House))
        graph.add((person_job_Diplomat_House, Is, House))
        graph.add((person_job_Violinist_House, Is, House))
        graph.add((person_job_Doctor_House, Is, House))
        graph.add((person_job_Painter_House, Is, House))

        ### ================================================
        ### ================================================

        graph.add((Pet, RDF.type, OWL.Class))
        graph.add((Pet, RDFS.subClassOf, OWL.Thing))
        graph.add((Pet, RDFS.label, Literal("The pet type")))
        graph.add((Pet, RDFS.comment, Literal("The class of all pet")))
        graph.add((Dog, Is, Pet))
        graph.add((Horse, Is, Pet))
        graph.add((Snail, Is, Pet))
        graph.add((Fox, Is, Pet))
        graph.add((Zebra, Is, Pet))

        graph.add((Job, RDF.type, OWL.Class))
        graph.add((Job, RDFS.subClassOf, OWL.Thing))
        graph.add((Job, RDFS.label, Literal("The job type")))
        graph.add((Job, RDFS.comment, Literal("The class of all job")))
        graph.add((Photographer, Is, Job))
        graph.add((Diplomat, Is, Job))
        graph.add((Violinist, Is, Job))
        graph.add((Doctor, Is, Job))
        graph.add((Painter, Is, Job))
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
        graph.add((First, LeftsideOf, Second))
        graph.add((Second, LeftsideOf, middleHouse))
        graph.add((middleHouse, LeftsideOf, Fourth))
        graph.add((Fourth, LeftsideOf, Fifth))
        graph.add((First, Nextto, Second))
        graph.add((Second, Nextto, middleHouse))
        graph.add((middleHouse, Nextto, Fourth))
        graph.add((Fourth, Nextto, Fifth))

        graph.add((Second, RightsideOf, First))
        graph.add((middleHouse, RightsideOf, Second))
        graph.add((Fourth, RightsideOf, middleHouse))
        graph.add((Fifth, RightsideOf, Fourth))
        graph.add((Second, Nextto, First))
        graph.add((middleHouse, Nextto, Second))
        graph.add((Fourth, Nextto, middleHouse))
        graph.add((Fifth, Nextto, Fourth))

        graph.add((Norwegian, live_in, First))
        # 绿房子在白房子的右边    
        graph.add((GreenHouse, RightsideOf, WhiteHouse))  
        # 摄影师养了一只蜗牛        
        graph.add((Photographer, has_pet, Snail))
        # 外交官住在黄房子里        
        graph.add((Diplomat, live_in, YellowHouse))
        # 中间那个房子的人喜欢喝牛奶   
        graph.add((person_in_middleHouseHouse, like_drink, Milk))     
        # 喜欢喝咖啡的人住在绿房子里        
        graph.add((person_drink_Coffee, live_in, GreenHouse))
        # 挪威人住在蓝色的房子旁边   
        graph.add((Norwegian, liveNextto, BlueHouse))   
        # 小提琴家喜欢喝橘子汁
        graph.add((Violinist, like_drink, Orange_juice))
        # 养狐狸的人所住的房子与医生的房子相邻
        graph.add((person_has_Fox_House, Nextto, person_job_Doctor_House))
        # 养马的人所住的房子与外交官的房子相邻
        graph.add((person_has_Horse_House, Nextto, person_job_Diplomat_House))

        # 绑定命名空间
        graph.bind("owl", OWL)
        graph.bind("nmPerson", namesPerson)

        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.rdf", format="xml")
        graph.serialize(f"{os.getcwd()}/knowledgedb/initDB.ttl", format="turtle")
        