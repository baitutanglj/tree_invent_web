from dash import html, dcc
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
import sys
sys.path.append("..")
from server import app


params = ["train", "rl", "docking", "sample_constrain"]


def build_value_setter_line(line_num, label, value, col3):
    return html.Div(
        id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(value, className="four columns"),
            html.Div(col3, className="four columns"),
        ],
        className="row",
    )


tab2 = html.Div(
    id='app-tab2',
    children=[
        fac.AntdSpace([
            fac.AntdSpace(
                id="metric-select-menu",
                align='start',
                size="large",
                children=[
                    html.Div(
                        style={'width': '300px'},
                        children=[
                        fac.AntdDivider(id="component-select", children="Select Component", innerTextOrientation='left'),
                        dcc.Dropdown(
                            id="component-select-dropdown",
                            options=list(
                                {"label": param, "value": param} for param in params
                            ),
                            value=params[0],
                        ),
                    ]),
                    html.Div(
                        children=[
                            fac.AntdDivider("Component Value Setter",),
                            fac.AntdSpace(id="component-value-setter",
                                          direction="vertical")
                    ]),
                ],
            ),
            dbc.Button("update value", id="update-value", color="primary", style={"margin": "10px"}),
            fac.AntdDivider(children="Export", innerTextOrientation='left'),
            dbc.Button("Export Json", id="export-json-all", color="primary", style={"margin": "10px"}),
        ],
        direction="vertical"),

    ],
)



input_style = {"width":500}

train_input = fac.AntdForm(
    id="train_input",
    children=[
        fac.AntdFormItem(fac.AntdInputNumber(value=1000), label='batchsize'),
        fac.AntdFormItem(fac.AntdInputNumber(value=1000), label='epochs'),
        fac.AntdFormItem(fac.AntdInputNumber(value=0.0001, step=0.0001), label='initlr'),
        fac.AntdFormItem(fac.AntdInput(value='./datasets'), label='dataset_path'),
    ],
    labelAlign='left',
    labelCol={'span':6},
    wrapperCol={'span':20},
    style={'width': '400px','margin': '0 auto'}
)


rl_input = fac.AntdForm(
    id='rl_input',
    children=[
        fac.AntdSpace([
        fac.AntdInput(addonBefore='score_components', value="['dockscore']", style=input_style),
        fac.AntdInput(addonBefore='score_weights', value='[1]', style=input_style),
        fac.AntdInput(addonBefore='target_smiles', value="['CO[C@H](C)[C@H](O)CC1CCOCC1']", style=input_style),
        fac.AntdInput(addonBefore='score_type', value='continuous', style=input_style),
        fac.AntdInput(addonBefore='qsar_models_path', value='./qsar.pkl', style=input_style),
        fac.AntdInputNumber(addonBefore='max_gen_atoms', value=38, style=input_style),
        fac.AntdInput(addonBefore='score_thresholds', value='[1.0]', style=input_style),
        fac.AntdInputNumber(addonBefore='tanimoto_k', value=0.7, style=input_style),
        fac.AntdInputNumber(addonBefore='sigma', value=50, style=input_style),
        fac.AntdInputNumber(addonBefore='vsigma', value=1.5, style=input_style),
        fac.AntdInputNumber(addonBefore='ksigma', value=1.5, style=input_style),
        fac.AntdInputNumber(addonBefore='acc_steps', value=1, style=input_style),
        fac.AntdInput(addonBefore='target_molfile', value='', style=input_style),
        fac.AntdInput(addonBefore='temperature_range', value='(1.0,1.2)', style=input_style),
        fac.AntdInput(addonBefore='temperature_scheduler', value="same", style=input_style),
        fac.AntdInput(addonBefore='unknown_fielter', value='False', style=input_style),
        fac.AntdInput(addonBefore='save_pic', value='True', style=input_style),
        ], direction="vertical")

    ]
)

docking_input = fac.AntdForm(
    id='docking_input',
    children=[
        fac.AntdSpace([
            fac.AntdInput(addonBefore='dock_input_path', value="./Tree_Invent/scripts/3CLPro/7RFS", style=input_style),
            fac.AntdInput(addonBefore='backend', value='Glide', style=input_style),
            fac.AntdInputNumber(addonBefore='low_threshold', value=-9.0, style=input_style),
            fac.AntdInputNumber(addonBefore='high_threshold', value=-4.0, style=input_style),
            fac.AntdInputNumber(addonBefore='k', value=-4.0, style=input_style),
            fac.AntdInput(addonBefore='dockstream_root_path', value='./Tree_Invent/envs/DockStream', style=input_style),
            fac.AntdInput(addonBefore='grid_path', value="./glide-grid_7RFS_CovPosConstraint.zip", style=input_style),
            fac.AntdInputNumber(addonBefore='ncores', value=25, style=input_style),
            fac.AntdInputNumber(addonBefore='nposes', value=2, style=input_style),
            html.Label('glide_keywords'),
            fuc.FefferyJsonViewer(
                data={},
                editable=True, addible=True, deletable=True)
        ], direction="vertical")
    ]
)

sample_constrain_input = fac.AntdForm(
    id='sample_constrain_input',
    children=[
        fac.AntdSpace([
            fac.AntdInputNumber(addonBefore='max_node_steps', value=100, style=input_style),
            fac.AntdInputNumber(addonBefore='max_ring_nodes', value=100, style=input_style),
            fac.AntdInputNumber(addonBefore='temperature', value=1.0, style=input_style),
            fac.AntdInput(addonBefore='ring_check_mode', value="easy", style=input_style),
            fac.AntdInput(addonBefore='constrain_step_dict_file', value="./Tree_Invent/constrain_step_dict.json", style=input_style),
        ], direction="vertical")
    ]
)


@app.callback(
    Output("component-value-setter", "children"),
    Input("component-select-dropdown", "value")
)
def update_Component(component_select):
    if component_select == 'train':
        return train_input
    elif component_select == 'rl':
        return rl_input
    elif component_select == 'docking':
        return docking_input
    else:
        return sample_constrain_input



