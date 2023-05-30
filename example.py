from bokeh.plotting import figure, show
import numpy as np
import sympy as sp

x_vals = np.arange(-10, 10)
y_vals = x_vals

fig = figure(
    title='Initial Graph', x_axis_label = "x axis", y_axis_label = 'y axis'
)

fig.line(x_vals, y_vals, legend_label = "Temp.", line_width=2)

show(fig) # type: ignore
