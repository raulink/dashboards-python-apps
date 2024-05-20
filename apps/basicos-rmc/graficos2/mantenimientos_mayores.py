import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_table

# Cargar los datos desde el archivo Excel
df = pd.read_excel('costo16horas.xlsx', sheet_name='cálculo manttos mayores', usecols='B:C', skiprows=2, nrows=16, names=['Mantenimiento anual', 'Suma de Cantidad'])

# Crear el gráfico de barras horizontal
fig = go.Figure([go.Bar(y=df['Mantenimiento anual'], x=df['Suma de Cantidad'], orientation='h')])

# Establecer el título y etiquetas de los ejes
fig.update_layout(
    title='Cantidad de Mantenimientos Mayores en unidades 2023',
    xaxis_title='Suma de Cantidad',
    yaxis_title='Mantenimiento'
)

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div(style={'display': 'flex'}, children=[
    html.Div(style={'flex': '75%'}, children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
    html.P(children='''La cantidad de mantenimientos mayores realizados en la gestión toma en cuenta los mantenimientos 
                       de mayor alcance en complejidad, logística y costo. Estos son realizados en las diferentes líneas 
                       conforme a la planificación de las Jefaturas de Mantenimiento de Línea.'''),
    ]),
    html.Div(style={'flex': '25%'}, children=[
        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '5px'
            },
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold'
            }
        ),
    ])
])

# Ejecutar el servidor de Dash solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)
