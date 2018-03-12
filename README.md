# Nuance
I use Nuance to curate varied visualization thoughts during my data scientist career.   
It is not yet a package but a list of small ideas. Welcome to test them out!

## Why Nuance?
**nuance n.**  
a subtle difference in meaning or opinion or attitude 

## How to use?
Take **simple_tree** as an example:
1. Download the folder [**simple_tree**](https://github.com/SauceCat/Nuance/tree/master/tree/simple_tree)
2. The folder structure:
    ```
    simple_tree
      - src: folder for all codes regarding the visualization
      - data: folder for the test data
      - simple_tree_output: folder for outputs (will be re-generated if it was deleted)
      - simple_tree_test.ipynb: instructions and examples in jupyter notebook
    ```
3. Use simple_tree visualization:
    ```python
    import sys
    sys.path.insert(0, 'src/')
    import simple_tree
    
    simple_tree.generate_simple_tree(tree_title='Titanic_Tree', tree_model=dt, X=titanic[features], 
                                     target_names=['Not Survived', 'Survived'], target_colors = None,
                                     color_map=None, width=1500, height=1000)
    ```
    
## List of ideas
1. **simple tree**: visualize a sklearn Decision Tree  
    <img src="https://github.com/SauceCat/Nuance/blob/master/tree/image/simple_tree.gif" />      
2. **sankey tree**: visualize a sklearn Decision Tree  
    <img src="https://github.com/SauceCat/Nuance/blob/master/tree/image/sankey_tree.gif" />  
