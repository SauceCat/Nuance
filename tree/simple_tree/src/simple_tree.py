
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

import copy
import sys

import json
import jinja2


def _get_tree_info(X, tree_model, target_names, target_colors, tree_title, color_map):
	# classify features into 3 types: binary, float and int
	binary_features = []
	for col in X.columns.values:
		if list(sorted(np.unique(X[col].values))) == [0, 1]:
			binary_features.append(col)

	int_features = []
	for col in list(set(X.columns.values) - set(binary_features)):
		if list(X[col].map(int).values) == list(X[col].values):
			int_features.append(col)

	# get feature names
	feature_names = X.columns.values

	# check target names
	if type(target_names) != list or len(target_names) != tree_model.tree_.n_classes:
		raise ValueError("target_names should be a list of length %d." % (tree_model.tree_.n_classes))

	# color mapping for targets
	if target_colors is None:
		if color_map is not None:
			cm = plt.get_cmap(color_map)
		else:
			cm = plt.get_cmap('Vega20')
		target_colors = []
		for n in range(tree_model.tree_.n_classes):
			target_colors.append(str(matplotlib.colors.rgb2hex(cm(n + 1))))

	tree_info = {
		'tree_model': tree_model,
		'features': [feature_names[i] for i in tree_model.tree_.feature],
		'tree_title': tree_title,
		'binary_features': binary_features,
		'int_features': int_features,
		'target_names': target_names,
		'target_colors': target_colors
	}
	return tree_info


def _parse_tree(node_id, parent, pos, tree_info):
	tree_model = tree_info['tree_model']
	features = tree_info['features']
	tree_title = tree_info['tree_title']
	binary_features = tree_info['binary_features']
	int_features = tree_info['int_features']
	target_names = tree_info['target_names']

	node = {}
	if parent == 'null':
		node['name'] = tree_title
	else:
		feature = features[parent]
		if pos == 'left':
			if feature in binary_features:
				node['name'] = feature + ': 0'
			elif feature in int_features:
				node['name'] = feature + " <= " + str(int(tree_model.tree_.threshold[parent]))
			else:
				node['name'] = feature + " <= " + str(round(tree_model.tree_.threshold[parent], 3))
		else:
			if feature in binary_features:
				node['name'] = feature + ': 1'
			elif feature in int_features:
				node['name'] = feature + " > " + str(int(tree_model.tree_.threshold[parent]))
			else:
				node['name'] = feature + " > " + str(round(tree_model.tree_.threshold[parent], 3))
	try:
		node['parent'] = int(parent)
	except:
		node['parent'] = parent

	node['self'] = int(node_id)
	node['sample'] = int(tree_model.tree_.n_node_samples[node_id])
	node['impurity'] = round(tree_model.tree_.impurity[node_id], 3)
	node['value'] = [int(v) for v in tree_model.tree_.value[node_id][0]]
	node['predict'] = target_names[np.argmax(node['value'])]
	node['color'] = tree_info['target_colors'][np.argmax(node['value'])]

	if tree_model.tree_.children_left[node_id] != -1 or tree_model.tree_.children_right[node_id] != -1:
		node['children'] = []
		if tree_model.tree_.children_left[node_id] != -1:
			child = tree_model.tree_.children_left[node_id]
			node['children'].append(_parse_tree(child, node_id, 'left', tree_info))
		if tree_model.tree_.children_right[node_id] != -1:
			child = tree_model.tree_.children_right[node_id]
			node['children'].append(_parse_tree(child, node_id, 'right', tree_info))
	return node


def _extract_rules(node_id, parent, pos, tree_rules, tree_info):
	features = tree_info['features']
	tree_model = tree_info['tree_model']

	tree_rules[node_id] = {}
	tree_rules[node_id]['features'] = {}

	if parent != "null":
		previous = copy.deepcopy(tree_rules[parent]['features'])
		tree_rules[node_id]['features'] = previous
		feat = features[parent]
		thre = tree_model.tree_.threshold[parent]
		if feat not in previous.keys():
			tree_rules[node_id]['features'][feat] = [-sys.maxint, sys.maxint]
		if pos == "left":
			origin = tree_rules[node_id]['features'][feat][1]
			tree_rules[node_id]['features'][feat][1] = np.min([thre, origin])
		if pos == "right":
			origin = tree_rules[node_id]['features'][feat][0]
			tree_rules[node_id]['features'][feat][0] = np.max([thre, origin])

	if tree_model.tree_.children_left[node_id] != -1:
		child = tree_model.tree_.children_left[node_id]
		_extract_rules(child, node_id, "left", tree_rules, tree_info)

	if tree_model.tree_.children_right[node_id] != -1:
		child = tree_model.tree_.children_right[node_id]
		_extract_rules(child, node_id, "right", tree_rules, tree_info)

	return tree_rules


def _clean_rules(tree_rules, tree_info):
	tree_rules_clean = {}
	for key in tree_rules.keys():
		key = int(key)
		node = copy.deepcopy(tree_rules[key])
		rules = []
		if node['features'].keys():
			for k in node['features'].keys():
				feat = node['features'][k]
				if k in tree_info['binary_features']:
					if feat[0] == -sys.maxint:
						rule = k + ': 0'
					else:
						rule = k + ': 1'
				elif k in tree_info['int_features']:
					if feat[0] == -sys.maxint:
						rule = k + ' <= ' + str(int(feat[1]))
					elif feat[1] == sys.maxint:
						rule = k + ' > ' + str(int(feat[0]))
					else:
						rule = str(int(feat[0])) + ' < ' + k + ' <= ' + str(int(feat[1]))
				else:
					if feat[0] == -sys.maxint:
						rule = k + ' <= ' + str(round(feat[1], 3))
					elif feat[1] == sys.maxint:
						rule = k + ' > ' + str(round(feat[0], 3))
					else:
						rule = str(round(feat[0], 3)) + ' < ' + k + ' <= ' + str(round(feat[1], 3))
				rules.append(rule)
			rules = sorted(rules, key= lambda x : len(x))
		tree_rules_clean[key] = rules
	return tree_rules_clean


def generate_simple_tree(tree_title, tree_model, X, target_names,
						 target_colors=None, color_map=None, width=None, height=None):

	# get tree information
	tree_info = _get_tree_info(X, tree_model, target_names, target_colors, tree_title, color_map)

	# get the tree structure
	final_tree = _parse_tree(0, "null", "null", tree_info)

	# extract tree rules
	tree_rules = {}
	tree_rules = _extract_rules(0, "null", "null", tree_rules, tree_info)

	# clean up rules
	tree_rules_clean = _clean_rules(tree_rules, tree_info)

	# get template
	temp = open('src/simple_tree_template.html').read()
	template = jinja2.Template(temp)

	# generate output html
	with open('simple_tree_%s.html' %(tree_title), 'wb') as fh:
		render_result = {
			'tree': json.dumps(final_tree), 'rule': json.dumps(tree_rules_clean),
			'num_node': tree_info['tree_model'].tree_.capacity,
			'tree_depth': tree_info['tree_model'].tree_.max_depth,
			'width': width, 'height': height
		}
		fh.write(template.render(render_result))
	fh.close()
