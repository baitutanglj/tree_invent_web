import json
import sys

import dash
import dash_bio as dashbio
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import feffery_antd_components as fac
from dash import html, dcc
from dash.dependencies import Input, Output, State

sys.path.append("..")
from server import app
from .app_dropdown import dropdown_card
from .common_layout import card_style, form_style, number_style, getter_value, sample_constrain_dict

stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    },
    {
        "selector": "node:selected",
        "style": {
            "border-width": "6px",
            "border-color": "#AAD8FF",
            "border-opacity": "0.5",
            "background-color": "#77828C",
            "text-outline-color": "#77828C"
        }
    },
    {
        "selector": "edge:selected",
        "style": {
            'line-color': '#77828C'
        }
    },

]


nodes = [
    {"data": {"id": "0", "label": "0", 'node add': {},  'node conn': {}}},
    {"data": {"id": "1", "label": "1", 'node add': {}, 'node conn': {'constrain_connect_node_id': [0]}}},
]
edges = [
    {"data": {"index": '0', "source": '0', "target": '1'}}
]

elements = nodes + edges

graph = cyto.Cytoscape(
    id='cytoscape-elements-callbacks',
    layout={'name': 'cose'},
    stylesheet=stylesheet,
    style={'width': '100%', 'height': '450px'},
    elements=elements,
    minZoom=0.5,
    maxZoom=2
)

graph_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Click the 'Add node' or 'Del node' button to to add or remove node in graph")),
        dbc.CardBody(dbc.Col(graph)
                     ),
        dbc.CardFooter(
            dbc.Row([
                dbc.Col(dbc.Button('Add Node', id='btn-add-node', n_clicks_timestamp=0, className="me-2", active=True),
                        md=3),
                dbc.Col(
                    dbc.Button('Del Node', id='btn-remove-node', n_clicks_timestamp=0, className="me-2", active=False),
                    md=3),
                dbc.Col(dbc.Button('Add Edge', id='btn-add-edge', n_clicks_timestamp=0, className="me-2", active=True),
                        md=3),
                dbc.Col(
                    dbc.Button('Del Edge', id='btn-remove-edge', n_clicks_timestamp=0, className="me-2", active=False),
                    md=3),
            ]),
        ),
    ],
    style={"width": "45rem"}
)

graph_data_card = fac.AntdSpace([
    fac.AntdCollapse(
        id='cytoscape-tapNodeData-json',
        title='constrain that have been added the current node',
        children='No node is selected',
        style={
            'width': 700,
            'marginBottom': 10,
            'display': 'block'
        },
        # style=card_style

    ),
    # fac.AntdCollapse(
    #     id='cytoscape-tapEdgeData-json',
    #     title='TapEdgeData',
    #     children='No edge is selected',
    #     style=card_style
    # ),
])

general_constrain_layout = fac.AntdCollapse(
    title='general constrain',
    isOpen=True,
    style=card_style,
    children=fac.AntdForm(
        id='general-constrain-input',
        children=[
            fac.AntdFormItem(fac.AntdInputNumber(value=5, style=number_style), label="max_node_steps"),
            fac.AntdFormItem(fac.AntdInputNumber(value=100, style=number_style), label="max_ring_nodes"),
            fac.AntdFormItem(fac.AntdInputNumber(value=1.0, style=number_style), label="temp"),
            fac.AntdFormItem(fac.AntdRadioGroup(
                options=[{'label': i, 'value': i} for i in ['easy', 'only ring', 'strict']],
                defaultValue='easy'
            ),
                label='ring_check_mode'),
            fac.AntdButton('Update value', id='general-constrain-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle'))
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

##=======================jsme layout==============================
jsme_layout = dashbio.Jsme(
    id='jsme-graph',
    options='query useOCLidCode exportInChIauxInfo exportInChIkey '
            'exportInChI exportSVG searchInChIkey useOpenChemLib paste rButton',
    height='450px', width='100%'
)

jsme_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Draw a molecule and click Button to submit"), close_button=True),
                dbc.ModalBody(jsme_layout),
                dbc.ModalFooter(
                    [
                        html.P(['Please click',
                                fac.AntdAvatar(mode='image', shape='square', src='/assets/imgs/jsme.png'),
                                'button and click the close button to mark the connected site for the molecule']),
                        dbc.Button("submit", id="jsme-button", className="ms-auto", n_clicks=0)
                    ]
                ),
            ],
            id="jsme-modal",
            size="lg",
            centered=True,
            is_open=False,
        ),
    ]
)

graph_layout = dbc.Container(
    fac.AntdSpace(
        id='graph-layout',
        direction='vertical',
        style={'width': '100%'},
        children=[
            fac.AntdSpace([graph_card,
                           fac.AntdSpace(
                               [dropdown_card, graph_data_card],
                               direction='vertical'
                           )
                           ]),

            jsme_modal,
            # graph_data_card,
            general_constrain_layout,
            fac.AntdButton(
                'Download Json File', id='graph-download-button', type='primary',
                icon=fac.AntdIcon(icon='antd-cloud-download')
            ),
            dcc.Download(id='graph-download-json'),
            html.Div(id='graph-message'),
            dcc.Store(id='graph-value-setter-store', data=sample_constrain_dict),
        ]
    )
)


##=========================general_constrain_layout callback================================
@app.callback(
    Output('graph-value-setter-store', 'data', allow_duplicate=True),
    Output("graph-message", "children", allow_duplicate=True),
    Input("general-constrain-button", 'nClicks'),
    State("general-constrain-input", 'children'),
    State('graph-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_train_value(nClicks, input_data, previous_data):
    data = previous_data
    if nClicks:
        data["sample_constrain"].update(getter_value(input_data[:-1]))
        # print('general_constrain_layout callback', data)
        return data, fac.AntdMessage(content='Update node attribute successfully', type='success')
    else:
        return dash.no_update, []


##======================graph json download============================
def check_node_data(data):
    empty_list = []
    for node, v in data['sample_constrain']['constrain_step_dict'].items():
        if v['node add'] == {} and v['node conn'] == {}:
            empty_list.append(node)
    return empty_list


@app.callback(
    Output('graph-download-json', 'data'),
    Output("graph-message", "children", allow_duplicate=True),
    Input('graph-download-button', 'nClicks'),
    State('graph-value-setter-store', 'data'),
    prevent_initial_call=True,
)
def download_func(nClicks, data):
    empty_list = check_node_data(data)
    if len(empty_list)>0:
        return dash.no_update, fac.AntdModal(f"Please set related constraints for node {empty_list}",
                                             title='Download constrain json file Error', centered=True, visible=True)
    else:
        data = json.dumps(data)
        return dict(content=str(data), filename="sample_constrain.json"), []
