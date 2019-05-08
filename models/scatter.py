from bokeh.plotting import figure
from bokeh.embed import components

def get_data():
    plot = figure(sizing_mode="scale_width", tools="")
    plot.circle([1,2], [3,4])

    return components(plot)