from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate
from num2words import num2words

class ReportGenerator:
    def __init__(self, template_path: str, excel_path: str, output_path: str = None):
        self.template_path = Path(template_path)
        self.excel_path = Path(excel_path)
        self.output_path = Path(output_path) if output_path else self.template_path.with_name('output.docx')
        self.data = {}
    
    def read_excel_data(self):
        df = pd.read_excel(self.excel_path, sheet_name="Datos", usecols="A:B", skiprows=0)
        self.data = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        self.data = {str(k): v for k, v in self.data.items()}

    @staticmethod
    def convertir_a_literal(numero):
        numero_redondeado = round(numero, 2)
        entero, decimal = str(numero_redondeado).split('.')
        entero = int(entero)
        decimal = int(decimal)
        entero_en_palabras = num2words(entero, lang='es')
        resultado = f"{entero_en_palabras} {decimal}/100"
        return resultado

    def process_data(self):
        self.data['Monto'] = round(self.data['Monto'], 2)
        self.data['monto_literal'] = self.convertir_a_literal(self.data['Monto'])
        
        df_tabla1 = pd.read_excel(self.excel_path, sheet_name="Tabla1")
        df_tabla2 = pd.read_excel(self.excel_path, sheet_name="Tabla2")
        
        df_tabla1 = df_tabla1.fillna(0).applymap(lambda x: round(x, 2) if isinstance(x, float) else x)
        df_tabla2 = df_tabla2.fillna(0).applymap(lambda x: round(x, 2) if isinstance(x, float) else x)
        
        self.data.update({'tabla1': df_tabla1.to_dict('split')})
        self.data.update({'tabla2': df_tabla2.to_dict('split')})

    def generate_report(self):
        doc = DocxTemplate(self.template_path)
        doc.render(self.data)
        doc.save(self.output_path)
    
    def create_report(self):
        self.read_excel_data()
        self.process_data()
        self.generate_report()
        return str(self.output_path), self.output_path.name

# Example usage:
# generator = ReportGenerator('./proceso/inf_plantilla.docx', './proceso/items.xlsx')
# output_path, output_name = generator.create_report()
# print(f"Report generated at: {output_path} with name: {output_name}")
