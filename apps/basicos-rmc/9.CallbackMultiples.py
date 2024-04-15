from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd

app = Dash(__name__)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

app.layout = html.Div([
    html.Div([

        html.Div([
            #Dropdown de seleccion  de dataframe
            dcc.Dropdown(df['Indicator Name'].unique(),'Fertility rate, total (births per woman)',id='xaxis-column'),
            #Opcion de visualizacion
            dcc.RadioItems(['Linear', 'Log'],'Linear',id='xaxis-type',inline=True)], 
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            #Dropdown de seleccion  de dataframe
            dcc.Dropdown(df['Indicator Name'].unique(),'Life expectancy at birth, total (years)',id='yaxis-column'),
            #Opcion de visualizacion
            dcc.RadioItems(['Linear', 'Log'],'Linear',id='yaxis-type',inline=True)
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='grafico-cambiable'),

    dcc.Slider(df['Year'].min(),df['Year'].max(),step=None,id='slider-anio',value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
    )
])


@callback(
    Output('grafico-cambiable', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('slider-anio', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,xaxis_type, yaxis_type,year_value):
    dff = df[df['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     # Nombre del pais que se visualizara al pasar el cursor
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')  #Actualizar el layout los margenes
    #Modificar si se establece graficacion logaritmica o lineal
    fig.update_xaxes(title=xaxis_column_name,type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name,type='linear' if yaxis_type == 'Linear' else 'log')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
