import IncreasedOntology
from ReasoningOnScenarios import is_logical_consequence
import sys
from InputFromFile import build_ontology, read_symptoms
from OntologyManager import OntologyManager
from time import time

'''
Modulo principale, rappresenta la corretta sequenza di chiamate 
che permette al tool di funzionare
'''


def entailed_knowledge():
    print("========== {:s} ==========".format("Adding a set of Symptoms to the KB"))
    patient_sym = read_symptoms(ontology_manager, result=True)
    print("========== {:s} ==========".format("Checking consistency"))
    result = ontology_manager.consistency(condition=True)
    if not result == "The ontology is consistent":
        print(result)
        print("+++++++++++++++ {:s} +++++++++++++++\n".format("The set of Symptoms is NOT consistent with the KB"))
        ontology_manager.show_classes_iri_my()
        ontology_manager.show_members_in_classes_my()
        print("---- {:s} -----".format("Ending"))
        sys.exit(5)
    print("========== {:s} ==========".format(result))
    print("========== {:s} ==========\n".format("The set of Symptoms is consistent with the KB"))
    return patient_sym


if __name__ == '__main__':

    t = time()

    ontology_manager = OntologyManager()
    build_ontology(ontology_manager)
    sym = entailed_knowledge()
    IncreasedOntology.compute_probability_for_typical_members(ontology_manager)
    IncreasedOntology.set_probability_for_each_scenario(ontology_manager)
    ontology_manager.show_scenarios()
    query_result = is_logical_consequence(ontology_manager)
    query_result.show_query_result()
    query_result.create_and_show_plot(sym, ontology_manager.cost_dict)

    t = time() - t
    print("\nFine simulazione, tempo totale: ", float(t), " s")

    OntologyManager.remove_onto_file()
    query_result.save_query_result("caso_di_studio_alt")

