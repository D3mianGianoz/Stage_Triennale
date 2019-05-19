from OntologyManager import *
import InputFromFile
import IncreasedOntology
import ReasoningOnScenarios

if __name__ == '__main__':
    # Inizio simulazione
    t = time.time()

    ontology_manager = OntologyManager()
    InputFromFile.build_ontology(ontology_manager)
    InputFromFile.some_method(ontology_manager)
    IncreasedOntology.compute_probability_for_typical_members(ontology_manager)
    IncreasedOntology.set_probability_for_each_scenario(
        IncreasedOntology.generate_scenarios(ontology_manager),
        ontology_manager)
    ontology_manager.show_scenarios()
    query_result = ReasoningOnScenarios.is_logical_consequence(ontology_manager)
    query_result.show_query_result()

    # Fine simulazione
    t = time.time() - t
    print("\nFine simulazione, tempo totale: ", float(t), " s")

    # Rimozione DB
    ontology_manager.destroy_backend_db()