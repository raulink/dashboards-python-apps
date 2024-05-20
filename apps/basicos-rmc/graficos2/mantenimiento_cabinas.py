import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
import dash_table

# Cargar los datos desde el archivo Excel
df = pd.read_excel("costo16horas.xlsx", sheet_name="CUMPLIMIENTO ESTACIONES", usecols="A:T", skiprows=0)
df_cabinas = pd.read_excel("costo16horas.xlsx", sheet_name="Cabinas", usecols="D:H", skiprows=29)

# Eliminar columnas y filas vacías en la tabla de Cabinas
df_cabinas.dropna(axis=1, how='all', inplace=True)
df_cabinas.dropna(axis=0, how='all', inplace=True)

# Agrupar por semana y calcular la sumatoria de "Pinzas" y los máximos de "Ciclo de Pinzas"
df_agrupado = df.groupby("Semana").agg({'Cabinas': 'sum', 'Periodo de Cabinas': 'sum', 'Suspensiones': 'max'}).reset_index()

# Calcular la suma total de la columna "Pinzas" y la columna "Cambio de mordazas"
suma_cabinas_total = df_agrupado["Cabinas"].sum()
suma_suspensiones = df_agrupado["Suspensiones"].sum()

# Crear la figura
fig = go.Figure()

# Añadir las columnas
fig.add_trace(go.Bar(
    x=df_agrupado["Semana"],
    y=df_agrupado["Cabinas"],
    name='Cabinas',
    hovertemplate="<b>Semana %{x}</b><br><b>Cabinas: %{y}</b>",
))
fig.add_trace(go.Bar(
    x=df_agrupado["Semana"],
    y=df_agrupado["Periodo de Cabinas"],
    name='Periodo de Cabinas',
    hovertemplate="<b>Semana %{x}</b><br><b>Periodo de Cabinas: %{y}</b>",
))
fig.add_trace(go.Bar(
    x=df_agrupado["Semana"],
    y=df_agrupado["Suspensiones"],
    name='Suspensiones',
    hovertemplate="<b>Semana %{x}</b><br><b>Suspensiones: %{y}</b>",
))

# Configurar el layout de la figura
fig.update_layout(
    barmode='group',  # Agrupa las barras
    title="Cantidad de Cabinas y Suspensiones sometidas a Mantenimiento en unidades 2023",
    xaxis_title="Semana",
    #yaxis_title="Valor",
    legend_title="Tipo"
)

# Crear la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Mantenimiento de Cabinas"),
    html.Div([
        html.H3(f"Total Cabinas en el Periodo: {suma_cabinas_total}"),
        html.H3(f"Total Suspensiones en el Periodo: {suma_suspensiones}")
    ], style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
    html.Div([
        html.P("Las cabinas sometidas a mantenimiento mensual consideran la inspección visual, limpieza y lubricación de cabinas cada seis semanas."),
    ], style={'margin-top': '20px'}),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_cabinas.columns],
        data=df_cabinas.to_dict('records'),
        style_table={'overflowX': 'auto', 'width': 'fit-content', 'margin': '0 auto'},  # Ajustar tabla y centrar
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        # Redondear valores a 2 decimales y añadir "%" al final
        style_data_conditional=[{
            'if': {'column_id': c},
            'type': 'numeric',
            'format': {'specifier': '2f %'}  # Añade el signo "%" al final
        } for c in df_cabinas.columns if c == 'Cumplimiento del 10%'],
    ),
    html.P("Solo el 10% de las suspensiones de cabinas de cada línea son sometidas, cada gestión, a mantenimientos preventivos siendo las tareas de mantenimiento el desmontaje, limpieza, inspección visual, ensayos no destrcutivos y lubricación"),
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
