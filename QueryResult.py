"""
Classe che rappresenta i risultati dell'interrogazione dell'ontologia
"""


class QueryResult:

    def __init__(self, list_of_logical_consequent_scenarios=None, probability=None):
        if list_of_logical_consequent_scenarios is None:
            list_of_logical_consequent_scenarios = []
        if probability is None:
            probability = 2
        self.list_of_logical_consequent_scenarios = list_of_logical_consequent_scenarios
        self.probability = probability

    def show_query_result(self):
        print("RISULTATI DELL'INTERROGAZIONE: ")
        print("SCENARI IN CUI LA QUERY SEGUE LOGICAMENTE")
        num_scenario = 1
        for s in self.list_of_logical_consequent_scenarios:
            print("INIZIO SCENARIO " + str(num_scenario))
            record = ""
            if len(s.list_of_typical_members) == 0:
                print("Scenario vuoto; " + str(s.probability))
            else:
                for tm in s.list_of_typical_members:
                    record = record + tm.t_class_identifier.name + "," + tm.member_name + "," \
                             + str(tm.probability) + "; "
                record = record + "\nProbabilita complessiva dello scenario: " + str(s.probability)
                print(record)
            print("FINE SCENARIO " + str(num_scenario))
            print("\n")
            num_scenario = num_scenario + 1
        print("PROBABILITA' TOTALE: " + str(self.probability))

    def save_query_result(self):
        print("Vuoi salvare i risultati in un file ? Y/N")
        wannaStore = input()
        if wannaStore.upper() == "Y":
            f = open("myResult.txt", "w")
            f.write("Lista degli scenari:\n")
            for scenario in self.list_of_logical_consequent_scenarios:
                f.write(scenario.__str__() + "\n")
            f.write("Probabilità complessiva:\n")
            f.write(str(self.probability))
            f.flush()
            f.close()
            print("Operazione eseguita con successo, fine esecuzione")
        else:
            print("Risultati NON salvati, fine esecuzione")

