# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Grafico y controles'),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='radio-item'), # Botones radio
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),  # page_size es paginacion de datos en la tabla
    dcc.Graph(figure={}, id='graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='radio-item', component_property='value')
)
def update_graph(valor):
    fig = px.histogram(df, x='continent', y=valor, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
