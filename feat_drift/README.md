## Visualize feature drift
<img src="https://github.com/SauceCat/Nuance/blob/master/feat_drift/images/feat_drift.gif"/>       

## How to use?
1. Download the folder [**feat_drift**](https://github.com/SauceCat/Nuance/tree/master/feat_drift)
2. The folder structure:
    ```
    feat_drift
      - src: folder for all codes regarding the visualization
      - data: folder for the test data
      - feature_drift_output: folder for outputs (will be re-generated if it was deleted)
      - feat_drift_test.ipynb: instructions and examples in jupyter notebook
      - ...
    ```
3. Install `jinja2`
    ```
    pip install jinja2
    ```
4. Use feature drift visualization: (visualization depends on D3.js, so you need to connect to the network)
    ```python
    import sys
    sys.path.insert(0, 'src/')
    import feature_drift_draw
    
    feature_drift_draw.feature_drift_graph(feat_imp1=feat_imp1, feat_imp2=feat_imp2, feature_name='feat_name', imp_name='imp',
                                           ds_name1='training set', ds_name2='test set', graph_name='train_test',
                                           top_n=20, max_bar_width=300, bar_height=30, middle_gap=300, fontsize=12, color_dict=None)
    ```
5. A html file would be generated in [feature_drift_output](https://github.com/SauceCat/Nuance/tree/master/feat_drift/feature_drift_output) or [sankey_tree_output](https://github.com/SauceCat/Nuance/tree/master/tree/sankey_tree_output) folder. Open it using any browser you like (I like Chrome anyway). 

## Parameters
```python
def feature_drift_graph(feat_imp1, feat_imp2, feature_name, imp_name, ds_name1, ds_name2, graph_name=None,
                        top_n=None, max_bar_width=300, bar_height=30, middle_gap=300, fontsize=12, color_dict=None):
    """
    Draw feature drift graph

    :param feat_imp1: feature importance dataframe #1
    :param feat_imp2: feature importance dataframe #2
    :param feature_name: column name of features
    :param imp_name: column name of importance value
    :param ds_name1: name of dataset #1
    :param ds_name2: name of dataset #2
    :param top_n: show top_n features
    :param max_bar_width: maximum bar width
    :param bar_height: bar height
    :param middle_gap: gap between bars
    :param fontsize: font size
    :param color_dict: color dictionary
    """
```
