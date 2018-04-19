# author: Don Fox
# date: July 7, 2017
# file name: canonical_dataset.py
#
# The purpose of this script is to create a CSV file that contains pertinent
# information gathered from various data sets.

import pandas as pd
import pickle

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar
from bokeh.palettes import Viridis256 as palette
from bokeh.plotting import figure, show

def create_plot():

	# Load tree census data set
	df = pd.read_csv('tree_data_by_ct_Jul-10.csv')
	df = df.rename(columns={'Unnamed: 0': 'Census Tract'})
	df.set_index(df['Census Tract'], inplace=True)

	# Load census tract lon/lat and area data
	with open('nyct.p', 'r') as f:
		ct_patches = pickle.load(f)

	# Plot data using bokeh
	color_mapper = LinearColorMapper(palette=palette, low=2E-7, high=2E-4)
	TOOLS = "pan, box_zoom, wheel_zoom, reset, hover, save"

	cts = df.index
	xs = [ct_patches[ct][0] for ct in cts]
	ys = [ct_patches[ct][1] for ct in cts]
	source = ColumnDataSource(
    	data=dict(x=xs, y=ys, cts=cts,
              	nta=df['nta'].values,
              	density=df['density'].values,
              	income=df['Median Income'].values))

	p = figure(title="Tree Density in New York City",
				tools=TOOLS,
           		x_axis_location=None,
           		y_axis_location=None)

	p.grid.grid_line_color = None

	p.patches('x', 'y', source=source,
          	fill_color={'field': 'density', 'transform': color_mapper},
          	fill_alpha=0.7, line_color="white", line_width=0.5)

	color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12,
                     	border_line_color=None, location=(20, 0))

	p.add_layout(color_bar, 'right')

	hover = p.select_one(HoverTool)
	hover.point_policy = "follow_mouse"
	hover.tooltips = [
    	("Census Tract", "@cts"),
    	("NTA", "@nta"),
    	("Median Income", "$@income"),
    	("Tree Density", "@density (count/sq-ft)"),
    	("(Long, Lat)", "($x, $y)")]

	return components(p)
