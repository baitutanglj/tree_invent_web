import json
import sys

import dash
import feffery_antd_components as fac
from dash import html, dcc
from dash.dependencies import Input, Output, State

sys.path.append("..")
from server import app
from .common_layout import train_dict, model_input, train_input, system_input, getter_value, success_message, error_message

train_layout = fac.AntdSpace(
    id='train-layout',
    direction='vertical',
    children=[model_input,
              train_input,
              system_input,
              fac.AntdButton(
                  'Generate json file for model setting', id='train-download-button', type='primary', icon=fac.AntdIcon(icon='antd-cloud-download')
              ),
              html.Div(id='train-layout-update-value-message'),
              dcc.Store(id='training-value-setter-store', data=train_dict),
              dcc.Download(id='train-download-json'),
    ]
)

for name in ['model', 'train', 'system']:
    @app.callback(
        Output(f"{name}-value-setter-store", 'data'),
        Output('train-layout-update-value-message', 'children', allow_duplicate=True),
        Output(f"{name}-button", 'nClicks'),
        Input(f"{name}-button", 'nClicks'),
        State(f"{name}-input", 'children'),
        prevent_initial_call=True
    )
    def update_train_layout_value(nClicks, input_data):
        if nClicks:
            output_dict = getter_value(input_data[:-2])
            if output_dict is not None:
                data = output_dict
                return data, success_message, 0
            else:
                return dash.no_update, error_message, 0
        else:
            return dash.no_update, [], 0


@app.callback(
    Output("training-value-setter-store", 'data', allow_duplicate=True),
    Input('model-value-setter-store', 'data'),
    Input('train-value-setter-store', 'data'),
    Input('system-value-setter-store', 'data'),
    State('training-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_training_layout_value(model_data, train_data, system_data, previous_data):
    data = previous_data
    data.update({'model': model_data})
    data.update({'train': train_data})
    data.update({'system': system_data})
    return data


@app.callback(
    Output('train-download-json', 'data'),
    Input('train-download-button', 'nClicks'),
    State('training-value-setter-store', 'data'),
    State('training-value-setter-store', 'data'),
    prevent_initial_call=True,
)
def download_func(nClicks, data):
    data = json.dumps(data)
    return dict(content=str(data), filename="train_model.json")


# @app.callback(
#     Output('sample-value-setter-store', 'data', allow_duplicate=True),
#     Input('training-value-setter-store', 'data'),
#     State('sample-value-setter-store', 'data'),
#     prevent_initial_call=True
# )
# def update_graph_value(train_data, previous_data):
#     data = previous_data
#     data.update(train_data)
#     data['train'] = {'prior': train_data['train']['model_save_path'],
#                      'batchsize': train_data['train']['batchsize'],
#                      'initlr': train_data['train']['initlr']}
#     return data

for name in ['model', 'train', 'system']:
    @app.callback(
        Output(f"{name}-button", 'nClicks', allow_duplicate=True),
        Input('app-tabs', 'value'),
        prevent_initial_call=True
        )
    def setter_nClicks(value):
        if value=='tab2':
            return None
        else:
            return dash.no_update