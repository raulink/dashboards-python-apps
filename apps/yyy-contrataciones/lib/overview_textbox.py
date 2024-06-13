from dash import dcc
import dash_bootstrap_components as dbc

content = """
#### Dashboards de mantenimiento

Este es el proyecto base para la visualización de datos del Departamento de Mantenimiento


La descripción completa se presenta en el documento, [Sistema de Contrataciones](https://docs.google.com/document/d/1dCmA8yI97d3_5Smukmo6prUbArymdYG8vqvryUCo3a4/edit).

Comprende inicialmente 2 modulos:
* Entradas / Salidas almacen
* Procesos PAC

Para el control de procesos de contratacion se propone un flujo de trabajo realizado en la direccion [Lineas](http://lineas.miteleferico.bo)

"""



card = dbc.Card(
    dcc.Markdown(content, link_target="_blank"),
    className="shadow-sm p-3",
)
