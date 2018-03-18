
import matplotlib
import matplotlib.pyplot as plt

import json
import jinja2
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def _get_node_names(df):
	'''
	:param df: pandas DataFrame, each column represents a state
	:return:
		dictionary of (column name, column unique value list)
		which means (state name, unique values in this state)
	'''

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
	'''
	:param node_infos:
		dictionary of (state name, unique values in this state)
	:param node_color_type:
		node coloring strategy, can be one of ['col', 'val', 'col_val', 'cus']
		- 'col': each column has different color
		- 'val': each unique value has different color (unique values through all columns)
		- 'col_val': each unique value in each column has different color
		- 'cus': customer provide node color mapping
	:param node_color_mapping:
		if node_color_type == 'cus', node_color_mapping should't be None
	:param cm: matplotlib color map
	:return:
		dictionary of (node name, node color)
	'''

	node_colors = {}

	if (node_color_type == 'col') or (node_color_type == 'cus' and node_color_mapping['type'] == 'col'):
		for col_idx, col in enumerate(node_infos.keys()):
			if node_color_type == 'cus':
				col_color = node_color_mapping['mapping'][col]
			else:
				col_color = cm(col_idx % 20)
			for col_name in node_infos[col]['col_names']:
				node_colors[col_name] = matplotlib.colors.rgb2hex(col_color)

	if (node_color_type == 'val') or (node_color_type == 'cus' and node_color_mapping['type'] == 'val'):
		unique_values = []
		for col in node_infos.keys():
			unique_values += list(node_infos[col]['col_values'])
		unique_values = list(set(unique_values))

		for col in node_infos.keys():
			for col_value in node_infos[col]['col_values']:
				if node_color_type == 'cus':
					val_color = node_color_mapping['mapping'][col_value]
				else:
					val_idx = unique_values.index(col_value)
					val_color = matplotlib.colors.rgb2hex(cm(val_idx % 20))
				node_colors['%s: %s' %(col, str(col_value))] = val_color

	if (node_color_type == 'col_val') or (node_color_type == 'cus' and node_color_mapping['type'] == 'col_val'):
		for col_idx, col in enumerate(node_infos.keys()):
			if node_color_type == 'cus':
				for col_value in node_color_mapping['mapping'][col]:
					node_colors['%s: %s' % (col, str(col_value))] = node_color_mapping['mapping'][col][col_value]
			else:
				for col_name_idx, col_name in enumerate(node_infos[col]['col_names']):
					col_name_idx_true = col_idx * len(node_infos[col]['col_names']) + col_name_idx
					node_colors[col_name] = matplotlib.colors.rgb2hex(cm(col_name_idx_true % 20))

	return node_colors


def _prepare_sankey_data(df, node_colors):
	'''
	:param df: pandas DataFrame, each column represents a state
	:param node_colors: dictionary of (node name, node color)
	:return:
		dictionary of links and nodes
	'''

	links = []
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


def draw_sankey_flow(df, node_color_type, link_color_type, width, height, graph_name=None,
					 node_color_mapping=None, color_map=None, link_color=None):
	'''
	:param df:
		pandas DataFrame, each column represents a state
	:param node_color_type:
		node coloring strategy, can be one of ['col', 'val', 'col_val', 'cus']
			- 'col': each column has different color
			- 'val': each unique value has different color (unique values through all columns)
			- 'col_val': each unique value in each column has different color
			- 'cus': customer provide node color mapping
	:param link_color_type:
		link coloring strategy, default='source'
		Can be one of ['source', 'target', 'both', 'same']
			- 'source': same color as the source node
			- 'target': same color as the target node
			- 'both': color from both target and source
			- 'same': all links have same color
	:param width: wdith
	:param height: height
	:param graph_name: name of the graph
	:param node_color_mapping:
		if node_color_type == 'cus', color_mapping should be provided
		example:
		node_color_mapping = {
			'type': 'col',
			'mapping': {
				column1: color1, column2: color2, ...
			}
		}
	:param color_map: matplotlib color map
	:param link_color:
		if link_color_type == 'same', link color should be provided
	'''

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
	temp = open('src/sankey_flow_template.html').read()
	template = jinja2.Template(temp)

	# create the output root if it is not exits
	if not os.path.exists('sankey_flow_output'):
		os.mkdir('sankey_flow_output')

	# generate output html
	if graph_name is None:
		output_path = 'sankey_flow_output/sankey_flow_output.html'
	else:
		output_path = 'sankey_flow_output/sankey_flow_%s.html' %(graph_name)
	with open(output_path, 'wb') as fh:
		fh.write(template.render({'data': json.dumps(sankey_data), 'link_color_type': link_color_type,
								  'link_color': link_color, 'width': width, 'height': height}))
	print('The output is in %s. Enjoy!' %(output_path))
