import dash
from dash import html, dcc
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
import json
import sys
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
                  'Generate json file', id='train-download-button', type='primary', icon=fac.AntdIcon(icon='antd-cloud-download')
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
        Output(f"{name}-button", 'nClicks', allow_duplicate=True),
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
    # print('training data', data)
    return data



# @app.callback(
#     Output('training-value-setter-store', 'data'),
#     Output('train-layout-update-value-message', 'children'),
#     Input("model-button", 'nClicks'),
#     Input("train-button", 'nClicks'),
#     Input("system-button", 'nClicks'),
#     State("model-input", 'children'),
#     State("train-input", 'children'),
#     State("system-input", 'children'),
#     State('training-value-setter-store', 'data'),
# )
# def update_train_value(model_clicks, train_clicks, system_clicks,
#                        model_input, train_input, system_input,
#                        previous_data):
#     if model_clicks or train_clicks or system_clicks:
#         data = previous_data
#         if model_clicks:
#             print(model_input[:-1])
#             output_dict = getter_value(model_input[:-1])
#             if output_dict is not None:
#                 data['model'] = output_dict
#             else:
#                 return dash.no_update, fac.AntdMessage(content='Please enter the correct value!', type='error')
#         if train_clicks:
#             output_dict = getter_value(train_input[:-1])
#             if output_dict is not None:
#                 data['train'] = output_dict
#             else:
#                 return dash.no_update, fac.AntdMessage(content='Please enter the correct value!', type='error')
#         if system_clicks:
#             data['system'] = getter_value(system_input[:-1])
#         # print('training-value-setter-store', data)
#         return data, fac.AntdMessage(content='Update value Successfully', type='success')
#     else:
#         return dash.no_update, []


for name in ['model', 'train', 'system']:
    @app.callback(
        Output(f"{name}-button", 'nClicks'),
        Input('app-tabs', 'value')
    )
    def setter_nClicks(value):
        if value=='tab2':
            return None
        else:
            return dash.no_update


@app.callback(
    Output('train-download-json', 'data'),
    Input('train-download-button', 'nClicks'),
    State('training-value-setter-store', 'data'),
    prevent_initial_call=True,
)
def download_func(nClicks, data):
    data = json.dumps(data)
    return dict(content=str(data), filename="train_model.json")



