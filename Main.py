import IncreasedOntology
from ReasoningOnScenarios import is_logical_consequence, __read_symptoms
import sys
from InputFromFile import build_ontology
from OntologyManager import OntologyManager
from time import time

'''
Modulo principale da cui parte lo strumento
'''


def entailed_knowledge():
    print("========== {:s} ==========".format("Adding a set of Symptoms to the KB"))
    patient_sym = __read_symptoms(ontology_manager, result=True)
    print("========== {:s} ==========".format("Checking consistency"))
    result = ontology_manager.consistency()
    print("========== {:s} ==========".format(result))
    if result.__eq__("The ontology is inconsistent"):
        print("+++++++++++++++ {:s} +++++++++++++++\n\n\n".format("The set of Symptoms is NOT consistent with the KB"))
        print("---- {:s} -----".format("Ending"))
        sys.exit(5)
    print("========== {:s} ==========\n".format("The set of Symptoms is consistent with the KB"))
    return patient_sym


if __name__ == '__main__':

    t = time()

    ontology_manager = OntologyManager()
    build_ontology(ontology_manager)
    sym: str = entailed_knowledge()
    IncreasedOntology.compute_probability_for_typical_members(ontology_manager)
    IncreasedOntology.set_probability_for_each_scenario(
        IncreasedOntology.generate_scenarios(ontology_manager),
        ontology_manager)
    ontology_manager.show_scenarios()
    query_result = is_logical_consequence(ontology_manager)
    query_result.show_query_result()
    query_result.create_and_show_plot(sym)

    t = time() - t
    print("\nFine simulazione, tempo totale: ", float(t), " s")

    # query_result.save_query_result()

