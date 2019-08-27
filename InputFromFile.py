from typing import Any, Union

from owlready2 import Not

import IncreasedOntology
import ReasoningOnScenarios
from OntologyManager import *

'''
Il seguente metodo prendendo in input un oggetto di tipo OntologyManager
ha il compito di costruire l'ontologia leggendo i dati forniti dal file
"OntologyInput"
'''


def build_ontology(onto_manager: OntologyManager):
    file_object = open("OntologyInput", "r")
    for line in file_object:
        if line[:-1] == "Classes:":
            line = file_object.readline().rstrip("\n")
            class_names_list = line.split()
            for class_name in class_names_list:
                if class_name.startswith("Not"):
                    class_name = class_name.replace("Not", "", 1).replace("(", "").replace(")", "")
                    onto_manager.create_class(class_name)
                    test = onto_manager.create_class("Not("+class_name+")")
                    test.equivalent_to = [
                        onto_manager.create_complementary_class(onto_manager.get_class(class_name))]
                else:
                    onto_manager.create_class(class_name)
        if line[:-1] == "Set_as_sub_class:":
            line = file_object.readline().rstrip("\n")
            sub_class_list = line.split()
            for classes_couple in sub_class_list:
                split_classes_couple = classes_couple.split(",")
                sub_class = onto_manager.get_class(split_classes_couple[0])
                super_class = onto_manager.get_class(split_classes_couple[1])
                onto_manager.add_sub_class(sub_class, super_class)
        if line[:-1] == "Add_members_to_class:":
            line = file_object.readline().rstrip("\n")
            list_couple_member_classes = line.split(" | ")
            for couple_member_classes in list_couple_member_classes:
                couple_splitted = couple_member_classes.split(";")
                member_name = couple_splitted[0]
                classes = couple_splitted[1].split(",")
                member_identifier = onto_manager.add_member_to_class(member_name,
                                                                     onto_manager.get_class(classes[0]), False)
                i = 1
                while i < len(classes):
                    onto_manager.add_member_to_multiple_classes(member_identifier,
                                                                [onto_manager.get_class(classes[i])], False)
                    i += 1
        if line[:-1] == "Set_typical_facts:":
            fact_list: list = file_object.read().splitlines()
            for fact in fact_list:
                splitted_fact = fact.split(",")
                splitted_fact[0] = splitted_fact[0].replace("Typical", "", 1).replace("(", "").replace(")", "")

                # Crea la classe complementare negata
                if splitted_fact[1].startswith("Not"):
                    splitted_fact[1] = splitted_fact[1].replace("Not", "", 1).replace("(", "").replace(")", "")
                    splitted_fact_1_identifier = onto_manager.create_class("Not(" + splitted_fact[1] + ")")
                    splitted_fact_1_identifier.equivalent_to = [
                        onto_manager.create_complementary_class(onto_manager.get_class(splitted_fact[1]))]

                    # Controllo se c'è la probabilità o no
                    if len(splitted_fact) > 2:
                        onto_manager.add_typical_fact(onto_manager.get_class(splitted_fact[0]),
                                                      onto_manager.get_class("Not(" + splitted_fact[1] + ")"),
                                                      float(splitted_fact[2]))
                    else:
                        onto_manager.add_typical_fact(onto_manager.get_class(splitted_fact[0]),
                                                      onto_manager.get_class("Not(" + splitted_fact[1] + ")"))
                else:
                    if len(splitted_fact) > 2:
                        onto_manager.add_typical_fact(onto_manager.get_class(splitted_fact[0]),
                                                      onto_manager.get_class(splitted_fact[1]),
                                                      float(splitted_fact[2]))
                    else:
                        onto_manager.add_typical_fact(onto_manager.get_class(splitted_fact[0]),
                                                      onto_manager.get_class(splitted_fact[1]))
    file_object.close()
