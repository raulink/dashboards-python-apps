from dash import dcc, html, Input, Output, callback
import pandas as pd
import sqlalchemy as sa
import plotly.express as px
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Conexión a la base de datos
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
url = f'postgresql://{user}:{password}@{host}:5432/{db}'

print(f"Conectando BD Postgres: {url}")
# Crear un motor de base de datos con SQLAlchemy
engine = sa.create_engine(url)

# Cargar datos de la base de datos
df_pac = pd.read_sql("SELECT * FROM pac", con=engine)

# Callback para actualizar el gráfico de línea
@callback(
    Output('line-chart', 'figure'),  # El callback retorna un gráfico Plotly
    [Input('gestion-checkbox', 'value')]  # El callback recibe valores de un checklist
)
def update_graph(selected_gestiones):
    # Filtrar el dataframe por las gestiones seleccionadas
    df_filtrado = df_pac[df_pac['gestion'].isin(selected_gestiones)]
    
    # Agrupar los datos filtrados por 'gestion' y 'causal' y calcular la media de 'precio_referencial'
    df_grouped = df_filtrado.groupby(['gestion', 'causal']).agg({
        'precio_referencial': 'mean'  # Calcula la media de precio referencial
    }).reset_index()  # Resetea el índice para que sea un dataframe estándar

    # Crear un gráfico de línea utilizando Plotly Express
    fig = px.line(
        df_grouped,
        x='gestion',  # Eje x será 'gestion'
        y='precio_referencial',  # Eje y será 'precio_referencial'
        color='causal',  # Diferenciar por 'causal' con colores
        markers=True,  # Mostrar marcadores en el gráfico
        title='Precio Referencial por Causal'  # Título del gráfico
    )
    
    # Retornar la figura (gráfico) creado
    return fig

# Diseño de la aplicación
layout = html.Div(
    [
        # Espacio para mostrar el gráfico
        html.Div(
            dcc.Graph(id='line-chart'),  # Contiene el gráfico que será actualizado por el callback
            style={'width': '90%', 'display': 'inline-block'}  # Estilo del div que contiene el gráfico
        ),
        # Sección para los checkboxes
        html.Div(
            [
                # Título para los checkboxes
                html.H3("Gestión"),
                # Checkbox para seleccionar las gestiones a visualizar
                dcc.Checklist(
                    id='gestion-checkbox',  # ID para recibir valores del checklist
                    options=[
                        # Crea una opción para cada gestión única en el dataframe
                        {'label': str(gestion), 'value': gestion} for gestion in df_pac['gestion'].unique()
                    ],
                    # Establece los valores seleccionados inicialmente como todas las gestiones únicas
                    value=df_pac['gestion'].unique().tolist(),
                    # Estilo para mostrar las opciones en bloques
                    labelStyle={'display': 'block'}
                )
            ],
            style={'width': '10%', 'display': 'inline-block', 'padding-left': '10px'}  # Estilo del div que contiene los checkboxes
        )
    ],
    # Estilo para alinear los divs horizontalmente
    style={'display': 'flex', 'align-items': 'center'}
)
