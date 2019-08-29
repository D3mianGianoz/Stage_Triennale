import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""
Classe che rappresenta i risultati dell'interrogazione dell'ontologia
Generando anche un grafico interattivo con l'utilizzo di plotly
"""


class QueryResult:

    def __init__(self, list_of_logical_consequent_scenarios=None, probability: float = None):
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
        wanna_store = input()
        if wanna_store.upper() == "Y":
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

    def create_and_show_plot(self, patient_symptoms: str):
        i: int = 1
        l: list = list()
        class_id_acc: str = ""
        scatter_x = []

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        for scen in self.list_of_logical_consequent_scenarios:
            # Non ho gestito lo scenario vuoto
            for tm in scen.list_of_typical_members:
                class_id_acc += tm.t_class_identifier.name + "; "
            l.append(go.Bar(
                x=[i],
                y=[scen.probability * 100],
                name="Hypotesis " + str(i),
                text=class_id_acc,
                textposition="auto"
            ))
            l[i-1].marker.line.width = 2
            l[i-1].marker.line.color = "black"
            scatter_x.append(i)
            i += 1
            class_id_acc = ""

        fig.add_traces(l)

        trace2 = go.Scatter(
            x=scatter_x,
            y=[1000, 6000, 3000, 4000, 20000, 5000, 900, 2000, 9000, 8000],
            name="Cost of",
        )

        fig.add_trace(trace2, secondary_y=True)

        # Added titles and fonts
        fig.update_layout(
            title=go.layout.Title(
                text="Result of Computation on Symptoms: " + patient_symptoms,
                xref="paper",
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text="Set of Diagnosis",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                    )
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text="Probability",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                    )
                )
            ),
            yaxis2=dict(
                title="Euro €",
                titlefont=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            ),
            hovermode="x"
        )
        fig.show()
        #fig.write_html("first_plot.html")
