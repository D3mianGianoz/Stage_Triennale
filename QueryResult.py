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

    def create_and_show_plot(self, patient_symptoms: str, disease_cost: dict):
        i: int = 1
        l: list = list()
        cost = 0
        class_id_acc: str = ""
        scatter_x = []
        scatter_y = []
        tot_prb_for = "{0:.2f}".format(self.probability * 100) + "%"

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        for scen in self.list_of_logical_consequent_scenarios:
            # Non ho gestito lo scenario vuoto
            for tm in scen.list_of_typical_members:
                class_id_acc += tm.t_class_identifier.name + "; "
                cost += disease_cost.get(tm.t_class_identifier.name)
            l.append(go.Bar(
                x=[i],
                y=[scen.probability * 100],
                name="Hypothesis " + str(i),
                text=class_id_acc,
                textposition="auto"
            ))
            l[i-1].marker.line.width = 2
            l[i-1].marker.line.color = "black"
            scatter_x.append(i)
            scatter_y.append(cost)
            i += 1
            class_id_acc = ""
            cost = 0

        fig.add_traces(l)

        trace2 = go.Scatter(
            x=scatter_x,
            y=scatter_y,
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
                    text="Probability: Max " + tot_prb_for,
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
        return fig

    def save_query_result(self, fig: go.Figure, name=None):
        print("Vuoi salvare i risultati in un file ? Y/N")
        wanna_store = input()
        if wanna_store.upper() == "Y":
            if name is not None:
                fig.write_html(name + ".html")
            else:
                fig.write_html("plot.html")
            print("Operazione eseguita con successo, fine esecuzione")
        else:
            print("Risultati NON salvati, fine esecuzione")

        # TODO  se si usa la  guida https://github.com/plotly/orca  si puo usare: fig.write_image("plotDepression.pdf")
