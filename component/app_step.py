import sys
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
sys.path.append("..")
from server import app
from component.app_train import train_layout
from component.app_sample import sample_common_layout
from component.app_graph import graph_layout
from .common_layout import card_style, card_style_hide

step_layout = html.Div([
    fac.AntdSteps(
        id='steps-demo',
        steps=[
            # {'title': f'Step 1: Model setting'},
            {'title': f'Step 1: Topology generate'},
            {'title': f'Step 2: Sample setting'},
        ],
        direction='horizontal',
        type='navigation',
        allowClick=True
    ),
    # html.Br(),
    # html.Div(id='step1', children=dbc.Container(train_layout), style=card_style_hide),
    html.Div(id='step1', children=graph_layout),
    html.Div(id='step2', children=dbc.Container(sample_common_layout)),
    fac.AntdDivider(isDashed=True),
    fac.AntdSpace([
        fac.AntdButton('Previous step', id='steps-demo-go-last', type='primary'),
        # fac.AntdDivider(id='step-divider', direction='vertical'),
        fac.AntdButton('Next step', id='steps-demo-go-next', type='primary')
    ]),

])



# ===================step swap callback========================
def check_node_data(data):
    empty_list = []
    if data['sample_constrain']['constrain_step_dict'] == {}:
        return ['0', '1']
    for node, v in data['sample_constrain']['constrain_step_dict'].items():
        if v['node add'] == {} and v['node conn'] == {}:
            empty_list.append(node)
    return empty_list

@app.callback(
    Output('steps-demo', 'current'),
    Output("graph-message", "children", allow_duplicate=True),
    Input('steps-demo-go-next', 'nClicks'),
    Input('steps-demo-go-last', 'nClicks'),
    State('steps-demo', 'current'),
    State('graph-value-setter-store', 'data'),
    prevent_initial_call=True
)
def steps_callback_demo_part1(go_next, go_last,  current, graph_data):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].startswith('steps-demo-go-next'):
        empty_list = check_node_data(graph_data)
        # return current + 1, []
        if (current==0) and (len(empty_list) > 0):
            return current, fac.AntdModal(f"Please set related constraints for nodes {empty_list}",
                                          title='Error', centered=True, visible=True)
        else:
            return current + 1, []
    elif ctx.triggered[0]['prop_id'].startswith('steps-demo-go-last'):
        return max(current - 1, 0), []
    else:
        return 0, []

#================check swap next step=================
for name in ['general', 'rl', 'sample-download']:
    @app.callback(
        Output(f"{name}-button", 'disabled'),
        Input('steps-demo', 'current'),
        Input('graph-value-setter-store', 'data'),
        prevent_initial_call=True
    )
    def steps_callback_demo_part1(current, graph_data):
        empty_list = check_node_data(graph_data)
        if (current==1) and (len(empty_list) > 0):
            return True
        else:
            return False

# ===================step swap layout callback========================
@app.callback(
    Output('step1', 'style'),
    Output('step2', 'style'),
    Input('steps-demo', 'current'),
    prevent_initial_call=True
)
def steps_callback_demo_part2(current):
    if current == 0:
        return card_style, card_style_hide
    else:
        return card_style_hide, card_style



##=====================click button nClicks=====================
for name in ['enter-value', 'general-constrain']:
    @app.callback(
        Output(f"{name}-button", 'nClicks'),
        Input('steps-demo', 'current'),
        Input('app-tabs', 'value'),
        )
    def setter_nClicks(value, tabs_value):
        if value!='0' or tabs_value=='tab1':
            return None
        else:
            return dash.no_update

for name in ['general', 'rl-button']:
    @app.callback(
        Output(f"{name}-button", 'nClicks'),
        Input('steps-demo', 'current'),
        Input('app-tabs', 'value'),
    )
    def setter_nClicks(value, tabs_value):
        if value!='1' or tabs_value=='tab1':
            return None
        else:
            return dash.no_update

##===================hide prevision button======================
@app.callback(
    Output('steps-demo-go-last', 'style'),
    Input('steps-demo', 'current'),
    prevent_initial_call=True
)
def steps_callback_demo_part2(current):
    if current == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

##=================hide next button=====================
@app.callback(
    Output('steps-demo-go-next', 'style'),
    Input('steps-demo', 'current'),
    prevent_initial_call=True
)
def steps_callback_demo_part2(current):
    if current == 1:
        return {'display': 'none'}
    else:
        return {'display': 'block'}
