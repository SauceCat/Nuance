## Visualize a sankey flow
<table>
<tr>
    <td><img src="https://github.com/SauceCat/Nuance/blob/master/sankey/images/sankey_flow_tab20.PNG" /></td>
    <td><img src="https://github.com/SauceCat/Nuance/blob/master/sankey/images/sankey_flow_same.PNG" /></td>
</tr>
<tr>
    <td><img src="https://github.com/SauceCat/Nuance/blob/master/sankey/images/sankey_flow_val.PNG" /></td>
    <td><img src="https://github.com/SauceCat/Nuance/blob/master/sankey/images/sankey_flow_col_val.PNG" /></td>
</tr>
</table>

## How to use?
1. Download the folder [**sankey**](https://github.com/SauceCat/Nuance/tree/master/sankey)
2. The folder structure:
    ```
    sankey
      - src: folder for all codes regarding the visualization
      - data: folder for the test data
      - sankey_flow_output: folder for outputs (will be re-generated if it was deleted)
      - sankey_flow_test.ipynb: instructions and examples in jupyter notebook
      - ...
    ```
3. Install `jinja2`
    ```
    pip install jinja2
    ```
4. Use sankey_flow visualization: (visualization depends on D3.js, so you need to connect to the network)
    ```python
    import sys
    sys.path.insert(0, 'src/')
    import generate_sankey_flow
    
    generate_sankey_flow.draw_sankey_flow(df=raw[use_cols], node_color_type='col', link_color_type='source', 
                                          width=1600, height=900, graph_name='Titanic', 
                                          node_color_mapping=None, color_map=None, link_color=None)
    ```
5. A html file would be generated in [sankey_flow_output](https://github.com/SauceCat/Nuance/tree/master/sankey/sankey_flow_output). Open it using any browser you like (I like Chrome anyway). 

## Parameters
```python
def draw_sankey_flow(df, node_color_type, link_color_type, width, height, 
                     graph_name=None, node_color_mapping=None, color_map=None, link_color=None):
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
```
