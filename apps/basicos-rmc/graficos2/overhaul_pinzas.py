import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Cargar los datos desde el archivo Excel
df = pd.read_excel('costo16horas.xlsx', sheet_name='oh pinz', usecols='A:U', skiprows=3, nrows=12)

# Reemplazar los valores '#¡DIV/0!' con NaN y luego con 0
df.replace('#¡DIV/0!', pd.NA, inplace=True)
df.fillna(0, inplace=True)

# Convertir los datos a numéricos cuando sea posible
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Verificar los nombres de las columnas
print(df.columns)

# Crear el gráfico de barras apiladas horizontalmente
fig = go.Figure()

# Añadir una barra para cada conjunto de datos
for col in df.columns[2:]:
    fig.add_trace(go.Bar(
        y=df[df.columns[0]],  # Primer columna como 'Linea Sección'
        x=df[col],
        name=col,
        orientation='h'  # Orientación horizontal
    ))

# Establecer el layout del gráfico e invertir el eje y
fig.update_layout(
    barmode='stack',
    title='Duraciones Promedio de Mantenimiento por Línea y Sección',
    xaxis_title='Duración (minutos)',
    yaxis_title='Línea Sección',
    legend_title='Tipo de Duración/Espera',
    yaxis=dict(
        autorange='reversed'  # Invertir el eje y
    )
)

# Crear la aplicación Dash
app = Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Mantenimientos'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# Ejecutar el servidor de Dash solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)
