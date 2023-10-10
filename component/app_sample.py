import os
import json
import sys

import dash
import dash_bootstrap_components as dbc
import feffery_antd_components as fac
from dash import html, dcc
from dash.dependencies import Input, Output, State

sys.path.append("..")
from server import app
from .common_layout import train_dict, sample_constrain_dict, card_style, card_style_hide, \
    form_style, number_style, getter_value, success_message, error_message, upload_dir, sample_dir, sample_dict
from .app_score_components import similarities_layout, activity_layout, \
    shape_layout, dockscore_layout
from .app_graph import graph_layout
from flask import send_from_directory
import uuid
import zipfile

# sample_dict = train_dict.copy()
sample_dict.update(sample_constrain_dict)
rl_dict = {
    'score_components': [],
    'score_weights': [],
    'acc_steps': 1,
    'temperature_range': (1.0, 1.2),
    'temperature_scheduler': 'linear',
    'save_pic': True
}

##==================general_setting value input=====================
general_value_card = fac.AntdCard(
    title='General setting',
    children=[
        fac.AntdForm(
            id='general-input',
            children=[
                fac.AntdFormItem(fac.AntdInput(value=''), help='prior model path, example: XXX/XXX.zip', label='prior'),
                fac.AntdFormItem(fac.AntdInput(value=''),
                                 help='path of save output model file, example:XXX/XXX.zip', label='model_save_path'),
                fac.AntdFormItem(fac.AntdInputNumber(value=1000, style=number_style),
                                 label="batchsize"),
                fac.AntdFormItem(fac.AntdInputNumber(value=0.0001, step=0.0001, style=number_style), label='initlr'),
                fac.AntdButton('Update value', id='general-button', type='primary',
                               icon=fac.AntdIcon(icon='antd-check-circle'))

            ],
            labelCol={'span': 10},
            style=form_style
        )
    ],
    headStyle={'background-color': '#fafafa'},
    style=card_style,
)

# ===================sample_model_rl layout========================
score_func_name = ["similarities", "activity", "shape", "dockscore"]
score_titles = ["Similarities", "Activity", "Shape rocs", "Dockscore"]
score_layout_list = [similarities_layout, activity_layout, shape_layout, dockscore_layout]
similarities_dict = {'target_smiles': '', 'target_molfile': ''}
activity_dict = {'qsar_models_path': ''}
shape_dict = {'rocs': {'cff_path':'', 'refig_sdf_path': '', 'shape_w': '', 'color_w': '', 'sim_measure': 'Tanimoto'}}
dockscore_dict = {'docking': {'backend':'AutoDockVina', 'dock_input_path': '', 'dockstream_root_path': '',
                              'low_threshold': -13, 'high_threshold': -4, 'k': 0.2, 'ncores': 10, 'nposes': 2,
                              'AutoDockVina': '', 'target_pdb': '', 'refligh_pdb': '', 'vina_bin_path': ''}}
score_data_dict = [similarities_dict, activity_dict, shape_dict, dockscore_dict]

def set_score_components(score_name, score_title, score_layout, score_dict):
    components = fac.AntdFormItem([
        fac.AntdCheckbox(id=f"{score_name}-checkbox", label=score_title, style={'width': '100px'}),
        fac.AntdInputNumber(id=f"{score_name}-weight", value=1, min=0, addonBefore='weight', disabled=True),
        fac.AntdButton('Configuration', id=f"{score_name}-button", type='primary',
                       icon=fac.AntdIcon(icon='antd-tool-two-tone'), disabled=True),
        fac.AntdModal(
            id=f"{score_name}-modal",
            title=score_title,
            renderFooter=True,
            children=score_layout,
            okText='Submit',
            cancelText='Cancel',
            centered=True,
            width='60vw'
        ),
        dcc.Store(id=f"{score_name}-value-setter-store", data=score_dict),
        html.Div(id=f"{score_name}-upload-modal"),
        # html.Div(id=f"{score_name}-upload-progress"),
    ])
    return components


rl_value_card = fac.AntdCollapse(
    id='rl-Collapse',
    title='Reinforcement learning setting',
    isOpen=True,
    style=card_style,
    children=fac.AntdForm(
        id='rl-input',
        children=[
            fac.AntdDivider('Reinforcement learning general setting'),
            html.Div(
                id='rl-general-input',
                children=[
                    fac.AntdFormItem(fac.AntdInputNumber(id='acc-steps',value=1, min=1, style=number_style), label="acc_steps"),
                    fac.AntdFormItem(fac.AntdRadioGroup(
                        id='temperature-scheduler',
                        options=
                        [
                            {'label': 'same', 'value': 'same'},
                            {'label': 'linear', 'value': 'linear'}
                        ],
                        defaultValue='same'
                    ),
                        label='temperature_scheduler'),
                    fac.AntdFormItem(
                        [
                            fac.AntdSpace(
                                id='temperature-range-linear',
                                direction='horizontal',
                                children=
                                [
                                    fac.AntdInputNumber(id='temperature-range-min', value=1, step=0.1, addonBefore='min'),
                                    fac.AntdInputNumber(id='temperature-range-max', value=1.2, step=0.1, addonBefore='max'),
                                ],
                            ),
                            fac.AntdInputNumber(id='temperature-range-same', value=1, step=0.1, style=number_style),
                            html.Div(id='temperature-range-message'),
                        ],
                        label='temperature_range'
                    ),
                    dcc.Store(id='rl-general-value-setter-store'),
                ]),

            # fac.AntdFormItem(fac.AntdSwitch(checked=True), label="save_pic"),

            # score_components,
            fac.AntdDivider('Score components'),
            fac.AntdFormItem([set_score_components(score_name, score_title, score_layout, score_dict) for
                              score_name, score_title, score_layout, score_dict in
                              zip(score_func_name, score_titles, score_layout_list, score_data_dict)]),
            html.Div(id='glide-Collapse-callback'),
            fac.AntdButton('Update value', id='rl-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle'))
        ],
        labelCol={'span': 10},
        style=form_style
    ),
)


# ===================sample model layout==========================
sample_common_layout_with_rl = [
    general_value_card,
    fac.AntdSpace(
        [
            html.Div(html.H5('sample with Reinforcement learning constrain model')),
            fac.AntdSwitch(
                id='use-rl',
                checkedChildren='on',
                unCheckedChildren='off',
                checked=True
            )
        ],
    ),
    rl_value_card,
    dcc.Store(id='sample-value-setter-store', data=sample_dict),
    dcc.Store(id='sample-constrain-upload-path-store'),
    dcc.Store(id='rl-value-setter-store', data=rl_dict),
    fac.AntdButton(
        'Generate sample setting file', id='sample-download-button', type='primary',
        icon=fac.AntdIcon(icon='antd-cloud-download'),
        style={'display': 'block'},
    ),
    dcc.Download(id='sample-download-json'),
    html.Div(id='samlpe-layout-update-value-message'),
    html.Div(id='modal-basic-demo-open'),
    html.Div(id='upload-callback'),
]

sample_common_layout = fac.AntdSpace(
    id='sample-common-layout',
    direction='vertical',
    children=sample_common_layout_with_rl
)


##===================initialize general input=====================
# @app.callback(
#     Output('general-input', 'children'),
#     Input('general-input', 'children'),
#     Input('training-value-setter-store', 'data'),
#     prevent_initial_call=True,
# )
# def initialize_general_input(general_input, train_data):
#     general_input[0]['props']['children']['props']['value'] = train_data['train']['model_save_path']
#     general_input[1]['props']['children']['props']['value'] = train_data['train']['batchsize']
#     general_input[2]['props']['children']['props']['value'] = train_data['train']['initlr']
#     return general_input


##====================update general_setting for sample value======================
@app.callback(
    Output('sample-value-setter-store', 'data', allow_duplicate=True),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('general-button', 'nClicks'),
    Input('general-input', 'children'),
    State('sample-value-setter-store', 'data'),
    prevent_initial_call=True,
)
def update_sample_value(general_nClicks, general_data, previous_data):
    if general_nClicks:
        data = previous_data
        general_dict = getter_value(general_data[:-1])
        if general_dict is None:
            return dash.no_update, error_message
        data['model'].update(general_dict)
        return data, success_message
    else:
        return dash.no_update, []


##====================download sample_model.json============================

# @app.callback(
#     Output('final-download-button', 'href'),
#     Input('sample-download-button', 'nClicks'),
#     prevent_initial_call=True,
# )
# def download_func(nClicks):
#     if nClicks:
#         # with zipfile.ZipFile('/home/linjie/projects/dash_projects/tree_invent_web/upload/sample_dir/download.zip', 'w') as zipobj:
#         #     for file in ['case_1.sdf', 'sp_8DZ0_Hconstraint_TI_ENS_2.in']:
#         #         try:
#         #             zipobj.write(os.path.join('/home/linjie/projects/dash_projects/tree_invent_web/upload/test_dir', file))
#         #         except FileNotFoundError:
#         #             pass
#         return f"/download/case_1.sdf"
#     else:
#         return dash.no_update

@app.callback(
    Output('sample-download-json', 'data'),
    Input('sample-download-button', 'nClicks'),
    State('sample-value-setter-store', 'data'),
    State('atom-index-value-setter-store', 'data'),
    prevent_initial_call=True,
)
def download_func(nClicks, data, mol_data):
    uuid_name = str(uuid.uuid4())
    result_dir = os.path.join(sample_dir, uuid_name)
    os.makedirs(result_dir)
    with open(os.path.join(result_dir, 'sample_file.json'), 'w')as f:
        json.dump(data, f)
    dir_list, filename_list = [result_dir], ['sample_file.json']
    if len(mol_data)>0:
        for k, v in mol_data.items():
            dir_list.append(os.path.dirname(v['specific_nodefile']))
            filename_list.append(os.path.basename(v['specific_nodefile']))
    with zipfile.ZipFile(os.path.join(result_dir, 'sample_file.zip'), 'w') as zipobj:
        for dir, filename in zip(dir_list, filename_list):
            try:
                os.chdir(dir)
                zipobj.write(filename)
            except FileNotFoundError:
                pass
    return dcc.send_file(os.path.join(result_dir, 'sample_file.zip'))

##========================================================================================
##=====================Choose the rl=========================
@app.callback(
    Output('rl-Collapse', 'style'),
    Input('use-rl', 'checked')
)
def choose_rl(checked):
    if checked:
        return card_style
    else:
        return card_style_hide

##======================temperature-range============================
@app.callback(
    Output('temperature-range-linear', 'style'),
    Output('temperature-range-same', 'style'),
    Input('temperature-scheduler', 'value')
)
def display_temp_range(value):
    if value == 'linear':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, number_style


@app.callback(
    Output('temperature-range-message', 'children'),
    Output('temperature-range-max', 'value'),
    Output('temperature-range-min', 'value'),
    Input('temperature-range-min', 'value'),
    Input('temperature-range-max', 'value')
)
def display_temp_range(min_value, max_value):
    if min_value is None or max_value is None:
        return error_message, 1.2, 1.0
    if min_value >= max_value:
        return fac.AntdAlert(message=f'The minimum value must be less than the maximum value', type='error',
                             showIcon=True), min_value+0.1, min_value
    else:
        return [], max_value, min_value

##====================update rl-general-value=====================
@app.callback(
    Output('rl-general-value-setter-store', 'data'),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('acc-steps', 'value'),
    Input('temperature-scheduler', 'value'),
    Input('temperature-range-min', 'value'),
    Input('temperature-range-max', 'value'),
    Input('temperature-range-same', 'value'),
    Input('rl-general-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_rl_value(acc_steps, scheduler, min_value, max_value, same_value, rl_general_data):
    output_data = rl_general_data or {}
    if acc_steps is None:
        return dash.no_update, error_message

    output_data.update({'acc_steps': acc_steps, 'temp_scheduler': scheduler})

    if output_data['temp_scheduler']=='linear':
        if min_value is None or max_value is None:
            return dash.no_update, error_message
        linear_value = tuple([min_value, max_value])
        output_data.update({'temp_range': linear_value})
    else:
        if same_value is None:
            return dash.no_update, error_message
        output_data.update({'temp_range': same_value})

    # print('rl-general-value-setter-store', output_data)
    return output_data, []

@app.callback(
    Output('sample-value-setter-store', 'data', allow_duplicate=True),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('rl-button', 'nClicks'),
    Input('use-rl', 'checked'),
    Input('similarities-checkbox', 'checked'),
    Input('activity-checkbox', 'checked'),
    Input('shape-checkbox', 'checked'),
    Input('dockscore-checkbox', 'checked'),
    State('similarities-weight', 'value'),
    State('activity-weight', 'value'),
    State('shape-weight', 'value'),
    State('dockscore-weight', 'value'),
    State('similarities-value-setter-store', 'data'),
    State('activity-value-setter-store', 'data'),
    State('shape-value-setter-store', 'data'),
    State('dockscore-value-setter-store', 'data'),
    State('rl-general-value-setter-store', 'data'),
    State('training-value-setter-store', 'data'),
    State('sample-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_sample_value(rl_nClicks, use_rl_nClicks, similarities_checkbox, activity_checkbox, shape_checkbox, dockscore_checkbox,
                        similarities_weight, activity_weight, shape_weight, dockscore_weight,
                        similarities_data, activity_data, shape_data, dockscore_data,
                        rl_general_data, train_data, previous_data):
    ctx = dash.callback_context
    if use_rl_nClicks and ctx.triggered[0]['prop_id'].startswith('rl-button'):
        if similarities_checkbox or activity_checkbox or shape_checkbox or dockscore_checkbox:
            weight_list, score_components = [], []
            data = previous_data or train_data
            data['rl']=rl_general_data
            # print('add rl-general-value-setter-store to data', data)
            if similarities_checkbox and similarities_data:
                weight_list.append(similarities_weight)
                score_components.append('similarities')
                data['rl'].update(similarities_data)
            if activity_checkbox and activity_data:
                weight_list.append(activity_weight)
                score_components.append('activity')
                data['rl'].update(activity_data)
            if shape_checkbox and shape_data:
                weight_list.append(shape_weight)
                score_components.append('shape')
                # print('shape_data', shape_data)
                data.update(shape_data)
            if dockscore_checkbox and dockscore_data:
                weight_list.append(dockscore_weight)
                score_components.append('dockscore')
                data.update(dockscore_data)
            data['rl'].update({'score_components': score_components})
            data['rl'].update({'score_weights': weight_list})
            # data = json.dumps(data)
            print('final data', data)
            return data, success_message
        else:
            return dash.no_update, fac.AntdModal('You must choose at least one scoring component!', title='Update reinforcement learning value Error', centered=True, visible=True)
    else:
        return dash.no_update, []

