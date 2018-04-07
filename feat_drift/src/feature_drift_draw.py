
import pandas as pd
import jinja2
import os


def _process_imp(imp_df, imp_name):
    """
    Preprocessing on the input feature importance dataframe

    :param imp_df: feature importance pandas dataframe
    :param imp_name: column name of the importance value
    :return:
        dataframe with relative_imp and feat_rank
    """

    imp_df = imp_df.sort_values(by=imp_name, ascending=False).reset_index(drop=True)
    imp_df['relative_imp'] = imp_df[imp_name] * 1.0 / imp_df[imp_name].max()
    imp_df['relative_imp'] = imp_df['relative_imp'].apply(lambda x : round(x, 3))
    imp_df['feat_rank'] = imp_df.index.values + 1
    return imp_df


def _rank2color(x, color_dict):
    """
    Map change of rank to color

    :param x: row of dataframe
    :param color_dict: color dictionary
    """

    if x['feat_rank_x'] < x['feat_rank_y']:
        return color_dict['drop']
    if x['feat_rank_x'] >= x['feat_rank_y']:
        return color_dict['up_or_stable']
    if pd.isnull(x['feat_rank_y']):
        return color_dict['disappear']
    if pd.isnull(x['feat_rank_x']):
        return color_dict['appear']
    

def _get_mark(x):
    """
    '1' for feature appears on both feature importance dataframes
    '0' for feature disappears on either dataframe
    """
    if pd.isnull(x['feat_rank_y']) or pd.isnull(x['feat_rank_x']):
        return "0"
    else:
        return "1"
    

def _merge_feat_imp(imp_df1, imp_df2, feature_name, top_n, color_dict):
    """
    Merge and compare two feature importance dataframes

    :param imp_df1: feature importance dataframe #1
    :param imp_df2: feature importance dataframe #2
    :param feature_name: column name of features
    :param top_n: show top_n features
    :param color_dict: color dictionary
    :return:
        The merged dataframe
    """

    imp_df1['pos'] = 'left'
    imp_df2['pos'] = 'right'
    if top_n:
        both_imp = imp_df1.head(top_n).merge(imp_df2.head(top_n), on=feature_name, how='outer')
    else:
        both_imp = imp_df1.merge(imp_df2, on=feature_name, how='outer')
        
    both_imp['bar_color'] = both_imp.apply(lambda x : _rank2color(x, color_dict), axis=1)
    both_imp['bar_mark'] = both_imp.apply(lambda x : _get_mark(x), axis=1)
    
    return both_imp


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

    feat_imp1 = _process_imp(feat_imp1, imp_name)
    feat_imp2 = _process_imp(feat_imp2, imp_name)
    
    if color_dict is None:
        color_dict = {
            'drop': '#f17182',
            'up_or_stable': '#abdda4',
            'disappear': '#bababa',
            'appear': '#9ac6df'
        }
    
    both_imp = _merge_feat_imp(feat_imp1, feat_imp2, feature_name, top_n, color_dict)
    
    bar_left_data = both_imp[['feat_name', 'relative_imp_x', 'pos_x', 'bar_color', 'bar_mark']
                            ].dropna().sort_values('relative_imp_x', ascending=False)
    bar_left_data.columns = [col.replace('_x', '') for col in bar_left_data.columns.values]

    bar_right_data = both_imp[['feat_name', 'relative_imp_y', 'pos_y', 'bar_color', 'bar_mark']
                             ].dropna().sort_values('relative_imp_y', ascending=False)
    bar_right_data.columns = [col.replace('_y', '') for col in bar_right_data.columns.values]

    line_data = both_imp[['feat_name', 'bar_color', 'feat_rank_x', 'feat_rank_y']].dropna()[['feat_name', 'bar_color']]
    
    legend_data = [
        {'name': 'Drop', 'color': color_dict['drop']},
        {'name': 'Up & Stable', 'color': color_dict['up_or_stable']},
        {'name': 'Disappear', 'color': color_dict['disappear']},
        {'name': 'Appear', 'color': color_dict['appear']}
    ]
    
    # render the output
    temp = open('src/feature_drift_template.html').read()
    template = jinja2.Template(temp)

    # create the output root if it is not exits
    if not os.path.exists('feature_drift_output'):
        os.mkdir('feature_drift_output')

    # generate output html
    if graph_name is None:
        output_path = 'feature_drift_output/feature_drift_output.html'
    else:
        output_path = 'feature_drift_output/feature_drift_%s.html' %graph_name

    with open(output_path, 'wb') as fh:
        fh.write(template.render({'bar_left_data': bar_left_data.to_dict('records'), 
                                  'bar_right_data': bar_right_data.to_dict('records'), 
                                  'line_data': line_data.to_dict('records'), 
                                  'legend_data': legend_data, 
                                  'max_bar_width': max_bar_width, 'bar_height': bar_height, 
                                  'middle_gap': middle_gap, 'fontsize': fontsize,
                                  'ds_name1': ds_name1, 'ds_name2': ds_name2}))
