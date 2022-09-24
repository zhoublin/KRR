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

        liveNextto = URIRef(namesPerson["liveNextto"])

        person_in_1stHouse = URIRef(namesPerson["person_in_1stHouse"])
        person_in_2ndHouse = URIRef(namesPerson["person_in_2ndHouse"])
        person_in_middleHouse = URIRef(namesPerson["person_in_middleHouse"])
        person_in_4thHouse = URIRef(namesPerson["person_in_4thHouse"])
        person_in_5thHouse = URIRef(namesPerson["person_in_5thHouse"])

        who_drink_Milk = URIRef(namesPerson["person_drink_milk"])
        who_drink_Tea = URIRef(namesPerson["person_drink_tea"])
        who_drink_Orange_juice = URIRef(namesPerson["person_drink_orange_juice"])
        who_drink_Coffee = URIRef(namesPerson["person_drink_coffee"])
        who_drink_Water = URIRef(namesPerson["person_drink_water"])

        who_has_Dog = URIRef(namesPerson["person_have_dog"])
        who_has_Horse = URIRef(namesPerson["person_have_horse"])
        who_has_Snail = URIRef(namesPerson["person_have_snail"])
        who_has_Fox = URIRef(namesPerson["person_have_fox"])
        who_has_Zebra = URIRef(namesPerson["person_have_zebra"])

        whos_job_Photographer = URIRef(namesPerson["person_job_photographer"])
        whos_job_Diplomat = URIRef(namesPerson["person_job_diplomat"])
        whos_job_Violinist = URIRef(namesPerson["person_job_violinist"])
        whos_job_Doctor = URIRef(namesPerson["person_job_doctor"])
        whos_job_Painter = URIRef(namesPerson["person_job_painter"])
### ===========================================
        House = URIRef(namesHouse["house"])
        Location = URIRef(namesHouse["location"])
        RightsideOf = URIRef(namesHouse["right_side_of"])
        LeftsideOf = URIRef(namesHouse["left_side_of"])
        Nextto = URIRef(namesHouse["next_to"])
        At = URIRef(namesHouse["at"])
        First = URIRef(namesHouse["1st"])
        Second = URIRef(namesHouse["2nd"])
        Middle = URIRef(namesHouse["middle"])
        Fourth = URIRef(namesHouse["4th"])
        Fifth = URIRef(namesHouse["5th"])
        RedHouse = URIRef(namesHouse["redHouse"])
        GreenHouse = URIRef(namesHouse["greenHouse"])
        WhiteHouse = URIRef(namesHouse["whiteHouse"])
        YellowHouse = URIRef(namesHouse["yellowHouse"])
        BlueHouse = URIRef(namesHouse["blueHouse"])

        British_House = URIRef(namesHouse["British_House"])
        Spaniard_House = URIRef(namesHouse["Spaniard_House"])
        Japanese_House = URIRef(namesHouse["Japanese_House"])
        Italian_House = URIRef(namesHouse["Italian_House"])
        Norwegian_House = URIRef(namesHouse["Norwegian_House"])

        person_in_1stHouse_House = URIRef(namesHouse["person_in_1stHouse_House"])
        person_in_2ndHouse_House = URIRef(namesHouse["person_in_2ndHouse_House"])
        person_in_middleHouse_House = URIRef(namesHouse["person_in_middleHouse_House"])
        person_in_4thHouse_House = URIRef(namesHouse["person_in_4thHouse_House"])
        person_in_5thHouse_House = URIRef(namesHouse["person_in_5thHouse_House"])
        who_drink_Milk_House = URIRef(namesHouse["who_drink_Milk_House"])
        who_drink_Tea_House = URIRef(namesHouse["who_drink_Tea_House"])
        who_drink_Orange_juice_House = URIRef(namesHouse["who_drink_Orange_juice_House"])
        who_drink_Coffee_House = URIRef(namesHouse["who_drink_Coffee_House"])
        who_drink_Water_House = URIRef(namesHouse["who_drink_Water_House"])
        who_has_Dog_House = URIRef(namesHouse["who_has_Dog_House"])
        who_has_Horse_House = URIRef(namesHouse["who_has_Horse_House"])
        who_has_Snail_House = URIRef(namesHouse["who_has_Snail_House"])
        who_has_Fox_House = URIRef(namesHouse["who_has_Fox_House"])
        who_has_Zebra_House = URIRef(namesHouse["who_has_Zebra_House"])
        whos_job_Photographer_House = URIRef(namesHouse["whos_job_Photographer_House"])
        whos_job_Diplomat_House = URIRef(namesHouse["whos_job_Diplomat_House"])
        whos_job_Violinist_House = URIRef(namesHouse["whos_job_Violinist_House"])
        whos_job_Doctor_House = URIRef(namesHouse["whos_job_Doctor_House"])
        whos_job_Painter_House = URIRef(namesHouse["whos_job_Painter_House"])
### ===========================================
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
        has_pet = URIRef(namesPerson["pet"])
        like_drink = URIRef(namesPerson["like_drink"])
        has_job = URIRef(namesPerson["job"])
# House:

        # 将OWL数据添加到图
        graph.add((Person, RDF.type, OWL.Class))
        graph.add((Person, RDFS.subClassOf, OWL.Thing))
        graph.add((Person, RDFS.label, Literal("The person type")))
        graph.add((Person, RDFS.comment, Literal("The class of all person")))
        graph.add((British, isPerson, Person))
        graph.add((Spaniard, isPerson, Person))
        graph.add((Japanese, isPerson, Person))
        graph.add((Italian, isPerson, Person))
        graph.add((Norwegian, isPerson, Person))
        graph.add((person_in_1stHouse, isPerson, Person))
        graph.add((person_in_2ndHouse, isPerson, Person))
        graph.add((person_in_middleHouse, isPerson, Person))
        graph.add((person_in_4thHouse, isPerson, Person))
        graph.add((person_in_5thHouse, isPerson, Person))
        graph.add((who_drink_Milk, isPerson, Person))
        graph.add((who_drink_Tea, isPerson, Person))
        graph.add((who_drink_Orange_juice, isPerson, Person))
        graph.add((who_drink_Coffee, isPerson, Person))
        graph.add((who_drink_Water, isPerson, Person))
        graph.add((who_has_Dog, isPerson, Person))
        graph.add((who_has_Horse, isPerson, Person))
        graph.add((who_has_Snail, isPerson, Person))
        graph.add((who_has_Fox, isPerson, Person))
        graph.add((who_has_Zebra, isPerson, Person))
        graph.add((whos_job_Photographer, isPerson, Person))
        graph.add((whos_job_Diplomat, isPerson, Person))
        graph.add((whos_job_Violinist, isPerson, Person))
        graph.add((whos_job_Doctor, isPerson, Person))
        graph.add((whos_job_Painter, isPerson, Person))

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
        graph.add((RedHouse, isHouse, House))
        graph.add((GreenHouse, isHouse, House))
        graph.add((WhiteHouse, isHouse, House))
        graph.add((YellowHouse, isHouse, House))
        graph.add((BlueHouse, isHouse, House))
        graph.add((First, isHouse, House))
        graph.add((Second, isHouse, House))
        graph.add((Middle, isHouse, House))
        graph.add((Fourth, isHouse, House))
        graph.add((Fifth, isHouse, House))

        graph.add((British_House, isHouse, House))
        graph.add((Spaniard_House, isHouse, House))
        graph.add((Japanese_House, isHouse, House))
        graph.add((Italian_House, isHouse, House))
        graph.add((Norwegian_House, isHouse, House))

        graph.add((person_in_1stHouse_House, isHouse, House))
        graph.add((person_in_2ndHouse_House, isHouse, House))
        graph.add((person_in_middleHouse_House, isHouse, House))
        graph.add((person_in_4thHouse_House, isHouse, House))
        graph.add((person_in_5thHouse_House, isHouse, House))
        graph.add((who_drink_Milk_House, isHouse, House))
        graph.add((who_drink_Tea_House, isHouse, House))
        graph.add((who_drink_Orange_juice_House, isHouse, House))
        graph.add((who_drink_Coffee_House, isHouse, House))
        graph.add((who_drink_Water_House, isHouse, House))
        graph.add((who_has_Dog_House, isHouse, House))
        graph.add((who_has_Horse_House, isHouse, House))
        graph.add((who_has_Snail_House, isHouse, House))
        graph.add((who_has_Fox_House, isHouse, House))
        graph.add((who_has_Zebra_House, isHouse, House))
        graph.add((whos_job_Photographer_House, isHouse, House))
        graph.add((whos_job_Diplomat_House, isHouse, House))
        graph.add((whos_job_Violinist_House, isHouse, House))
        graph.add((whos_job_Doctor_House, isHouse, House))
        graph.add((whos_job_Painter_House, isHouse, House))

### ================================================
### ================================================

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
        graph.add((Second, LeftsideOf, Middle))
        graph.add((Middle, LeftsideOf, Fourth))
        graph.add((Fourth, LeftsideOf, Fifth))
        graph.add((First, Nextto, Second))
        graph.add((Second, Nextto, Middle))
        graph.add((Middle, Nextto, Fourth))
        graph.add((Fourth, Nextto, Fifth))

        graph.add((Second, RightsideOf, First))
        graph.add((Middle, RightsideOf, Second))
        graph.add((Fourth, RightsideOf, Middle))
        graph.add((Fifth, RightsideOf, Fourth))
        graph.add((Second, Nextto, First))
        graph.add((Middle, Nextto, Second))
        graph.add((Fourth, Nextto, Middle))
        graph.add((Fifth, Nextto, Fourth))
        
        graph.add((Norwegian, live_in, First))
        # 绿房子在白房子的右边    
        graph.add((GreenHouse, RightsideOf, WhiteHouse))  
        # 摄影师养了一只蜗牛        
        graph.add((Photographer, has_pet, Snail))
        # 外交官住在黄房子里        
        graph.add((Diplomat, live_in, YellowHouse))
        # 中间那个房子的人喜欢喝牛奶   
        graph.add((person_in_middleHouse, like_drink, Milk))     
        # 喜欢喝咖啡的人住在绿房子里        
        graph.add((who_drink_Coffee, live_in, GreenHouse))
        # 挪威人住在蓝色的房子旁边   
        graph.add((Norwegian, liveNextto, BlueHouse))   
        # 小提琴家喜欢喝橘子汁
        graph.add((Violinist, like_drink, Orange_juice))
        # 养狐狸的人所住的房子与医生的房子相邻
        graph.add((who_has_Fox_House, liveNextto, whos_job_Doctor_House))
        # 养马的人所住的房子与外交官的房子相邻
        graph.add((who_has_Horse_House, liveNextto, whos_job_Diplomat_House))

#---------------------------------------
        # 绑定命名空间
        graph.bind("owl", OWL)
        graph.bind("nmPerson", namesPerson)
        graph.bind("nmHouse", namesHouse)
        graph.bind("nmDrink", namesDrink)
        graph.bind("nmPet", namesPet)
        graph.bind("nmJob", namesJob)

        graph.serialize("foaf.rdf", format="xml")
        graph.serialize("foaf.ttl", format="turtle")

        # q = "SELECT ?a ?b WHERE {?a nmPerson:is ?b}"
        q = """
        SELECT ?a
        WHERE {
            ?a nmPerson:liveNextto nmHouse:whos_job_Doctor_House.
        }
        """
        print(list(graph.query(q)))


if __name__ == "__main__":
    RDF.test()