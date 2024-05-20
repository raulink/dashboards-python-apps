import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Cargar el archivo .xlsx
excel_file = 'archivo.xlsx'
sheets = pd.ExcelFile(excel_file).sheet_names

def load_data(sheet_name):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    # Seleccionar los datos desde la fila G54 hasta la fila AH56 para el gráfico
    data_grafico = df.iloc[54:55, 7:34].T
    # Cambiar los índices del DataFrame para que solo muestren el año y empiecen en 2024
    data_grafico.index = pd.date_range(start='2024-01-01', periods=len(data_grafico), freq='Y').year
    # Seleccionar los datos para la tabla, incluyendo la primera fila como encabezado
    data_tabla = df.iloc[33:56, 6:35]
    data_tabla.columns = data_tabla.iloc[0]  # Establecer la primera fila como encabezado de columna
    data_tabla = data_tabla.drop(data_tabla.index[0])  # Eliminar la primera fila de datos
    # Redondear los valores numéricos a dos decimales
    data_tabla = data_tabla.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
    return data_grafico, data_tabla

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Gráfico de Líneas'),
    dcc.Dropdown(
        id='sheet-selector',
        options=[{'label': sheet, 'value': sheet} for sheet in sheets],
        value=sheets[0]  # Seleccionar la primera hoja por defecto
    ),
    dcc.Graph(
        id='line-chart',
        style={'width': '100%'}
    ),
    html.Hr(),  # Línea horizontal para separar el gráfico de la tabla
    html.H3(children='Tabla de datos'),
    html.Div(
        id='data-table',
        style={'height': '400px', 'overflowY': 'scroll'}
    )
], style={'width': '100%', 'display': 'inline-block'})

# Callback para actualizar el gráfico y la tabla cuando se selecciona una hoja diferente
@app.callback(
    [Output('line-chart', 'figure'), Output('data-table', 'children')],
    [Input('sheet-selector', 'value')]
)
def update_output(sheet_name):
    data_grafico, data_tabla = load_data(sheet_name)
    
    # Crear un gráfico de líneas con Plotly
    fig = go.Figure()
    for column in data_grafico.columns:
        fig.add_trace(go.Scatter(x=data_grafico.index, y=data_grafico[column], mode='markers+lines', line_shape='spline', name=column))
    
    fig.update_layout(title='Datos de línea',
                      xaxis_title='Año',
                      yaxis_title='Valor',
                      legend_title='Sistema')

    table = html.Table([
        # Encabezados de columna
        html.Tr([html.Th(col, style={'border': '1px solid black', 'padding': '5px'}) for col in data_tabla.columns]),
        # Contenido de la tabla
        html.Tbody([
            html.Tr([
                html.Td(data_tabla.iloc[i, j], style={'border': '1px solid black', 'padding': '5px'}) for j in range(len(data_tabla.columns))
            ]) for i in range(len(data_tabla))
        ])
    ], style={'width': '100%', 'border-collapse': 'collapse'})

    return fig, table

# Ejecutar el servidor de Dash solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)
