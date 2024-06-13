import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from io import BytesIO
import base64
import os
from docxtpl import DocxTemplate

# Crear la carpeta temp si no existe
if not os.path.exists('temp'):
    os.makedirs('temp')

# Inicializar la app de Dash con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Sistema de Contrataciones"),
    
    # Botón para subir el archivo Excel
    dcc.Upload(
        id='upload-excel',
        children=html.Button('Subir Archivo Excel'),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
    ),
    
    # Botón para subir la plantilla de Word
    dcc.Upload(
        id='upload-template',
        children=html.Button('Subir Plantilla'),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
    ),
    
    # Botón para generar el documento final
    html.Button("Generar Documento", id="generate-button", n_clicks=0, disabled=True),
    dcc.Download(id="download-docx"),
    
    # Mensaje de estado
    html.Div(id='output-state', style={'marginTop': 20})
])

@app.callback(
    [Output('generate-button', 'disabled'), Output('output-state', 'children')],
    [Input('upload-excel', 'contents'), Input('upload-template', 'contents')],
    [State('upload-excel', 'filename'), State('upload-template', 'filename')]
)
def handle_uploads(excel_contents, template_contents, excel_filename, template_filename):
    messages = []
    if excel_contents:
        content_type, content_string = excel_contents.split(',')
        decoded = base64.b64decode(content_string)
        path = os.path.join('temp', excel_filename)
        with open(path, 'wb') as f:
            f.write(decoded)
        messages.append(f"Archivo Excel {excel_filename} subido exitosamente.")
    
    if template_contents:
        content_type, content_string = template_contents.split(',')
        decoded = base64.b64decode(content_string)
        path = os.path.join('temp', template_filename)
        with open(path, 'wb') as f:
            f.write(decoded)
        messages.append(f"\nPlantilla Word {template_filename} subida exitosamente.")
    
    if excel_contents and template_contents:
        return False, " ".join(messages)
    else:
        return True, " ".join(messages)

@app.callback(
    Output('download-docx', 'data'),
    [Input('generate-button', 'n_clicks')],
    [State('upload-excel', 'filename'), State('upload-template', 'filename')]
)
def generate_document(n_clicks, excel_filename, template_filename):
    if n_clicks >0:
        # Leer datos del archivo Excel
        excel_path = os.path.join('temp', excel_filename)        
        print(f"Path archivo excel: {template_path}")
        
        # Leer los datos de Excel desde la hoja especificada
        df = pd.read_excel(excel_path, sheet_name="Hoja1", usecols="A:B", skiprows=0)

        # Convertir el DataFrame en un diccionario (clave-valor)
        # Primera columna será las claves (Placeholder), segunda columna los valores (Value)
        data = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        # Asegúrate de que todas las claves sean cadenas de caracteres
        data = {str(k): v for k, v in data.items()}        
        
        
        from docxtpl import DocxTemplate

        # Definir la ruta del archivo
        template_path = os.path.join('temp',template_filename)  # dynamic_table_tpl.docx'
        print(f"Path plantilla :{template_path}")

        # Verificar si el archivo existe
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"El archivo {template_path} no se encuentra.")
        
        tpl = DocxTemplate(template_file=template_path)

        tpl.render(data)
        tpl.save('output/dynamic_table.docx')
        # context = {row['Variable']: row['Valor'] for _, row in df.iterrows()}
        #tpl.render(context)
        
        # Guardar el documento generado
        output_path = ('output.docx')
        tpl.save(output_path)
        
        return dcc.send_file(output_path)
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
