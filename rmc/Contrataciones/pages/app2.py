from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='Dash: A web application framework for Python.'),
])

server = app.server  # This is the Flask instance underlying the Dash app

if __name__ == '__main__':
    app.run_server(debug=True)
