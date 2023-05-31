import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div, MathML
from bokeh.plotting import figure, show

x = np.linspace(-10, 10, 500)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))

div = Div(
    text="""
        <p>This is a sinusoidal function represented by the equation <br> $$A\sin(Bx-C) + D$$ </p>
        <ul>
            <li>A is the amplitude</li>
            <li>B is the frequency</li>
            <li>C is the phase shift</li>
            <li>D is the vertical shift</li>
        </ul>

    """
)

plot = figure(
    y_range=(-5, 5),
    width=600,
    height=600,
    title="$$y=Asin(Bx-C) + D$$",
    tools="",
    toolbar_location=None,
)

plot.line("x", "y", source=source, line_width=3, line_color="#578164")

amp = Slider(
    start=0.1, end=10, value=1, step=0.1, title="Amplitude (A)", bar_color="green"
)
freq = Slider(
    start=0.1, end=10, value=1, step=0.1, title="Frequency (B)", bar_color="green"
)
phase = Slider(
    start=-6.4, end=6.4, value=0, step=0.1, title="Phase Shift (C)", bar_color="green"
)
offset = Slider(
    start=-9,
    end=9,
    value=0,
    step=0.1,
    title="Vertical Translation (D)",
    bar_color="green",
)

callback = CustomJS(
    args=dict(source=source, amp=amp, freq=freq, phase=phase, offset=offset),
    code="""
    const A = amp.value
    const k = freq.value
    const phi = phase.value
    const B = offset.value

    const x = source.data.x
    const y = Array.from(x, (x) => B + A*Math.sin(k*x+phi))


    source.data = { x, y }
""",
)

amp.js_on_change("value", callback)
freq.js_on_change("value", callback)
phase.js_on_change("value", callback)
offset.js_on_change("value", callback)

plot.xaxis.fixed_location = 0
plot.yaxis.fixed_location = 0

show(row(column(div, amp, freq, phase, offset), plot))
