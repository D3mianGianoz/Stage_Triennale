# Esistono principalmente due modi per rappresentare le figure:
# usando i dict di python 
import plotly.io as pio

fig_dict = {
    "data": [{"type": "bar",
              "x": [1, 2, 3],
              "y": [1, 3, 2]}],
    "layout": {"title": {"text": "A Bar Chart"}}
}
pio.show(fig)

# usando la gerarichia delle classi chiamata "graph objects". 
import plotly.graph_objects as go
fig_graph = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
    layout=go.Layout(
        title=go.layout.Title(text="A Bar Chart")
    )
)
fig.show()

# Si possono salvare i diagrammi in singoli file HTML:
fig.write_html('first_figure.html', auto_open=True)

# Esiste anche la possibilità di creare sottografici
from plotly.subplots import make_subplots

# Creiamo un grafico da una riga e due colonne:
fig = make_subplots(rows=1, cols=2)

# Aggiungiamo un grafico a dispersione e un istogramma:
fig.add_scatter(y=[4, 2, 1], mode="lines", row=1, col=1)
fig.add_bar(y=[2, 1, 3], row=1, col=2)
fig.show()
