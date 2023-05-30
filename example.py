from bokeh.plotting import figure, show
from bokeh.io import curdoc
import numpy as np
import sympy as sp

'''
    Built in themes to choose from are
    "caliber", "dark_minimal", "light_minimal", "night_sky", "contrast"
'''

curdoc().theme = "dark_minimal"
x_vals = np.arange(-10, 10)
y_vals = x_vals

'''
    #1. Setting the width and height
    #2. Responsive plot sizing
    #3. Setting axes' appearance
    #4. Axis Ranges
    #5. Positioning the axis

'''


fig = figure(
    title="Initial Graph",
    width=350,                      #1
    height=250,                     #1
    sizing_mode = 'stretch_width',  #2
    y_range=(-10, -10),             #4

)

fig.xaxis.axis_label = "X values"   #3
fig.xaxis.axis_line_width = 1       #3
fig.xaxis.axis_line_color = "red"   #3

fig.axis[0].fixed_location = 0      #5
fig.axis[1].fixed_location = 0      #5


fig.line(x_vals, y_vals, legend_label="Temp.", line_width=2)

show(fig)  # type: ignore
