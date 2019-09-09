from OntologyManager import Not
from QueryResult import QueryResult

'''
Questo modulo è composto da una serie di metodi che permettono di ragionare sugli scenari generati verificando se il/i 
sintomo/i in input segue/seguono logicamente dalla base di conoscenza con l'aggiunta dello scenario corrente.
'''

'''
TODO
lo sviluppo di un meccanismo di selezione degli scenari
su cui effettuare la fase di interrogazione; infatti attualmente vengono considera-
ti tutti gli scenari possibili tuttavia,in generale, solo alcuni possono concretamente
realizzarsi, per tanto risulta essere superfluo ragionare su questi scenari impossibili.
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
        ontology_manager.create_new_world()
        print("ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY")
        print("=================================")
        ontology_manager.show_members_in_classes()
        ontology_manager.show_classes_iri()
        print("=================================")
        print("FINE ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY")
        print("\n")
        print("LETTURA SINTOMI")
        print("=================================")
        __read_symptoms(ontology_manager, reasoning=True)
        print("=================================")
        print("LETTURA SINTOMI TERMINATA")
        print("\n")
        print("TRADUCENDO LO SCENARIO: ")
        print("=================================")
        ontology_manager.show_a_specific_scenario(scenario)
        __translate_scenario(scenario, ontology_manager)
        print("=================================")
        print("FINE TRADUZIONE SCENARIO")
        print("\n")
        print("ONTOLOGIA CON SCENARIO E SINTOMI")
        print("=================================")
        ontology_manager.show_classes_iri()
        ontology_manager.show_members_in_classes()
        print("=================================")
        print("FINE ONTOLOGIA CON SCENARIO E SINTOMI")
        print("\n")
        if __query_hermit(ontology_manager) == "The ontology is consistent":
            print("=====================")
            print("Il fatto non segue logicamente nel seguente scenario: ")
            ontology_manager.show_a_specific_scenario(scenario)
            print("=====================")
        else:
            print("=====================")
            print("Il fatto segue logicamente nel seguente scenario: ")
            ontology_manager.show_a_specific_scenario(scenario)
            print("=====================")
            query_result.list_of_logical_consequent_scenarios.append(scenario)
            total_probability = total_probability + scenario.probability
    query_result.probability = total_probability
    return query_result


def __read_symptoms(ontology_manager, result: bool = False, reasoning: bool = False):
    file_object = open("PatientSetOfSymptoms.txt", "r")
    line = file_object.readline().rstrip("\n")
    list_couple_patient_class = line.split(" | ")
    symptoms_for_plot: str = ""
    for couple in list_couple_patient_class:
        patient: str
        couple_member_class = couple.split(";")
        test: bool = couple_member_class[1].startswith("Not")
        couple_member_class[1] = couple_member_class[1].replace("Not", "", 1).replace("(", "").replace(")", "")
        class_c = ontology_manager.create_class(couple_member_class[1])
        not_class_c = ontology_manager.create_class("Not(" + couple_member_class[1] + ")")
        class_c.equivalent_to = [Not(not_class_c)]
        print_msg: str = "Sintomo aggiunto: " + couple_member_class[0]
        if reasoning: test = not test
        if not test:
            patient = class_c.name
            ontology_manager.add_member_to_class(couple_member_class[0], class_c, symp=True)
        else:
            patient = not_class_c.name
            ontology_manager.add_member_to_class(couple_member_class[0], not_class_c, symp=True)
        print(print_msg + " " + patient)
        symptoms_for_plot += "#" + patient + " "
    file_object.close()

    if result: return symptoms_for_plot
