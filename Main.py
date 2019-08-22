import IncreasedOntology
import ReasoningOnScenarios
import sys
from InputFromFile import build_ontology
from OntologyManager import OntologyManager
from time import sleep

def entailed_knowledge():
    print("========== Adding a set of Symptoms to the KB ==========")
    ReasoningOnScenarios.__read_symptoms(ontology_manager)
    print("========== Checking consistency ==========")
    result = ontology_manager.consistency()
    sleep(1)
    print("========== {:s} ==========".format(result))
    if result.__eq__("The ontology is inconsistent"):
        print("+++++++++++++++", "The set of Symptoms is NOT consistent with the KB", "+++++++++++++++\n\n\n")
        print("---- Ending -----")
        sys.exit(5)
    print("=============================", "\nThe set of Symptoms is consistent with the KB\n", "=====================")

if __name__ == '__main__':
    ontology_manager = OntologyManager()
    build_ontology(ontology_manager)
    entailed_knowledge()
    IncreasedOntology.compute_probability_for_typical_members(ontology_manager)
    #scenariiii = IncreasedOntology.generate_scenarios(ontology_manager)

    IncreasedOntology.set_probability_for_each_scenario(
        IncreasedOntology.generate_scenarios(ontology_manager),
        ontology_manager)
    ontology_manager.show_scenarios()
    query_result = ReasoningOnScenarios.is_logical_consequence(ontology_manager)
    query_result.show_query_result()



