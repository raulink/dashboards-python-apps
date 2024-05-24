import dash

from lib.code_and_show import example_app


dash.register_page(
    __name__,
    description="Iris plot with an interactive horizontal line. It has a top-bottom layout and a regular-callback."
)

filename = __name__.split("pages.")[1]

notes = """
#### Dash Components in App:
- [Slider](https://dash.plotly.com/dash-core-components/slider)

#### Plotly Documentation:  
- [Scatter Plot](https://plotly.com/python/line-and-scatter/)
- [Horizontal and Vertical Lines and Rectangles](https://plotly.com/python/horizontal-vertical-shapes/)

##### Contributed by:
This example app was contributed by [Plotly](https://plotly.com/python/)
"""

layout = example_app(filename, notes=notes)
