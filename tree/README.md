## Visualize a sklearn Decision Tree Classifier
- simple tree   
  <img src="https://github.com/SauceCat/Nuance/blob/master/tree/image/simple_tree.gif" />    
- sankey tree  
  <img src="https://github.com/SauceCat/Nuance/blob/master/tree/image/sankey_tree.gif" />      

## How to use?
Take **simple_tree** as an example:
1. Download the folder [**tree**](https://github.com/SauceCat/Nuance/tree/master/tree)
2. The folder structure:
    ```
    tree
      - src: folder for all codes regarding the visualization
      - data: folder for the test data
      - simple_tree_output: folder for simple_tree outputs (will be re-generated if it was deleted)
      - sankey_tree_output: folder for sankey_tree outputs (will be re-generated if it was deleted)
      - generate_tree_test.ipynb: instructions and examples in jupyter notebook
      - ...
    ```
3. Install `jinja2`
    ```
    pip install jinja2
    ```
4. Use simple_tree or sankey_tree visualization: (visualization depends on D3.js, so you need to connect to the network)
    ```python
    import sys
    sys.path.insert(0, 'src/')
    import generate_tree
    
    # simple tree
    generate_tree.generate_simple_tree(tree_title='Titanic_Tree', tree_model=dt, X=titanic[features], 
                                   target_names=['Not Survived', 'Survived'], target_colors = None,
                                   color_map=None, width=1500, height=1000)
				   
    # sankey tree
    generate_tree.generate_sankey_tree(tree_title='Titanic_Tree', tree_model=dt, X=titanic[features], 
                                   target_names=['Not Survived', 'Survived'], target_colors = None,
                                   color_map=None, width=1500, height=1200)
    ```
5. A html file would be generated in [simple_tree_output](https://github.com/SauceCat/Nuance/tree/master/tree/simple_tree_output) or [sankey_tree_output](https://github.com/SauceCat/Nuance/tree/master/tree/sankey_tree_output) folder. Open it using any browser you like (I like Chrome anyway). 

## Parameters
```python
def generate_simple_tree(tree_title, tree_model, X, target_names, 
                         target_colors=None, color_map=None, width=None, height=None):
	'''
	visualize a sklearn Decision Tree Classifier

	:param tree_title: string
		name of the tree
	:param tree_model: a fitted sklearn Decision Tree Classifier
	:param X: pandas DataFrame
		dataset model was fitted on
	:param target_names: list
		list of names for targets
	:param target_colors: list, default=None
		list of colors for targets
	:param color_map: string, default=None
		matplotlib color map name, like 'Vega20'
	:param width: int
		width of the html page
	:param height: int
		height of the html page
	'''
	
def generate_sankey_tree(tree_title, tree_model, X, target_names,
			 target_colors=None, color_map=None, width=None, height=None):
	'''
	visualize a sklearn Decision Tree Classifier

	:param tree_title: string
		name of the tree
	:param tree_model: a fitted sklearn Decision Tree Classifier
	:param X: pandas DataFrame
		dataset model was fitted on
	:param target_names: list
		list of names for targets
	:param target_colors: list, default=None
		list of colors for targets
	:param color_map: string, default=None
		matplotlib color map name, like 'Vega20'
	:param width: int
		width of the html page
	:param height: int
		height of the html page
	'''
```
