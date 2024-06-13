import os
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los detalles de la conexión desde el archivo .env
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Crear la URL de conexión
connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

# Crear el motor de conexión con SQLAlchemy
engine = create_engine(connection_string)

# Cargar datos desde la tabla 'ingreso' en un DataFrame
df = pd.read_sql('SELECT * FROM ingreso;', engine)

# Convertir la columna 'fecha_ingreso' a tipo de datos datetime
df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], dayfirst=True)

# Obtener opciones únicas para el combobox de 'codigo_item', 'descripcion' y 'anio'
codigo_item_options = [{'label': item, 'value': item} for item in df['codigo_item'].unique()]
descripcion_options = [{'label': desc, 'value': desc} for desc in df['descripcion'].unique()]
anio_options = [{'label': str(anio), 'value': anio} for anio in df['fecha_ingreso'].dt.year.unique()]

# Define el diseño de la aplicación
layout = html.Div([
    # Combobox para seleccionar el 'codigo_item'
    dcc.Dropdown(
        id='codigo-item-dropdown',
        options=codigo_item_options,
        placeholder='Selecciona un código de ítem',
        style={'margin-bottom': '10px'}
    ),
    # Combobox para seleccionar la 'descripcion'
    dcc.Dropdown(
        id='descripcion-dropdown',
        options=descripcion_options,
        placeholder='Selecciona una descripción',
        style={'margin-bottom': '10px'}
    ),
    # Combobox para seleccionar el 'anio'
    dcc.Dropdown(
        id='anio-dropdown',
        options=anio_options,
        placeholder='Selecciona un año',
        style={'margin-bottom': '10px'}
    ),
    # Gráfico de línea
    dcc.Graph(id='line-chart1'),
    # Div para mostrar las etiquetas con los resultados
    html.Div([
        html.P(id='suma-cantidad-label', style={'font-weight': 'bold'}),
        html.P(id='precio-unitario-maximo-label', style={'font-weight': 'bold'})
    ])
])

# Crear gráfico inicial sin filtro
fig = px.line(df, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)

# Callback para actualizar el gráfico y las etiquetas según las selecciones
@callback(
    [
        Output('line-chart1', 'figure'),
        Output('suma-cantidad-label', 'children'),
        Output('precio-unitario-maximo-label', 'children')
    ],
    [
        Input('codigo-item-dropdown', 'value'),
        Input('descripcion-dropdown', 'value'),
        Input('anio-dropdown', 'value')
    ]
)
def update_graph(codigo_item, descripcion, anio):
    # Crear una copia del DataFrame original para filtrar
    df_filtrado = df.copy()

    # Filtrar datos según el 'codigo_item' seleccionado
    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    
    # Filtrar datos según la 'descripcion' seleccionada
    if descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]
    
    # Filtrar datos según el 'anio' seleccionado
    if anio:
        df_filtrado = df_filtrado[df_filtrado['fecha_ingreso'].dt.year == int(anio)]

    # Crear gráfico de línea usando Plotly
    fig = px.line(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)
    
    # Calcular la suma de cantidades
    suma_cantidad = df_filtrado['cantidad'].sum()

    # Calcular el precio unitario máximo si existe la columna 'precio_unitario'
    if 'precio_unitario' in df_filtrado.columns:
        precio_unitario_maximo = df_filtrado['precio_unitario'].max()
    else:
        precio_unitario_maximo = None

    # Formatear los resultados como cadenas de texto para mostrarlos en las etiquetas
    suma_cantidad_label = f"Suma de cantidades: {suma_cantidad}"
    precio_unitario_maximo_label = f"Precio unitario máximo: {precio_unitario_maximo}" if precio_unitario_maximo else "Precio unitario máximo: N/A"

    # Retornar el gráfico y las etiquetas de resultados
    return fig, suma_cantidad_label, precio_unitario_maximo_label
