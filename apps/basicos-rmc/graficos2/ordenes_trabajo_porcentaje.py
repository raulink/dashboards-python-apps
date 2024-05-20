import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_table

# Cargar los datos desde el archivo Excel
df = pd.read_excel('costo16horas.xlsx', sheet_name="cálculo mantto tipo ot's", usecols='B:E', skiprows=4, nrows=12, names=['Línea', 'Suma de Mantenimientos preventivos', 'Suma de Mantenimientos correctivos', 'Suma de Total Mantenimientos'])

# Convertir las columnas numéricas a tipo numérico
numeric_columns = ['Suma de Mantenimientos preventivos', 'Suma de Mantenimientos correctivos', 'Suma de Total Mantenimientos']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Calcular los porcentajes de mantenimiento preventivo y correctivo
total_mantenimientos = df['Suma de Total Mantenimientos'].sum()
porcentaje_preventivo = (df['Suma de Mantenimientos preventivos'].sum() / total_mantenimientos) * 100
porcentaje_correctivo = (df['Suma de Mantenimientos correctivos'].sum() / total_mantenimientos) * 100

# Crear el gráfico de barras apiladas horizontal
fig = go.Figure()

fig.add_trace(go.Bar(
    y=df['Línea'],
    x=df['Suma de Mantenimientos preventivos'],
    name='Mantenimientos Preventivos',
    orientation='h'
))

fig.add_trace(go.Bar(
    y=df['Línea'],
    x=df['Suma de Mantenimientos correctivos'],
    name='Mantenimientos Correctivos',
    orientation='h'
))

# Configuración del diseño del gráfico
fig.update_layout(
    barmode='stack',
    title='Cantidad de ordenes de trabajo de mantenimiento correctivos y preventivos en unidades',
    legend_title='Tipo de Mantenimiento',
)

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div(children=[
    html.Div(style={'width': '100%', 'margin-top': '20px', 'text-align': 'center'}, children=[
        html.H4(f'Porcentaje de Mantenimiento Preventivo: {porcentaje_preventivo:.2f}%'),
        html.H4(f'Porcentaje de Mantenimiento Correctivo: {porcentaje_correctivo:.2f}%')
    ]),

    html.Div(style={'width': '100%'}, children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
    ]),
    
    html.P(children='''La cantidad de órdenes de trabajo de mantenimientos correctivos y preventivos tiene como fuente 
                       el software de mantenimiento de la EETC MT, considera las cantidades de órdenes de trabajo de 
                       mantenimiento correctivo y preventivo por cada línea de transporte por cable.'''),
    
    html.Div(style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'margin-top': '10px'}, children=[
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
