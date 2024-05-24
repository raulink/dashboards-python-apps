import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import sys
from importlib import import_module

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the sidebar
sidebar = dbc.Nav(
    [
        dbc.NavLink("Page 1", href="/page1", id="page1-link"),
        dbc.NavLink("Page 2", href="/page2", id="page2-link"),
        dbc.NavLink("Page 3", href="/page3", id="page3-link"),
    ],
    vertical=True,
    pills=True,
)

# Define the content area
content = html.Div(id="page-content")

# Define the app layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(content, width=10),
            ]
        )
    ],
    fluid=True,
)

# Callback to update the active link and load the correct page
@app.callback(
    [Output(f"page{page}-link", "active") for page in range(1, 4)],
    [Input("url", "pathname")]
)
def toggle_active_links(pathname):
    if pathname is None:
        return [False, False, False]
    return [pathname == f"/page{page}" for page in range(1, 4)]

# Callback to update the page content
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname is None or pathname == "/":
        pathname = "/page1"
    module_name = pathname.strip("/").replace("/", ".")
    try:
        module = import_module(f'python.{module_name}')
        return module.layout
    except ImportError:
        return html.Div(["404 Page not found"])

# Add the location component to the layout
app.layout.children.append(dcc.Location(id="url"))

if __name__ == "__main__":
    app.run_server(debug=True)
