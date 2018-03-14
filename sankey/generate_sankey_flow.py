
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import json
import jinja2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def _get_node_names(df):
	node_infos = {}

	for col in df.columns.values:
	    col_values = sorted(df[col].unique())
	    col_names = []

	    for col_value in col_values:
	        node_name = '%s: %s' %(col, str(col_value))
	        col_names.append(node_name)

	    node_infos[col] = {'col_names': col_names, 'col_values': col_values}

	return node_infos


def _get_node_colors(node_infos, node_color_type, node_color_mapping, cm):
	node_colors = {}

	if node_color_type == 'col':
	    for col_idx, col in enumerate(node_infos.keys()):
	        col_color = cm(col_idx % 20)
	        for col_name in node_infos[col]['col_names']:
	            node_colors[col_name] = matplotlib.colors.rgb2hex(col_color)
	            
	if node_color_type == 'val':
	    unique_values = []
	    for col in node_infos.keys():
	        unique_values += list(node_infos[col]['col_values'])
	    unique_values = list(set(unique_values))
	    for col in node_infos.keys():
	        for col_value in node_infos[col]['col_values']:
	            val_idx = unique_values.index(col_value)
	            node_colors['%s: %s' %(col, str(col_value))] = matplotlib.colors.rgb2hex(cm(val_idx % 20))
	            
	if node_color_type == 'col_val':
	    node_names = []
	    for col in node_infos.keys():
	        node_names += node_infos[col]['col_names']
	    for node_name_idx, node_name in enumerate(node_names):
	        node_colors[node_name] = matplotlib.colors.rgb2hex(cm(node_name_idx % 20))
	        
	if node_color_type == 'cus':
	    for col in node_color_mapping.keys():
	        if type(node_color_mapping[col]) == dict:
	            for col_val in node_color_mapping[col].keys():
	                node_colors['%s: %s' %(col, str(col_val))] = node_color_mapping[col][col_val]
	        else:
	            for col_name in node_infos[col]['col_names']:
	                node_colors[col_name] = node_color_mapping[col]

	return node_colors


def _prepare_sankey_data(df, node_colors):
	links = []
	nodes = []
	for i in range(len(df.columns.values)-1):
	    source_col, target_col = df.columns.values[i], df.columns.values[i+1]
	    temp_df = df[[source_col, target_col]]
	    temp_df['count'] = 1
	    temp_df = temp_df.rename(columns={source_col: 'source', target_col: 'target'})
	    temp_df_gp = temp_df.groupby(['source', 'target'], as_index=False).count()
	    
	    temp_df_gp['source'] = temp_df_gp['source'].apply(lambda x : '%s: %s' %(source_col, str(x)))
	    temp_df_gp['target'] = temp_df_gp['target'].apply(lambda x : '%s: %s' %(target_col, str(x)))
	    
	    temp_df_gp['color_source'] = temp_df_gp['source'].apply(lambda x : node_colors[x] if x in node_colors.keys() else '#000')
	    temp_df_gp['color_target'] = temp_df_gp['target'].apply(lambda x : node_colors[x] if x in node_colors.keys() else '#000')
	    temp_df_gp['value'] = temp_df_gp['count'].map(str)
	    
	    links+= temp_df_gp[['source', 'target', 'value']].to_dict('records')

	nodes = [{'name': n, 'color': c} for (n, c) in node_colors.items()]
	data = {
	    'links': links,
	    'nodes': nodes
	}
	return data


def draw_sankey_flow(df, node_color_type, link_color_type, width, height, graph_name=None, node_color_mapping=None, color_map=None, link_color=None):
	# get node infos
	node_infos = _get_node_names(df)

	# get node colors
	if color_map is None:
		cm = plt.cm.get_cmap('Vega20')
	else:
		try:
			cm = plt.cm.get_cmap(color_map)
		except:
			cm = plt.cm.get_cmap('Vega20')

	node_colors = _get_node_colors(node_infos, node_color_type, node_color_mapping, cm)

	# prepare data for sankey
	sankey_data = _prepare_sankey_data(df, node_colors)

	# render the output
	temp = open('sankey_flow_template.html').read()
	template = jinja2.Template(temp)

	# generate output html
	if graph_name is None:
		output_path = 'sankey_flow_output.html'
	else:
		output_path = 'sankey_flow_output_%s.html' %(graph_name)
	with open(output_path, 'wb') as fh:
	    fh.write(template.render({'data': json.dumps(sankey_data), 'link_color_type': link_color_type, 'link_color': link_color, 
	                              'width': width, 'height': height}))
	    print('The output is in %s. Enjoy!' %(output_path))












