from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='grafico-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='slider-anio'
    )
])


@callback(
    Output('grafico-slider', 'figure'),
    Input('slider-anio', 'value'))
def update_figure(valor):
    filtered_df = df[df.year == valor]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    #fig.update_layout(transition_duration=500)  #Duracion de la transicion

    return fig


if __name__ == '__main__':
    app.run(debug=True)
