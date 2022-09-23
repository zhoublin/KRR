# -*- Coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 

import rdflib
from rdflib import RDF, Namespace, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS

class RDF(object):
    def __init__(self):
        self.graph = rdflib.Graph()
        self.graph.parse('initKnow.rdf', format='xml')
        self.names = Namespace("http://xmlns.com/foaf/0.1/Person#")
        # 创建图

    def _update(self):
        pass

    @staticmethod
    def test():
        import rdflib
        from rdflib import RDF, Namespace, URIRef, Literal
        from rdflib.namespace import OWL, RDF, RDFS
        graph = rdflib.Graph()

        # 构造链接数据工具的命名空间
        namesPerson = Namespace("http://xmlns.com/foaf/0.1/Person#")
        namesHouse = Namespace("http://xmlns.com/foaf/0.1/House#")
        namesDrink = Namespace("http://xmlns.com/foaf/0.1/Drinks#")
        namesPet = Namespace("http://xmlns.com/foaf/0.1/Pet#")
        namesJob = Namespace("http://xmlns.com/foaf/0.1/Job#")

        # 创建节点并添加到图
        Person = URIRef(namesPerson["person"])
        British = URIRef(namesPerson["british"])
        Spaniard = URIRef(namesPerson["spaniard"])
        Japanese = URIRef(namesPerson["japanese"])
        Italian = URIRef(namesPerson["italian"])
        Norwegian = URIRef(namesPerson["norwegian"])

        House = URIRef(namesHouse["house"])
        Red = URIRef(namesHouse["red"])
        green = URIRef(namesHouse["green"])
        white = URIRef(namesHouse["white"])
        yellow = URIRef(namesHouse["yellow"])
        blue = URIRef(namesHouse["blue"])

        Drink = URIRef(namesDrink["drink"])
        Milk = URIRef(namesDrink["milk"])
        Tea = URIRef(namesDrink["tea"])
        Orange_juice = URIRef(namesDrink["orange_juice"])
        Coffee = URIRef(namesDrink["coffee"])
        Water = URIRef(namesDrink["water"])

        Pet = URIRef(namesPet["pet"])
        Dog = URIRef(namesPet["dog"])
        Horse = URIRef(namesPet["horse"])
        Snail = URIRef(namesPet["snail"])
        Fox = URIRef(namesPet["fox"])
        Zebra = URIRef(namesPet["zebra"])

        Job = URIRef(namesJob["job"])
        Photographer = URIRef(namesJob["photographer"])
        Diplomat = URIRef(namesJob["diplomat"])
        Violinist = URIRef(namesJob["violinist"])
        Doctor = URIRef(namesJob["doctor"])
        Painter = URIRef(namesJob["painter"])

        isPerson = URIRef(namesPerson["is"])
        isDrink = URIRef(namesDrink["is"])
        isHouse = URIRef(namesHouse["is"])
        isPet = URIRef(namesPet["is"])
        isJob = URIRef(namesJob["is"])

# Person:
        live_in = URIRef(namesPerson["live_in"])
        has_pet = URIRef(namesPerson["has_pet"])
        like_drink = URIRef(namesPerson["like_drink"])
        has_job = URIRef(namesPerson["has_job"])
# House:

        # is_enemy_of = URIRef(names["is_enemy_of"])
        # like_eat = URIRef(names["like_eat"])
        # is_relative_of = URIRef(names["is_relative_of"])

        # 将OWL数据添加到图
        graph.add((Person, RDF.type, OWL.Class))  # 将Animals设置为一个类
        graph.add((Person, RDFS.subClassOf, OWL.Thing))  # Animals为Thing的子类
        graph.add((Person, RDFS.label, Literal("The person type")))  # 添加标签
        graph.add((Person, RDFS.comment, Literal("The class of all person")))  # 添加描述
        graph.add((British, isPerson, Person))
        graph.add((Spaniard, isPerson, Person))
        graph.add((Japanese, isPerson, Person))
        graph.add((Italian, isPerson, Person))
        graph.add((Norwegian, isPerson, Person))

        graph.add((Drink, RDF.type, OWL.Class))
        graph.add((Drink, RDFS.subClassOf, OWL.Thing))
        graph.add((Drink, RDFS.label, Literal("The drink type")))
        graph.add((Drink, RDFS.comment, Literal("The class of all drink type")))
        graph.add((Milk, isDrink, Drink))
        graph.add((Tea, isDrink, Drink))
        graph.add((Orange_juice, isDrink, Drink))
        graph.add((Coffee, isDrink, Drink))
        graph.add((Water, isDrink, Drink))

        graph.add((House, RDF.type, OWL.Class))
        graph.add((House, RDFS.subClassOf, OWL.Thing))
        graph.add((House, RDFS.label, Literal("The House type")))
        graph.add((House, RDFS.comment, Literal("The class of all house")))
        graph.add((Red, isHouse, House))
        graph.add((green, isHouse, House))
        graph.add((white, isHouse, House))
        graph.add((yellow, isHouse, House))
        graph.add((blue, isHouse, House))

        graph.add((Pet, RDF.type, OWL.Class))
        graph.add((Pet, RDFS.subClassOf, OWL.Thing))
        graph.add((Pet, RDFS.label, Literal("The pet type")))
        graph.add((Pet, RDFS.comment, Literal("The class of all pet")))
        graph.add((Dog, isPet, Pet))
        graph.add((Horse, isPet, Pet))
        graph.add((Snail, isPet, Pet))
        graph.add((Fox, isPet, Pet))
        graph.add((Zebra, isPet, Pet))

        graph.add((Job, RDF.type, OWL.Class))
        graph.add((Job, RDFS.subClassOf, OWL.Thing))
        graph.add((Job, RDFS.label, Literal("The job type")))
        graph.add((Job, RDFS.comment, Literal("The class of all job")))
        graph.add((Photographer, isJob, Job))
        graph.add((Diplomat, isJob, Job))
        graph.add((Violinist, isJob, Job))
        graph.add((Doctor, isJob, Job))
        graph.add((Painter, isJob, Job))

        # 绑定命名空间
        graph.bind("owl", OWL)
        graph.bind("nmPerson", namesPerson)
        graph.bind("nmHouse", namesHouse)
        graph.bind("nmDrink", namesDrink)
        graph.bind("nmPet", namesPet)
        graph.bind("nmJob", namesJob)

        graph.serialize("foaf.rdf", format="xml")  # 保存为RDF/XML格式，当然也可以保存为其他格式
        graph.serialize("foaf.ttl", format="turtle")
        # graph.serialize("foaf.xml", format="xml")

        q = "SELECT ?a ?b WHERE {?a nmPerson:is ?b}"
        print(list(graph.query(q)))


if __name__ == "__main__":
    RDF.test()