import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dash import Dash, dcc, html,callback
from dash.dependencies import Input, Output

# Conéctate a la base de datos MySQL
engine = create_engine('mysql+pymysql://mantto:Sistemas0,@192.168.100.50/Catalogo')

# Cargar datos desde la tabla 'salida' a un DataFrame
df = pd.read_sql('SELECT * FROM salida;', engine)

# Convertir la columna 'fecha_salida' a tipo de datos datetime
df['fecha_salida'] = pd.to_datetime(df['fecha_salida'], dayfirst=True)

# Reemplazar `None` o `null` por un valor adecuado en las columnas problemáticas
df['clasificacion_trabajo'] = df['clasificacion_trabajo'].fillna('')
df['partida_presupuestaria'] = df['partida_presupuestaria'].fillna('')
df['ubicacion'] = df['ubicacion'].fillna('')

# Crear la aplicación Dash
app = Dash(__name__)

# Obtener las fechas mínima y máxima
fecha_min = df['fecha_salida'].min()
fecha_max = df['fecha_salida'].max()

# Crear una paleta de colores personalizada para las ubicaciones
color_discrete_map = {
    "LINEA AMARILLA": "yellow",
    "LINEA ROJA": "red",
    "LINEA VERDE": "green",
    "LINEA AZUL": "blue",
    "LINEA NARANJA": "orange",
    "LINEA BLANCA": "black",
    "LINEA CELESTE": "lightblue",
    "LINEA MORADA": "purple",
    "LINEA CAFE": "brown",
    "LINEA PLATEADA": "silver"
}

# Crear el layout de la aplicación
layout = html.Div([
    # Comboboxes para filtros
    dcc.Dropdown(
        id='codigo-item-dropdown2',
        options=[
            {'label': str(item), 'value': item} for item in df['codigo_item'].unique()
        ],
        placeholder='Selecciona un código de item',
        style={'margin-bottom': '10px'}
    ),
    dcc.Dropdown(
        id='descripcion-dropdown2',
        options=[
            {'label': str(desc), 'value': desc} for desc in df['descripcion'].unique()
        ],
        placeholder='Selecciona una descripción',
        style={'margin-bottom': '10px'}
    ),
    dcc.Dropdown(
        id='anio-dropdown2',
        options=[
            {'label': str(anio), 'value': str(anio)} for anio in df['fecha_salida'].dt.year.unique()
        ],
        placeholder='Selecciona un año',
        style={'margin-bottom': '10px'}
    ),
    dcc.Dropdown(
        id='clasificacion-trabajo-dropdown',
        options=[
            {'label': str(clas), 'value': clas} for clas in df['clasificacion_trabajo'].unique()
        ],
        placeholder='Selecciona una clasificación de trabajo',
        style={'margin-bottom': '10px'}
    ),
    dcc.Dropdown(
        id='partida-presupuestaria-dropdown',
        options=[
            {'label': str(partida), 'value': partida} for partida in df['partida_presupuestaria'].unique()
        ],
        placeholder='Selecciona una partida presupuestaria',
        style={'margin-bottom': '10px'}
    ),
    # Espacio para mostrar el gráfico
    dcc.Graph(id='line-chart2'),
    # Range Slider para seleccionar un rango de fechas
    
    # Etiquetas para mostrar la suma de cantidades y el precio unitario máximo
    html.Div([
        html.P(id='suma-cantidad-label2', style={'font-weight': 'bold'}),
        html.P(id='precio-unitario-maximo-label2', style={'font-weight': 'bold'}),
    ])
])

# Callback para actualizar el gráfico y las etiquetas según los valores seleccionados en los comboboxes y el range slider
@callback(
    [
        Output('line-chart2', 'figure'),
        Output('suma-cantidad-label2', 'children'),
        Output('precio-unitario-maximo-label2', 'children')
    ],
    [
        Input('codigo-item-dropdown2', 'value'),
        Input('descripcion-dropdown2', 'value'),
        Input('anio-dropdown2', 'value'),
        Input('clasificacion-trabajo-dropdown', 'value'),
        Input('partida-presupuestaria-dropdown', 'value'),
    ]
)
def update_graph_and_labels(codigo_item, descripcion, anio, clasificacion_trabajo, partida_presupuestaria):
    # Filtrar datos según los valores seleccionados en los comboboxes
    df_filtrado = df.copy()
    
    # Filtrar datos según los valores seleccionados
    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    if descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]
    if anio:
        anio = int(float(anio))
        df_filtrado = df_filtrado[df_filtrado['fecha_salida'].dt.year == anio]
    if clasificacion_trabajo:
        df_filtrado = df_filtrado[df_filtrado['clasificacion_trabajo'] == clasificacion_trabajo]
    if partida_presupuestaria:
        df_filtrado = df_filtrado[df_filtrado['partida_presupuestaria'] == partida_presupuestaria]

    # Agrupar datos por fecha, ubicación, y sumar la cantidad
    df_agrupado = df_filtrado.groupby([df_filtrado['fecha_salida'].dt.to_period('M'), 'ubicacion'])['cantidad'].sum().reset_index()
    df_agrupado['fecha_salida'] = df_agrupado['fecha_salida'].astype(str)

    # Crear gráfico de línea usando Plotly
    fig = px.line(df_agrupado, x='fecha_salida', y='cantidad', title='Cantidad por fecha de salida', color='ubicacion', color_discrete_map=color_discrete_map, markers=True)
    fig.update_layout(height=600)
    
    # Calcular la suma de cantidades
    suma_cantidad = df_filtrado['cantidad'].sum()
    
    # Calcular el precio unitario máximo
    precio_unitario_maximo = df_filtrado['precio_unitario'].max()
    
    # Formatear los resultados como cadenas de texto para mostrarlos en las etiquetas
    suma_cantidad_label = f"Suma de cantidades: {suma_cantidad}"
    precio_unitario_maximo_label = f"Precio unitario máximo: {precio_unitario_maximo}"
    
    # Retornar el gráfico y las etiquetas de resultados
    return fig, suma_cantidad_label, precio_unitario_maximo_label
