import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output,callback
import dash_table

# Ruta al archivo de Excel en la misma carpeta del proyecto
excel_file = 'Ingresos 2017-20241.xlsx'

# Leer datos de la hoja "pasajeros" de Excel
df = pd.read_excel(excel_file, sheet_name='pasajeros', skiprows=0, usecols='A:L', nrows=13)

# Obtener la lista de líneas
lines = df[df.columns[0]].tolist()

# Define el layout de la aplicación
layout = html.Div([
    html.H1('Histograma de Pasajeros por Línea'),

    html.Div([
        # Gráfico de histograma
        html.Div([
            dcc.Graph(id='histograma-pasajeros'),
        ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

        # Checklist para seleccionar líneas
        html.Div([
            html.Label('Selecciona Líneas:'),
            dcc.Checklist(
                id='lineas-checklist',
                options=[{'label': line, 'value': line} for line in lines],
                value=[line for line in lines if line != 'TOTAL GENERAL'],  # Selecciona todas las líneas excepto 'TOTAL GENERAL'
                inline=False  # Mostrar las líneas en una columna
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px', 'textAlign': 'left'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

    # Tabla de datos
    dash_table.DataTable(
        id='tabla-pasajeros',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'scroll'},  # Permitir desplazamiento horizontal
        style_cell={'textAlign': 'center'},  # Alinear texto al centro
        style_header={'fontWeight': 'bold'},  # Estilo del encabezado
    )
], style={'textAlign': 'center'})

# Callback para actualizar el histograma
@callback(
    Output('histograma-pasajeros', 'figure'),
    [Input('lineas-checklist', 'value')]
)
def update_histogram(selected_lines):
    # Filtrar el DataFrame según las líneas seleccionadas
    filtered_df = df[df[df.columns[0]].isin(selected_lines)]
    # Crear el gráfico de barras
    fig = px.bar(
        filtered_df, x=filtered_df.columns[0], y=df.columns[1:],  # Fijar los años en y
        labels={'value': 'Pasajeros', 'variable': 'Año'},
        title='Histograma de Pasajeros por Línea'
    )
    fig.update_layout(height=510)  # Ajustar el tamaño vertical del gráfico
    return fig
