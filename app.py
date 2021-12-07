from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.transform import linear_cmap
import geopandas as gpd
import pandas as pd
import json
#Define function that returns json_data for year selected by user.

gdf = gpd.read_file("data\gdf.shp")
datafile = pd.read_csv("data\power.csv")

def json_data(selectedYear):
    yr = selectedYear
    df_yr = datafile[datafile['Year'] == yr]
    merged = gdf.merge(df_yr, left_on = 'country', right_on = 'Countries', how = 'left')
    merged.fillna('No data', inplace = True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data


    
#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data(2016))
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 390, high = 2000, nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels = {'400': '400', '600': '600', '800':'800', '1000':'1000', '1200':'1200', '1400':'1400', '1600':'1600','1800':'1800', '2000': '2000'}
#Add hover tool
hover = HoverTool(tooltips = [ ('Country/region','@Countries'),('% SolarPower', '@Values')])
#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

#Create figure object.
p = figure(title = 'Solar power of EU countries', plot_height = 1000 , plot_width = 800, toolbar_location = None, tools = [hover],  x_range=(-15, 35), y_range=(30, 85))
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'Values', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p.add_layout(color_bar, 'below')
# Define the callback function: update_plot

def update_plot(attr, old, new):
    yr = slider.value
    new_data = json_data(yr)
    geosource.geojson = new_data
    p.title.text = 'Solar power of EU countries, %d' %yr
    
# Make a slider object: slider 
slider = Slider(title = 'Year',start = 1986, end = 2015, step = 1, value = 2005)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)