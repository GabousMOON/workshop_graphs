import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div, SetValue
from bokeh.plotting import figure, show
from bokeh.io import curdoc


x = np.linspace(-15, 15, 500)
y = np.exp(x)

source = ColumnDataSource(data=dict(x=x, y=y))

# TODO: Clarify the description
div = Div(
    text=r"""
        <p>This is an exponential graph that is modeled by the equation <br>
        <div style = "text-align: center; font-size: 25px">$$y=ae^{x-h} + k$$</div>
        </p>
        <ul>
            <li>a is the leading coefficient and determines the dilation or reflection</li>
            <li>h is the horizontal translation</li>
            <li>k is the vertical translation</li>
        </ul>
    """,
    styles={
        "font-size": "20px",
    },
)

# TODO: Format the graph to be more responsive to window size
plot = figure(
    y_range=(-5, 5),
    x_range=(-5, 5),
    width=450,
    height=450,
    tools="",
    toolbar_location=None,
    styles={"margin-left": "10%"},
)


plot.xaxis.ticker = [num for num in range(-6, 7)]
plot.xgrid.grid_line_alpha = 0.5
plot.xgrid.grid_line_color = "#111111"

plot.yaxis.ticker = [num for num in range(-6, 7)]
plot.ygrid.grid_line_alpha = 0.5
plot.ygrid.grid_line_color = "#111111"

plot.outline_line_width = 6
plot.outline_line_color = "#78be20"
plot.outline_line_alpha = 0.7

# TODO: Create a line for the asymptote
plot.line("x", "y", source=source, line_width=3.5, line_color="#78be20")

leading_coefficient = Slider(
    width=500,
    start=-10,
    end=10,
    value=1,
    step=0.01,
    title="Leading Coefficient",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)

horiz_displace = Slider(
    width=500,
    start=-10,
    end=10,
    value=1,
    step=0.01,
    title="Horizontal displacement",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)
vert_displace = Slider(
    width=500,
    start=-10,
    end=10,
    value=0,
    step=0.01,
    title="Vertical Translation",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)

equation_div = Div(
    text="y=e<sup>x</sup>",
    styles={"font-size": "25px", "font-style": "italic", "margin-left": "45%"},
)

# TODO: Creating asymptote line compatability
# TODO: Fix the graph disappearing bug
callback = CustomJS(
    args=dict(
        source=source,
        horiz_displace=horiz_displace,
        leading_coefficient=leading_coefficient,
        vert_displace=vert_displace,
        eq_div=equation_div,
    ),
    code="""
    const h = horiz_displace.value
    const a = leading_coefficient.value
    const k = vert_displace.value

    const x = source.data.x
    const y = Array.from(x, (x) => a*Math.exp(x-h) + k)


    if (a*10%10 == 0){
        var new_a = String(a)
    } else{
        var new_a = String(a.toFixed(2))
    }

    if (h*10%10 == 0 && h > 0){
        var my_exp = "x-" + String(h)
    } else if (h*10%10 == 0 && h < 0){
        var my_exp = "x+" + String(Math.abs(h))
    } else if (h == 0){
        var my_exp = "x"
    } else if (h*10%10 != 0 && h > 0){
        var my_exp = "x-" + String(h.toFixed(2))
    } else if (h*10%10 != 0 && h < 0){
        var my_exp = "x+" + String(Math.abs(h).toFixed(2))
    }

    if (k*10%10 == 0 && k > 0){
        var new_k = "+" + String(k)
    } else if (k*10%10 == 0 && k < 0){
        var new_k = String(k)
    } else if (k == 0){
        var new_k = ""
    } else if (k*10%10 != 0 && k > 0){
        var new_k = "+" + String(k.toFixed(2))
    } else if (k*10%10 !=0 && k < 0){
        var new_k = String(k.toFixed(2))
    }

    eq_div.text = `y=${new_a}e<sup>${my_exp}</sup>${new_k}`

    source.data = { x, y }
""",
)

horiz_displace.js_on_change("value", callback)
leading_coefficient.js_on_change("value", callback)
vert_displace.js_on_change("value", callback)

plot.xaxis.fixed_location = 0
plot.yaxis.fixed_location = 0

show(
    row(
        column(
            div,
            leading_coefficient,
            horiz_displace,
            vert_displace,
            styles={"margin-left": "10%"},
        ),
        column(equation_div, plot, styles={"text-align": "center"}),
        styles={"margin-top": "3%"},
    )
)
