import dash
from dash import html, dcc
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
import json
import sys
sys.path.append("..")
from server import app
from .common_layout import train_dict, model_input, train_input, system_input, getter_value

train_layout = fac.AntdSpace(
    id='train-layout',
    direction='vertical',
    children=[model_input,
              train_input,
              system_input,
              fac.AntdButton(
                  'Download Json File', id='train-download-button', type='primary', icon=fac.AntdIcon(icon='antd-cloud-download')
              ),
              html.Div(id='train-layout-update-value-message'),
              dcc.Store(id='training-value-setter-store', data=train_dict),
              dcc.Download(id='train-download-json'),
    ]
)

@app.callback(
    Output('training-value-setter-store', 'data'),
    Output('train-layout-update-value-message', 'children'),
    Input("model-button", 'nClicks'),
    Input("train-button", 'nClicks'),
    Input("system-button", 'nClicks'),
    State("model-input", 'children'),
    State("train-input", 'children'),
    State("system-input", 'children'),
    State('training-value-setter-store', 'data'),
)
def update_train_value(model_clicks, train_clicks, system_clicks,
                       model_input, train_input, system_input,
                       previous_data):
    if model_clicks or train_clicks or system_clicks:
        data = previous_data.copy()
        if model_clicks:
            data['model'] = getter_value(model_input[:-1])
        if train_clicks:
            data['train'] = getter_value(train_input[:-1])
        if system_clicks:
            data['system'] = getter_value(system_input[:-1])
        # print('training-value-setter-store', data)
        return data, fac.AntdMessage(content='Update value Successfully', type='success')
    else:
        return dash.no_update, []


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



