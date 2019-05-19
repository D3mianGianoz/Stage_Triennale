from OntologyManager import *
from QueryResult import *


'''
Questo modulo è composto da una serie di metodi che permettono di ragionare sugli scenari generati verificando se la 
query in input segue logicamente dalla base di conoscenza con l'aggiunta dello scenario corrente.
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

# 1. Viene creata una copia dell’ontologia (righe [34;36]).
# 2. Alla copia viene aggiunta la query e lo scenario corrente (righe [51;58]).
# 3. Si verifica la conseguenzialità logica del fatto F (righe [69;78]).
# 4. Si salva lo scenario appena aggiunto, se viene verificata la conseguenzialità
#    logica (riga 79), in un oggetto di tipo QueryResult.
# 5. Viene accumulata la probabilità totale dell’interrogazione data dalla somma
#    delle probabilità degli scenari salvati (riga 80).
# 6. Viene distrutta la copia dell’ontologia (riga 81).
# 7. All’uscita del ciclo viene salvata la probabilità totale accumulata nell’oggetto
#    di tipo QueryResult

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
        print("LETTURA QUERY")
        print("=================================")
        __read_query(ontology_manager)
        print("=================================")
        print("LETTURA QUERY TERMINATA")
        print("\n")
        print("TRADUCENDO LO SCENARIO: ")
        print("=================================")
        OntologyManager.show_a_specific_scenario(scenario)
        __translate_scenario(scenario, ontology_manager)
        print("=================================")
        print("FINE TRADUZIONE SCENARIO")
        print("\n")
        print("ONTOLOGIA CON SCENARIO E QUERY")
        print("=================================")
        ontology_manager.show_classes_iri()
        ontology_manager.show_members_in_classes()
        print("=================================")
        print("FINE ONTOLOGIA CON SCENARIO E QUERY")
        print("\n")
        if __query_hermit(ontology_manager) == "The ontology is consistent":
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
        ontology_manager.close_new_world()
    query_result.probability = total_probability
    return query_result


# Il risultato è che se si vuole verificare che nome_membro;nome_classe segua lo-
# gicamente dalla base di conoscenza dell’ontologia, il membro nome_membro viene
# aggiunto alla classe not_class_c
# al contrario, se si deve controllare che nome_membro;Not(nome_classe) segua logicamente
# allora l’aggiunta del membro nome_membro alla classe class_c

def __read_query(ontology_manager):
    file_object = open("QueryInput", "r")
    line = file_object.readline().rstrip("\n")
    couple_member_class = line.split(";")
    if couple_member_class[1].startswith("Not"):
        couple_member_class[1] = couple_member_class[1].replace("Not", "", 1).replace("(", "").replace(")", "")
        class_c = ontology_manager.create_class(couple_member_class[1])
        not_class_c = ontology_manager.create_class("Not(" + couple_member_class[1] + ")")
        class_c.equivalent_to = [Not(not_class_c)]
        print("Query aggiunta: " + couple_member_class[0] + " " + ontology_manager.get_class(couple_member_class[1]).name)
        ontology_manager.add_member_to_class(couple_member_class[0], class_c)
    else:
        couple_member_class[1] = couple_member_class[1].replace("Not", "", 1).replace("(", "").replace(")", "")
        class_c = ontology_manager.create_class(couple_member_class[1])
        not_class_c = ontology_manager.create_class("Not(" + couple_member_class[1] + ")")
        class_c.equivalent_to = [Not(not_class_c)]
        print("Query aggiunta: " + couple_member_class[0] + " " + ontology_manager.get_class("Not(" + couple_member_class[1] + ")").name)
        ontology_manager.add_member_to_class(couple_member_class[0], not_class_c)
    file_object.close()

