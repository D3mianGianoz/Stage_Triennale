from owlready2 import *
import owlready2
import types
from TypicalFact import *
from AboxMember import *
 # owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jdk-11.0.2\\bin\\java.exe"

'''
Classe che rappresenta l'ontologia, fornisce vari metodi per gestirla.
'''

# Serve per l'ontologia di supporto

class OntologyManager:
    def __init__(self, iri="http://www.example.org/onto.owl"):
        self.typical_facts_list = list()
        self.a_box_members_list = list()
        self.typical_members_list = list()
        self.scenarios_list = list()
        self.my_world = World()
        if iri != "http://www.example.org/onto.owl":
            self.onto = self.my_world.get_ontology(iri)
        else:
            self.onto = self.my_world.get_ontology("http://www.example.org/onto.owl")

    def create_complementary_class(self, class_identifier):
        with self.onto:
            complementary_class = Not(class_identifier)
        return complementary_class

    def create_class(self, class_name):
        with self.onto:
            new_class = types.new_class(class_name, (Thing,))
        return new_class

    def create_property(self, property_name):
        with self.onto:
            new_property = types.new_class(property_name, (ObjectProperty,))
        return new_property

    @staticmethod
    def destroy_class(class_identifier):
        destroy_entity(class_identifier)

    def add_sub_class(self, sub_class_identifier, super_class_identifier):
        with self.onto:
            sub_class_identifier.is_a.append(super_class_identifier)

    # & operatore logico di owlready di intersezione.
    # r1 proprietà di owlready
    # only perogni
    # some invece significa esiste

    def add_typical_fact(self, t_class_identifier, class_identifier, probability="No probability"):
        with self.onto:
            t_class_identifier_1 = self.create_class(t_class_identifier.name + "1")
            t_class_intersection = self.create_class("Intersection"+t_class_identifier.name+t_class_identifier_1.name)
            t_class_intersection.equivalent_to = [t_class_identifier & t_class_identifier_1]
            self.add_sub_class(t_class_intersection, class_identifier)

            r1 = self.create_property("r1")
            t_class_identifier_1.is_a.append(r1.only(Not(t_class_identifier) & t_class_identifier_1))

            not_t_class_identifier_1 = self.create_class("Not" + t_class_identifier_1.name)
            not_t_class_identifier_1.is_a.append(r1.some(t_class_identifier & t_class_identifier_1))

            self.typical_facts_list.append(TypicalFact(t_class_identifier, class_identifier, probability))

    def show_scenarios(self):
        num_scenario = 1
        for s in self.scenarios_list:
            print("INIZIO SCENARIO " + str(num_scenario))
            record = ""
            if len(s.list_of_typical_members) == 0:
                print("Scenario vuoto" + "\n" + "Probabilità scenario: " + str(s.probability))
            else:
                for tm in s.list_of_typical_members:
                    record = record + "Typical(" + tm.t_class_identifier.name + ")" + "," + tm.member_name + "," + str(tm.probability) + "\n"
                record = record + "Probabilità scenario: " + str(s.probability)
                print(record)
            print("FINE SCENARIO " + str(num_scenario))
            print("\n")
            num_scenario = num_scenario + 1

    @staticmethod
    def show_a_specific_scenario(scenario):
        print("INIZIO SCENARIO")
        record = ""
        if len(scenario.list_of_typical_members) == 0:
            print("Scenario vuoto; " + str(scenario.probability))
        else:
            for tm in scenario.list_of_typical_members:
                record = record + tm.t_class_identifier.name + "," + tm.member_name + "," + str(tm.probability) + " ;"
            record = record + str(scenario.probability)
            print(record)
        print("FINE SCENARIO")

    @staticmethod
    def set_classes_as_disjoint(classes_identifier_list):
        AllDisjoint(classes_identifier_list)

    def add_member_to_class(self, member_name, class_identifier):
        self.a_box_members_list.append(AboxMember(class_identifier, member_name))
        return class_identifier(member_name)

    # C e C1
    # Interesezione serve per esplicitare il concetto della doppia appartenenza

    def set_as_typical_member(self, member_name, t_class_identifier, t_class_identifier_1):
        with self.onto:
            print("Membro tipico:")
            t_class_identifier(member_name)
            t_class_identifier_1(member_name)
            t_class_intersection = self.get_class("Intersection"+t_class_identifier.name + t_class_identifier_1.name)
            t_class_intersection(member_name)
            print(member_name + " is_a " + t_class_identifier.name)
            print(member_name + " is_a " + t_class_identifier_1.name)
            print(member_name + " is_a " + t_class_intersection.name)

    def add_member_to_multiple_classes(self, member_identifier, class_list):
        for c in class_list:
            member_identifier.is_a.append(c)
            self.a_box_members_list.append(AboxMember(c, member_identifier.name))

    def is_class_present(self, class_name):
        if self.get_class(class_name) is not None:
            return True
        return False

    def get_class(self, class_name):
        return self.onto[class_name]

    def is_consistent(self):
        return self.consistency()

    def consistency(self):
        try:
            with self.onto:
                sync_reasoner(self.my_world)
                return "The ontology is consistent"
        except OwlReadyInconsistentOntologyError:
            return "The ontology is inconsistent"

    def show_classes_iri(self):
        for c in self.my_world.classes():
            print(str(c.name) + " is_a " + str(c.is_a))

    def show_members_in_classes(self):
        for c in self.my_world.classes():
            for m in c.instances():
                print(m.name + " is_a " + c.name)
