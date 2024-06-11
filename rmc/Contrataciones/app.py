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
        messages.append(f"Plantilla Word {template_filename} subida exitosamente.")
    
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
        df = pd.read_excel(excel_path, sheet_name='Hoja1')
        
        # Renderizar la plantilla de Word con los datos del Excel
        #template_path = os.path.join('temp', template_filename)
        #doc = DocxTemplate(template_path)
        
        
        from docxtpl import DocxTemplate

                # Definir la ruta del archivo
        template_path = 'dynamic_table_tpl.docx'
        

        # Verificar si el archivo existe
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"El archivo {template_path} no se encuentra.")
        
        tpl = DocxTemplate(template_file=template_path)


        context = {
            'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
            'tbl_contents': [
                {'label': 'yellow', 'cols': ['banana', 'capsicum', 'pyrite', 'taxi']},
                {'label': 'red', 'cols': ['apple', 'tomato', 'cinnabar', 'doubledecker']},
                {'label': 'green', 'cols': ['guava', 'cucumber', 'aventurine', 'card']},
            ],
        }

        tpl.render(context)
        tpl.save('output/dynamic_table.docx')
        # context = {row['Variable']: row['Valor'] for _, row in df.iterrows()}
        tpl.render(context)
        
        # Guardar el documento generado
        output_path = ('output.docx')
        tpl.save(output_path)
        
        return dcc.send_file(output_path)
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
