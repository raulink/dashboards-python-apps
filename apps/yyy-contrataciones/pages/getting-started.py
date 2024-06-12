import dash

from lib.code_and_show import example_app


dash.register_page(
    __name__, order=0, description=" Aplicacion ingresos ."
)

filename = __name__.split("pages.")[1]

notes = """

#### Dash Components in App:  
- [Dropdown](https://dash.plotly.com/dash-core-components/dropdown)

#### Plotly Documentation:  
- [Bar Plots](https://plotly.com/python/bar-charts/)
- [Getting started with Plotly](https://plotly.com/python/getting-started/)

#### Contributed by:
This example app was contributed by [Plotly](https://plotly.com/python/)

"""


layout = example_app(filename, notes=notes)
