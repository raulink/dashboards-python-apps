import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
import dash_table

# Cargar los datos desde el archivo Excel
df = pd.read_excel("costo16horas.xlsx", sheet_name="CUMPLIMIENTO ESTACIONES", usecols="B:I", skiprows=0)

# Agrupar por semana y calcular el promedio de "Semanal", el máximo de "Mensual" y "Trimestral"
df_promedio = df.groupby("Semana").agg({'Semanal': 'mean', 'Mensual': 'max', 'Trimestral': 'max'}).reset_index()

# Redondear los datos a 2 decimales
df_promedio = df_promedio.round(2)

# Calcular los valores específicos para las etiquetas
promedio_semanal = df_promedio['Semanal'].mean()
maximo_mensual = df_promedio['Mensual'].max()
maximo_trimestral = df_promedio['Trimestral'].max()

# Crear la figura
fig = go.Figure()

# Añadir las líneas y los puntos de intersección
for col in ["Semanal", "Mensual", "Trimestral"]:
    fig.add_trace(go.Scatter(
        x=df_promedio["Semana"],
        y=df_promedio[col],
        mode='lines+markers',
        name=col,
        hovertemplate="<b>Semana %{x}</b><br><b>%{text}</b>",
        text=[f"{col} {y:.2f}" for y in df_promedio[col]]
    ))

# Configurar el layout de la figura
fig.update_layout(
    title="Cumplimiento de Mantenimiento Preventivo de Estacion en porcentaje 2023",
    xaxis_title="Semana",
    yaxis_title="Cumplimiento",
    legend_title="Tipo"
)

# Crear la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Cumplimiento de Estaciones"),
    html.Div([
        html.P(f"Promedio Semanal: {promedio_semanal:.2f}"),
        html.P(f"Máximo Mensual: {maximo_mensual:.2f}"),
        html.P(f"Máximo Trimestral: {maximo_trimestral:.2f}")
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    dcc.Graph(figure=fig),
    html.Div([
        html.P("El cumplimiento trimestral de estaciones está referido a las actividades ejecutadas con respecto de las planificadas en cuanto al mantenimiento predeterminado (preventivo) en porcentaje realizado en las estaciones de la EETC MT cada trimestre o 13 semanas. Para LTVS se considera de forma bimensual."),
        html.P("El cumplimiento mensual de mantenimiento en estaciones está referido a las actividades ejecutadas con respecto de las planificadas en cuanto al mantenimiento predeterminado (preventivo) en porcentaje realizado en las estaciones de la EETC MT cada 5 semanas."),
        html.P("El cumplimiento semanal de mantenimiento en estaciones está referido a las actividades ejecutadas con respecto de las planificadas en cuanto al mantenimiento predeterminado (preventivo) en porcentaje realizado en las estaciones de la EETC MT cada semana. Para LTVS se considera de forma quincenal.")
    ], style={'margin-top': '20px'}),
    html.H2("Tabla Agrupada por Semana"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_promedio.columns],
        data=df_promedio.to_dict('records'),
        style_table={'overflowX': 'auto', 'width': 'fit-content', 'margin': '0 auto'},  # Ajustar tabla y centrar
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
        style_cell={'textAlign': 'left', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        # Redondear valores a 2 decimales
        style_data_conditional=[{
            'if': {'column_id': c},
            'type': 'numeric',
            'format': {'specifier': '.2f'}
        } for c in df_promedio.columns],
    ),
])

# Ejecutar el servidor de Dash solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)
