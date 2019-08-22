from OntologyManager import *
from QueryResult import *
import InputFromFile

'''
Questo modulo è composto da una serie di metodi che permettono di ragionare sugli scenari generati verificando se la 
query in input segue logicamente dalla base di conoscenza con l'aggiunta dello scenario corrente.
'''


def __translate_scenario(scenario, ontology_manager):
    for tm in scenario.list_of_typical_members:
        ontology_manager.set_as_typical_member(
            tm.member_name, tm.t_class_identifier, ontology_manager.onto[tm.t_class_identifier.name + "1"])


def __query_hermit(ontology_manager):
    return ontology_manager.consistency()


def is_logical_consequence(ontology_manager, lower_probability_bound=0, higher_probability_bound=1):
    query_result = QueryResult()
    total_probability = 0
    if lower_probability_bound != 0 or higher_probability_bound != 1:
        filtered_scenarios = [scenario for scenario in ontology_manager.scenarios_list
                              if lower_probability_bound <= scenario.probability <= higher_probability_bound]
    else:
        filtered_scenarios = ontology_manager.scenarios_list
    for scenario in filtered_scenarios:
        ontology_manager_support = OntologyManager("http://test.org/onto.owl")
        InputFromFile.build_ontology(ontology_manager_support)
        print("ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY")
        print("=================================")
        ontology_manager_support.show_members_in_classes()
        ontology_manager_support.show_classes_iri()
        print("=================================")
        print("FINE ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY")
        print("\n")
        print("LETTURA SINTOMI")
        print("=================================")
        __read_symptoms(ontology_manager_support)
        print("=================================")
        print("LETTURA SINTOMI TERMINATA")
        print("\n")
        print("TRADUCENDO LO SCENARIO: ")
        print("=================================")
        OntologyManager.show_a_specific_scenario(scenario)
        __translate_scenario(scenario, ontology_manager_support)
        print("=================================")
        print("FINE TRADUZIONE SCENARIO")
        print("\n")
        print("ONTOLOGIA CON SCENARIO E SINTOMI")
        print("=================================")
        ontology_manager_support.show_classes_iri()
        ontology_manager_support.show_members_in_classes()
        print("=================================")
        print("FINE ONTOLOGIA CON SCENARIO E SINTOMI")
        print("\n")
        if __query_hermit(ontology_manager_support) != "The ontology is consistent":
            print("=====================")
            print("Il fatto non segue logicamente nel seguente scenario: ")
            OntologyManager.show_a_specific_scenario(scenario)
            print("=====================")
        else:
            print("=====================")
            print("Il fatto segue logicamente nel seguente scenario: ")
            OntologyManager.show_a_specific_scenario(scenario)
            print("=====================")
            query_result.list_of_logical_consequent_scenarios.append(scenario)
            total_probability = total_probability + scenario.probability
        # ontology_manager_support = None
    query_result.probability = total_probability
    return query_result


def __read_query(ontology_manager):
    file_object = open("QueryInput", "r")
    line = file_object.readline().rstrip("\n")
    couple_member_class = line.split(";")
    test: bool = couple_member_class[1].startswith("Not")
    couple_member_class[1] = couple_member_class[1].replace("Not", "", 1).replace("(", "").replace(")", "")
    class_c = ontology_manager.create_class(couple_member_class[1])
    not_class_c = ontology_manager.create_class("Not(" + couple_member_class[1] + ")")
    class_c.equivalent_to = [Not(not_class_c)]
    if test:
        print("Query aggiunta: " + couple_member_class[0] + " " + ontology_manager.get_class(couple_member_class[1]).name)
        ontology_manager.add_member_to_class(couple_member_class[0], class_c, False)
    else:
        print("Query aggiunta: " + couple_member_class[0] + " " + ontology_manager.get_class("Not(" + couple_member_class[1] + ")").name)
        ontology_manager.add_member_to_class(couple_member_class[0], not_class_c, False)
    file_object.close()


def __read_symptoms(ontology_manager):
    file_object = open("PatientSetOfSymptoms.txt", "r")
    line = file_object.readline().rstrip("\n")
    list_couple_patient_class = line.split(" | ")
    for couple in list_couple_patient_class:
        couple_member_class = couple.split(";")
        test: bool = couple_member_class[1].startswith("Not")
        couple_member_class[1] = couple_member_class[1].replace("Not", "", 1).replace("(", "").replace(")", "")
        class_c = ontology_manager.create_class(couple_member_class[1])
        not_class_c = ontology_manager.create_class("Not(" + couple_member_class[1] + ")")
        class_c.equivalent_to = [Not(not_class_c)]
        if not test:
            print("Sintomo aggiunto: " + couple_member_class[0] + " " + class_c.name)
            ontology_manager.add_member_to_class(couple_member_class[0], class_c, True)
        else:
            print("Sintomo aggiunto: " + couple_member_class[0] + " " + not_class_c.name)
            ontology_manager.add_member_to_class(couple_member_class[0], not_class_c, True)
    file_object.close()

