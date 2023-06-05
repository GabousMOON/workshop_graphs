import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div, RadioButtonGroup
from bokeh.plotting import figure, show
from bokeh.io import curdoc


x = np.linspace(-10, 10, 100)
y = np.exp(x)
asymptote = x * 0

source = ColumnDataSource(data=dict(x=x, y=y, asymptote=asymptote))

# TODO: Clarify the description
div = Div(
    text=r"""
        <p>This is an exponential graph that is modeled by the equation <br>
        <div style = "text-align: center; font-size: 25px">$$y=ab^{x-h} + k$$</div>
        </p>
        <ul>
            <li>$$a$$ determines the reflection over the $$x$$ axis</li>
            <li>$$b$$ determines the dilation</li>
            <li>$$h$$ determines the horizontal translation</li>
            <li>$$k$$ determines the vertical translation</li>
            <li>the sign on $$x$$ determines reflection over the $$y$$ axis</li>
        </ul>
    """,
    styles={
        "font-size": "20px",
    },
)

# TODO: Format the graph to be more responsive to window size
plot = figure(
    y_range=(-6, 6),
    x_range=(-6, 6),
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

plot.outline_line_width = 1
plot.outline_line_color = "#000000"

plot.line(
    "x",
    "asymptote",
    source=source,
    line_width=3.5,
    line_color="#000000",
    line_dash="dashed",
)
plot.line("x", "y", source=source, line_width=3, line_color="#78bb20")


leading_coefficient = Slider(
    width=500,
    start=-6,
    end=6,
    value=2,
    step=0.05,
    title=r"Leading Coefficient $$a$$",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)

b_value = Slider(
    width=500,
    start=0,
    end=6,
    value=2,
    step=0.05,
    title=r"Dilation $$b$$",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)

horiz_displace = Slider(
    width=500,
    start=-6,
    end=6,
    value=0,
    step=0.05,
    title=r"Horizontal displacement: $$h$$",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)
vert_displace = Slider(
    width=500,
    start=-6,
    end=6,
    value=0,
    step=0.05,
    title=r"Vertical Translation: $$k$$",
    bar_color="green",
    styles={"font-size": "25px", "text-align": "center"},
)

# TODO: Add create an option to make x positive or negative


equation_div = Div(
    text=r"$$y=ab^{x}$$",
    styles={
        "font-size": "25px",
        "font-style": "italic",
        "margin-left": "30%",
        "font-weight": "bold",
    },
)

# TODO: Fix the graph disappearing bug
callback = CustomJS(
    args=dict(
        source=source,
        horiz_displace=horiz_displace,
        leading_coefficient=leading_coefficient,
        vert_displace=vert_displace,
        b_val=b_value,
        eq_div=equation_div,
    ),
    code="""
    const h = horiz_displace.value
    const a = leading_coefficient.value
    const k = vert_displace.value
    const b = b_val.value
    const x = source.data.x
    const y = Array.from(x, (x) => a*b**(x-h) + k)
    const asymptote = Array.from(x, (x) => k)

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

    eq_div.text = `y=${new_a}(${String(b.toFixed(2))})<sup>${my_exp}</sup>${new_k}`

    source.data = { x, y, asymptote }
""",
)

horiz_displace.js_on_change("value", callback)
leading_coefficient.js_on_change("value", callback)
vert_displace.js_on_change("value", callback)
b_value.js_on_change("value", callback)

plot.xaxis.fixed_location = 0
plot.yaxis.fixed_location = 0

show(
    row(
        column(
            div,
            leading_coefficient,
            b_value,
            horiz_displace,
            vert_displace,
            styles={"margin-left": "10%"},
        ),
        column(equation_div, plot, styles={"text-align": "center"}),
        styles={"margin-top": "3%"},
    )
)
