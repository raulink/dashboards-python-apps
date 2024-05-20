import pandas as pd
import plotly.express as px
import numpy as np
from dash import dcc, html
import dash_table


# Ruta al archivo de Excel en la misma carpeta del proyecto
excel_file = 'Ingresos 2017-20241.xlsx'

# Leer datos de la hoja de Excel especificada y el rango de celdas
df = pd.read_excel(excel_file, sheet_name=0, skiprows=16, usecols='A:K', nrows=12)

# Transponer el DataFrame para tener años como columnas y meses como filas
df = df.T
df.columns = df.iloc[0]  # Asigna los nombres de las columnas
df = df.iloc[1:]  # Remueve la primera fila con nombres de columnas
df.index.name = 'Gestion'  # Asigna nombre al índice

# Calcular totales de ingresos por mes
totales_por_Gestion = df.sum(axis=1)

# Ajuste de línea de tendencia logarítmica
x_values = np.arange(len(totales_por_Gestion))
y_values = totales_por_Gestion.values.astype(float)  # Convertimos a tipo float
y_values[y_values == 0] = np.nan  # Reemplazamos los valores 0 con NaN para evitar errores de logaritmos
y_log = np.log(y_values)
coef = np.polyfit(x_values, y_log, 1)
poly1d_fn = np.poly1d(coef)

# Predicción de valores futuros
periodos_futuros = 1
valores_futuros = np.exp(poly1d_fn(np.arange(len(totales_por_Gestion), len(totales_por_Gestion) + periodos_futuros)))

# Define el layout de la aplicación
layout = html.Div([
    # Gráfico de ingresos por mes y año
    dcc.Graph(
        id='ingresos-histogram',
        figure=px.histogram(
            df.reset_index(),  # Restablece el índice para tener 'index' como columna (meses)
            x='Gestion',  # Eje x: nombres de los meses
            y=df.columns,  # Eje y: ingresos por año
            labels={'value': 'Ingresos', 'variable': 'Meses'},  # Etiquetas de los ejes
            title='Histograma de ingresos por Gestion y año'  # Título del gráfico
        )
    ),
    # Gráfico de dispersión con línea de tendencia logarítmica y extrapolación
    dcc.Graph(
        id='scatter-tendencia',
        figure=px.scatter(
            x=x_values,  # Valores x: números de período
            y=totales_por_Gestion.values,  # Valores y: totales de ingresos por período
            title='Línea de tendencia logarítmica con extrapolación'
        ).add_scatter(
            x=np.arange(len(totales_por_Gestion) + periodos_futuros),  # Valores x: números de período (incluyendo futuros)
            y=np.concatenate((y_values, valores_futuros)),  # Valores y: totales de ingresos por período (incluyendo futuros)
            mode='lines',  # Línea
            line=dict(color='red', dash='dash'),  # Color y estilo de línea
            name='Tendencia logarítmica'  # Nombre de la serie
        ).update_layout(
            yaxis_title='Ingresos',  # Título del eje y
            xaxis_title='Periodo'  # Título del eje x
        )
    ),
    # Tabla de totales por mes
    dash_table.DataTable(
        id='totales-por-Gestion',
        columns=[
            # Una columna para cada mes
            {'name': Gestion, 'id': Gestion} for Gestion in totales_por_Gestion.index
        ],
        data=[
            # Los totales de ingresos por mes como una fila de datos
            {Gestion: totales_por_Gestion[Gestion] for Gestion in totales_por_Gestion.index}
        ],
        style_table={'overflowX': 'scroll'},  # Permitir desplazamiento horizontal
        style_cell={'textAlign': 'center'},  # Alinear texto al centro
        style_header={'fontWeight': 'bold'},  # Estilo del encabezado
    )
])
