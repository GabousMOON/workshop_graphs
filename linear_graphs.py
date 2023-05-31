import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div
from bokeh.plotting import figure, show

x = np.linspace(-10, 10, 500)
y = x

source = ColumnDataSource(data=dict(x=x, y=y))

div = Div(
    text="""
        <p>This is a Linear Graph that is modeled by the equation y=mx + b</p>
        <ul>
            <li>m is the slope of the function</li>
            <li>b is the y intercept of the function</li>
            <li>m is calculated by finding $$frac{y_2 - y_1}{x_2 - x_1}$$</li>
            <li>b can be calculated by setting x=0 and then solving for b</li>
        </ul>
    """
)

plot = figure(
    y_range=(-10, 10),
    width=600,
    height=600,
    title="y=mx + b",
    tools="",
    toolbar_location=None,
)

plot.line("x", "y", source=source, line_width=3, line_color="#578164")

rise = Slider(
    start=-10,
    end=10,
    value=1,
    step=0.1,
    title="Change in Rise",
    bar_color="green",
)
run = Slider(
    start=0.1,
    end=10,
    value=1,
    step=0.1,
    title="Change in run",
    bar_color="green",
)
y_intercept = Slider(
    start=-6.4, end=6.4, value=0, step=0.1, title="y-intercept (b)", bar_color="green"
)


callback = CustomJS(
    args=dict(source=source, rise=rise, run=run, y_intercept=y_intercept),
    code="""
    const del_y = rise.value
    const del_x = run.value
    const B = y_intercept.value
    const M = del_y / del_x

    const x = source.data.x
    const y = Array.from(x, (x) => B + M*x)


    source.data = { x, y }
""",
)

rise.js_on_change("value", callback)
run.js_on_change("value", callback)
y_intercept.js_on_change("value", callback)

plot.xaxis.fixed_location = 0
plot.yaxis.fixed_location = 0

show(row(column(div, rise, run, y_intercept), plot))
