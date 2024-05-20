import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_table

# Cargar los datos desde el archivo Excel
df_correctivos = pd.read_excel('costo16horas.xlsx', sheet_name="cálculo mantto tipo ot's", usecols='B:C', skiprows=52, nrows=29, names=['Subsistema identificado', 'Suma de Mantenimientos correctivos'])
df_preventivos = pd.read_excel('costo16horas.xlsx', sheet_name="cálculo mantto tipo ot's", usecols='F:G', skiprows=52, nrows=29, names=['Subsistema identificado', 'Suma de Mantenimientos preventivos'])

# Convertir las columnas numéricas a tipo numérico
df_correctivos['Suma de Mantenimientos correctivos'] = pd.to_numeric(df_correctivos['Suma de Mantenimientos correctivos'], errors='coerce')
df_preventivos['Suma de Mantenimientos preventivos'] = pd.to_numeric(df_preventivos['Suma de Mantenimientos preventivos'], errors='coerce')

# Calcular los totales de OT's
total_correctivos = df_correctivos['Suma de Mantenimientos correctivos'].sum()
total_preventivos = df_preventivos['Suma de Mantenimientos preventivos'].sum()

# Crear el gráfico de barras para mantenimientos correctivos
fig_correctivos = go.Figure()

fig_correctivos.add_trace(go.Bar(
    y=df_correctivos['Subsistema identificado'],
    x=df_correctivos['Suma de Mantenimientos correctivos'],
    name='Mantenimientos Correctivos',
    orientation='h'
))

# Configuración del diseño del gráfico
fig_correctivos.update_layout(
    barmode='stack',
    title='Cantidad de ordenes de trabajo de Mantenimientos Correctivos por Subsistema en unidades 2023',
    legend_title='Tipo de Mantenimiento',
)

# Crear el gráfico de barras para mantenimientos preventivos
fig_preventivos = go.Figure()

fig_preventivos.add_trace(go.Bar(
    y=df_preventivos['Subsistema identificado'],
    x=df_preventivos['Suma de Mantenimientos preventivos'],
    name='Mantenimientos Preventivos',
    orientation='h'
))

# Configuración del diseño del gráfico
fig_preventivos.update_layout(
    barmode='stack',
    title='Cantidad de ordenes de trabajo de Mantenimientos Preventivos por Subsistema en unidades 2023',
    legend_title='Tipo de Mantenimiento',
)

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div(children=[
    # Títulos con la cantidad total de OT's
    html.Div(style={'width': '100%', 'text-align': 'center', 'margin-top': '20px'}, children=[
        html.H4(f'Cantidad total de OT\'s Correctivas: {total_correctivos}'),
        html.H4(f'Cantidad total de OT\'s Preventivas: {total_preventivos}')
    ]),
    
    # Graficos
    html.Div(style={'width': '100%', 'display': 'flex', 'justify-content': 'space-around'}, children=[
        html.Div(style={'width': '48%'}, children=[
            dcc.Graph(
                id='graph-correctivos',
                figure=fig_correctivos
            ),
            html.P(children='''La cantidad de órdenes de trabajo de mantenimiento correctivo por subsistema tiene como fuente el software de mantenimiento de la EETC MT, considera las cantidades de órdenes de trabajo de mantenimiento correctivo por subsistema del STC.''')
        ]),
        html.Div(style={'width': '48%'}, children=[
            dcc.Graph(
                id='graph-preventivos',
                figure=fig_preventivos
            ),
            html.P(children='''La cantidad de órdenes de trabajo de mantenimiento preventivo por subsistema tiene como fuente el software de mantenimiento de la EETC MT, considera las cantidades de órdenes de trabajo de mantenimineto preventivo por subsistema del STC.''')
        ]),
    ]),
    
    # Tablas
    html.Div(style={'width': '100%', 'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'}, children=[
        html.Div(style={'width': '48%'}, children=[
            dash_table.DataTable(
                id='table-correctivos',
                columns=[{'name': col, 'id': col} for col in df_correctivos.columns],
                data=df_correctivos.to_dict('records'),
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
        ]),
        html.Div(style={'width': '48%'}, children=[
            dash_table.DataTable(
                id='table-preventivos',
                columns=[{'name': col, 'id': col} for col in df_preventivos.columns],
                data=df_preventivos.to_dict('records'),
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
        ]),
    ]),
])

# Ejecutar el servidor de Dash solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)
