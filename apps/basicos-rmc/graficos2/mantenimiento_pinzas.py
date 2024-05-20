import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
import dash_table

# Cargar los datos desde el archivo Excel
df = pd.read_excel("costo16horas.xlsx", sheet_name="CUMPLIMIENTO ESTACIONES", usecols="A:T", skiprows=0)

# Agrupar por semana y calcular la sumatoria de "Pinzas" y los máximos de "Ciclo de Pinzas"
df_agrupado = df.groupby("Semana").agg({'Pinzas': 'sum', 'Ciclo de Pinzas': 'max', 'Cambio de mordazas': 'sum', 'Ciclo de Pinzas': 'max'}).reset_index()

# Calcular la suma total de la columna "Pinzas" y la columna "Cambio de mordazas"
suma_pinzas_total = df_agrupado["Pinzas"].sum()
suma_cambio_mordazas_total = df_agrupado["Cambio de mordazas"].sum()

# Crear la figura
fig = go.Figure()

# Añadir las columnas
fig.add_trace(go.Bar(
    x=df_agrupado["Semana"],
    y=df_agrupado["Pinzas"],
    name='Suma de Pinzas',
    hovertemplate="<b>Semana %{x}</b><br><b>Suma de Pinzas: %{y}</b>",
))

fig.add_trace(go.Bar(
    x=df_agrupado["Semana"],
    y=df_agrupado["Ciclo de Pinzas"],
    name='Máximo Ciclo de Pinzas',
    hovertemplate="<b>Semana %{x}</b><br><b>Máximo Ciclo de Pinzas: %{y}</b>",
))

# Configurar el layout de la figura
fig.update_layout(
    barmode='group',  # Agrupa las barras
    title="Cantidad de Pinzas sometidas a Mantenimiento de 50000 ciclos en unidades2023",
    xaxis_title="Semana",
    #yaxis_title="Valor",
    legend_title="Tipo"
)

# Crear la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Mantenimiento de Pinzas"),
    html.Div([
        html.H3(f"Total Mantenimiento de Pinzas en el periodo: {suma_pinzas_total}"),
        html.H3(f"Total Cambio de Mordazas: {suma_cambio_mordazas_total}")
    ], style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
    html.Div([
        html.P("Las pinzas son sometidas a un despiece completo cada 50,000 ciclos de operación, siendo sometidas a limpieza, inspección visual, ensayos no destructivos y lubricación, las pinzas son sometidas a este mantenimiento una vez en la gestión pudiendo extenderse a la siguiente o reprogramarse en función del uso de cabinas que afecte el ciclaje. Para la gestión 2023 las frecuencias de mantenimiento de pinzas y ciclo correspondiente por línea son:"),
        dash_table.DataTable(
            columns=[
                {"name": "Linea", "id": "Linea"},
                {"name": "Frecuencia", "id": "Frecuencia"},
                {"name": "Ciclo", "id": "Ciclo"}
            ],
            data=[
                {"Linea": "Roja", "Frecuencia": "1 año", "Ciclo": "14"},
                {"Linea": "Amarilla", "Frecuencia": "1 año", "Ciclo": "14"},
                {"Linea": "Verde", "Frecuencia": "1 año", "Ciclo": "13/14"},
                {"Linea": "Azul", "Frecuencia": "1 año", "Ciclo": "8"},
                {"Linea": "Naranja", "Frecuencia": "1 año", "Ciclo": "8"},
                {"Linea": "Blanca", "Frecuencia": "1 año 5 meses", "Ciclo": "7"},
                {"Linea": "Celeste", "Frecuencia": "1 año 2 meses", "Ciclo": "6"},
                {"Linea": "Morada", "Frecuencia": "1 año", "Ciclo": "5/6"},
                {"Linea": "Cafe", "Frecuencia": "9 meses", "Ciclo": "6"},
                {"Linea": "Plateada", "Frecuencia": "1 año", "Ciclo": "4/5"}
            ],
            style_table={'overflowX': 'auto', 'width': 'fit-content', 'margin': '0 auto'},  # Ajustar tabla y centrar
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        )
    ], style={'margin-top': '20px'}),
    html.H2("TABLA DE CUMPLIMIENTO ESTACIONES"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_agrupado.columns],
        data=df_agrupado.to_dict('records'),
        style_table={'overflowX': 'auto', 'width': 'fit-content', 'margin': '0 auto'},  # Ajustar tabla y centrar
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
    )
])

# Ejecutar el servidor de Dash solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)
