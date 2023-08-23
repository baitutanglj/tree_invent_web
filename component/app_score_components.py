import os
import sys

import dash
import feffery_antd_components as fac
import pandas as pd
from dash import html
from dash.dependencies import Input, Output, State
from flask import request

sys.path.append("..")
from server import app
from .common_layout import card_style2, form_style, number_style, \
    getter_value, error_message, upload_error_message, upload_layout, \
    dockscore_dir


@app.server.route("/similarities/", methods=['POST'])
def similarities_upload():
    uploadId = request.values.get('uploadId')
    filename = request.files['file'].filename
    # try:
    #     os.makedirs(os.path.join(similarities_dir, uploadId))
    # except FileExistsError:
    #     pass
    #
    # with open(os.path.join(similarities_dir, uploadId, filename), 'wb') as f:
    #     # 流式写出大型文件，这里的10代表10MB
    #     for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
    #         f.write(chunk)
    return {'filename': filename}

@app.server.route("/activity/", methods=['POST'])
def activity_upload():
    uploadId = request.values.get('uploadId')
    filename = request.files['file'].filename
    # try:
    #     os.makedirs(os.path.join(activity_dir, uploadId))
    # except FileExistsError:
    #     pass
    #
    # with open(os.path.join(activity_dir, uploadId, filename), 'wb') as f:
    #     # 流式写出大型文件，这里的10代表10MB
    #     for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
    #         f.write(chunk)
    return {'filename': filename}


@app.server.route("/shape_rocs/", methods=['POST'])
def shape_rocs_upload():
    filename = request.files['file'].filename
    return {'filename': filename}

@app.server.route("/shape_reflig/", methods=['POST'])
def shape_reflig_upload():
    filename = request.files['file'].filename
    return {'filename': filename}


@app.server.route("/dockscore/", methods=['POST'])
def dockscore_upload():
    uploadId = request.values.get('uploadId')
    filename = request.files['file'].filename
    # try:
    #     os.makedirs(os.path.join(dockscore_dir, uploadId))
    # except FileExistsError:
    #     pass
    #
    # with open(os.path.join(dockscore_dir, uploadId, filename), 'wb') as f:
    #     # 流式写出大型文件，这里的10代表10MB
    #     for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
    #         f.write(chunk)
    return {'filename': filename}


@app.server.route("/glide/", methods=['POST'])
def glide_upload():
    uploadId = request.values.get('uploadId')
    filename = request.files['file'].filename
    try:
        os.makedirs(os.path.join(dockscore_dir, uploadId))
    except FileExistsError:
        pass

    with open(os.path.join(dockscore_dir, uploadId, filename), 'wb') as f:
        # 流式写出大型文件，这里的10代表10MB
        for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
            f.write(chunk)
    return {'filename': filename}


##======================score_components=========================
similarities_layout = fac.AntdCard(
    id='similarities-Collapse',
    title='Similarities',
    headStyle={'display': 'none'},
    style=card_style2,
    children=fac.AntdForm(
        id='similarities-input',
        children=[
            fac.AntdFormItem(fac.AntdRadioGroup(
                id='target_type',
                options=
                [
                    {'label': 'target_smiles', 'value': 'target_smiles'},
                    {'label': 'target_molfile', 'value': 'target_molfile'}
                ],
                defaultValue='target_smiles'),
                label='target_type'),
            fac.AntdFormItem(fac.AntdInput(id='target-smiles', value=''),
                             help='["CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F"]',
                             label="target_smiles"),
            # fac.AntdFormItem(fac.AntdInput(id='target-molfile', value=''), help='./target_molfile.smi',
            #                  label="target_molfile"),
            fac.AntdFormItem(fac.AntdInput(id='target-mol-dictionary', value=''),
                             help='local absolute target file dictionary',
                             label="target_mol_dictionary"),
            fac.AntdFormItem(upload_layout(id='upload-target-molfile', filetype=['smi'], apiurl='/similarities/',
                                            buttonContent='upload .smi target molfile'),
                             label="target_molfile"),
            fac.AntdFormItem(fac.AntdInputNumber(value=0.7, step=0.1, style=number_style), label="tanimoto_k"),
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

activity_layout = fac.AntdCard(
    id='activity-Collapse',
    title='Activity',
    headStyle={'display': 'none'},
    style=card_style2,
    children=fac.AntdForm(
        id='activity-input',
        children=[
            # fac.AntdFormItem(fac.AntdInput(), help="./activity/SVC.pickle", label="qsar_models_path"),
            fac.AntdFormItem(fac.AntdInput(id='qsar-models-dictionary', value=''),
                             help='local absolute qsar models file dictionary',
                             label="qsar_models_dictionary"),
            fac.AntdFormItem(upload_layout(id='upload-qsar-models', filetype=['pickle'], apiurl='/activity/',
                                           buttonContent='upload qsar model pickle file'), label="qsar_models_file")
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

shape_layout = fac.AntdCard(
    id='shape-Collapse',
    title='Shape rocs',
    headStyle={'display': 'none'},
    style=card_style2,
    children=fac.AntdForm(
        id='shape-input',
        children=[
            # fac.AntdFormItem(fac.AntdInput(value=''), help="./6w8i_ligand.cff", label="cff_path"),
            # fac.AntdFormItem(fac.AntdInput(value=''), help="./6w8i_ligand.sdf", label="reflig_sdf_path"),
            fac.AntdFormItem(fac.AntdInput(id='shape-rocs-dictionary', value=''),
                             help='local absolute rocs file dictionary',
                             label="shape_rocs_dictionary"),
            fac.AntdFormItem(upload_layout(id='upload-cff-file', filetype=['cff'], apiurl='/shape_rocs/',
                                           buttonContent='upload cff file'), label="cff_file"),
            fac.AntdFormItem(upload_layout(id='upload-reflig-sdf-file', filetype=['sdf'], apiurl='/shape_rocs/',
                                           buttonContent='upload reflig sdf file'), label="reflig_sdf_file"),
            fac.AntdFormItem(fac.AntdInputNumber(value=0.5, step=0.1, style=number_style), label="shape_w"),
            fac.AntdFormItem(fac.AntdInputNumber(value=0.5, step=0.1, style=number_style), label="color_w"),
            fac.AntdFormItem(fac.AntdRadioGroup(
                options=
                [
                    {'label': 'Tanimoto', 'value': 'Tanimoto'},
                    {'label': 'RefTversky', 'value': 'RefTversky'}
                ],
                defaultValue='Tanimoto'),
                label='sim_measure'),
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

vina_layout = html.Div(
    id='vina-dockscore-input',
    style={'display': 'block'},
    children=[
        fac.AntdFormItem(fac.AntdInputNumber(value=20, style=number_style), label="box_size"),
        # fac.AntdFormItem(fac.AntdInput(value=''), help="target.pdb", label="target_pdb"),
        # fac.AntdFormItem(fac.AntdInput(value=''), help="reflig.pdb", label="reflig_pdb"),
        fac.AntdFormItem(
            upload_layout(id='upload-target-pdb', filetype=['pdb'], apiurl='/dockscore/',
                          buttonContent='upload target pdb file'),
            label="target_pdb"),
        fac.AntdFormItem(
            upload_layout(id='upload-reflig-pdb', filetype=['pdb'], apiurl='/dockscore/',
                          buttonContent='upload reflig pdb file'),
            label="reflig_pdb"),
        fac.AntdFormItem(fac.AntdInput(value=''), help="./Tree_Invent/envs/autodock_vina_1_1_2_linux_x86/bin",
                         label="vina_bin_path"),

    ],
)

glide_layout = html.Div(
    id='glide-dockscore-input',
    style={'display': 'none'},
    children=[
        # fac.AntdFormItem(fac.AntdInput(value=''), help="{}", label="glide_flags"),
        fac.AntdFormItem(fac.AntdInput(value="2017"), label="glide_ver"),
        fac.AntdFormItem(
            upload_layout(id='upload-glide-input-file', filetype=['in'], apiurl='/glide/', buttonContent='upload glide input file'),
            label="glide_input_file"),
    ],
)

dockscore_layout = fac.AntdCard(
    id='dockscore-Collapse',
    title='Dockscore',
    headStyle={'display': 'none'},
    style=card_style2,
    children=fac.AntdForm(
        id='dockscore-input',
        labelCol={'span': 10},
        style=form_style,
        children=[
            html.Div(
                id='dockscore-general-input',
                children=
                [
                    fac.AntdFormItem(fac.AntdRadioGroup(
                        id='dockscore-backend',
                        options=
                        [
                            {'label': 'AutoDockVina', 'value': 'AutoDockVina'},
                            {'label': 'Glide', 'value': 'Glide'}
                        ],
                        defaultValue='AutoDockVina',
                    ),
                        label='backend'),
                    fac.AntdFormItem(fac.AntdInput(value=''), help="./Tree_Invent/3CLPro/7RFS",
                                     label="dock_input_dictionary"),
                    fac.AntdFormItem(fac.AntdInput(value=''), help="./Tree_Invent/envs/DockStream",
                                     label="dockstream_root_path"),
                    fac.AntdFormItem(fac.AntdInputNumber(value=-13.0, style=number_style), label="low_threshold"),
                    fac.AntdFormItem(fac.AntdInputNumber(value=-4.0, style=number_style), label="high_threshold"),
                    fac.AntdFormItem(fac.AntdInputNumber(value=0.2, step=0.1, style=number_style), label="k"),
                    fac.AntdFormItem(fac.AntdInputNumber(value=10, style=number_style), label="ncores"),
                    fac.AntdFormItem(fac.AntdInputNumber(value=2, style=number_style), label="nposes"),
                ]),
            vina_layout,
            glide_layout,

        ]
    )
)


##==================similarities_layout target type#######################
@app.callback(
    Output('target-smiles', 'disabled'),
    Output('target-mol-dictionary', 'disabled'),
    Output('upload-target-molfile', 'disabled'),
    Input('target_type', 'value'),
)
def modify_similarities_input(target_type):
    if target_type == 'target_smiles':
        return False, True, True
    else:
        return True, False, False


##====================select score components callback===================
for name in ["similarities", "activity", "shape", "dockscore"]:
    @app.callback(
        Output(f"{name}-weight", 'disabled'),
        Output(f"{name}-button", 'disabled'),
        Output(f"{name}-modal", 'okCounts', allow_duplicate=True),
        Input(f"{name}-checkbox", 'checked'),
        prevent_initial_call=True
    )
    def score_components_callback(checked):
        disabled = False if checked else True
        nClicks = 0 if checked else dash.no_update
        return disabled, disabled, nClicks


    @app.callback(
        Output(f"{name}-modal", 'visible'),
        Input(f"{name}-button", 'nClicks'),
        prevent_initial_call=True
    )
    def score_components_callback(nClicks):
        if nClicks:
            return True
        else:
            return dash.no_update


    ##===========submit callback===============
    @app.callback(
        Output(f"{name}-modal", 'visible', allow_duplicate=True),
        Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
        Output(f"{name}-modal", 'okCounts', allow_duplicate=True),
        Input(f"{name}-modal", 'okCounts'),
        Input(f"{name}-value-setter-store", 'data'),
        prevent_initial_call=True
    )
    def validateStatuss_core_components(okCounts, data):
        # print(name, 'okCounts', okCounts, 'data', data)
        if okCounts:
            if data is not None:
                return False, fac.AntdMessage(content='Submit Successfully!', type='success'), 0
            else:
                return True, error_message, 0
        else:
            return dash.no_update


@app.callback(
    Output('vina-dockscore-input', 'style'),
    Output('glide-dockscore-input', 'style'),
    Input('dockscore-backend', 'value'),
    prevent_initial_call=True
)
def update_dockscore_backend(backend):
    if backend == 'AutoDockVina':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}


##=====================get_upload_filename======================
def get_upload_filename(lastUploadTaskRecord):
    if lastUploadTaskRecord and lastUploadTaskRecord['taskStatus'] == 'success':
        filename = lastUploadTaskRecord['fileName']
    else:
        filename = None
    return filename

def update_output_dict(dirname, filename, keyname, output_dict, pop_dirname=True, pop_keyname=None):
    output_dict[keyname] = os.path.join(output_dict[dirname], filename) if dirname != '' else filename
    if pop_dirname:
        output_dict.pop(dirname)
    if pop_keyname:
        for k in pop_keyname:
            output_dict.pop(k)
    return output_dict


##=====================update similarities-value-setter-store======================
@app.callback(
    Output('similarities-value-setter-store', 'data'),
    Output('similarities-upload-modal', 'children'),
    Input('target_type', 'value'),
    Input('similarities-modal', 'okCounts'),
    State('similarities-input', 'children'),
    State('upload-target-molfile', 'lastUploadTaskRecord'),
    prevent_initial_call=True
)
def update_score_func(target_type, okCounts, input_data, lastUploadTaskRecord):
    upload_file_label = 'target_molfile'
    if target_type == 'target_smiles':
        input_data = [input_data[i] for i in range(len(input_data)) if
                      input_data[i]['props']['label'] not in ['target_mol_dictionary', upload_file_label]]
    else:
        input_data = [input_data[i] for i in range(len(input_data)) if
                      input_data[i]['props']['label'] not in ['target_smiles', upload_file_label]]

    if okCounts:
        output_dict = getter_value(input_data)
        if output_dict is not None:
            if target_type == 'target_smiles':
                output_dict.pop('target_type')
                return output_dict, dash.no_update
            else:
                filename = get_upload_filename(lastUploadTaskRecord)
                if filename is None:
                    return None, upload_error_message
                output_dict = update_output_dict('target_mol_dictionary', filename, upload_file_label, output_dict, pop_keyname=['target_type'])
                # print('okCounts', okCounts, 'similarities_data', output_dict)
                return output_dict, dash.no_update
        else:
            return None, dash.no_update
    else:
        return dash.no_update


##=====================update activity-value-setter-store======================
@app.callback(
    Output('activity-value-setter-store', 'data'),
    Output('activity-upload-modal', 'children'),
    Input('activity-input', 'children'),
    Input('activity-modal', 'okCounts'),
    State('upload-qsar-models', 'lastUploadTaskRecord'),
    prevent_initial_call=True
)
def update_score_func(input_data, okCounts, lastUploadTaskRecord):
    upload_file_label = 'qsar_models_file'
    input_data = [input_data[i] for i in range(len(input_data)) if
                  input_data[i]['props']['label'] not in [upload_file_label]]
    if okCounts:
        output_dict = getter_value(input_data)
        filename = get_upload_filename(lastUploadTaskRecord)
        if filename is None:
            return None, upload_error_message
        if output_dict is not None:
            output_dict = update_output_dict('qsar_models_dictionary', filename, 'qsar_models_path', output_dict)
            # print('activity_data',output_dict)
            return output_dict, dash.no_update
        else:
            return None, dash.no_update
    else:
        return dash.no_update


##=====================update shape-value-setter-store======================
@app.callback(
    Output('shape-value-setter-store', 'data'),
    Output('shape-upload-modal', 'children'),
    Input('shape-input', 'children'),
    Input('shape-modal', 'okCounts'),
    State('upload-cff-file', 'lastUploadTaskRecord'),
    State('upload-reflig-sdf-file', 'lastUploadTaskRecord'),
    prevent_initial_call=True
)
def update_score_func(input_data, okCounts, cff_lastUploadTaskRecord, reflig_lastUploadTaskRecord):
    upload_file_label = ['cff_file', 'reflig_sdf_file']
    input_data = [input_data[i] for i in range(len(input_data)) if
                  input_data[i]['props']['label'] not in upload_file_label]
    if okCounts:
        output_dict = getter_value(input_data)
        filename_cff = get_upload_filename(cff_lastUploadTaskRecord)
        filename_reflig = get_upload_filename(reflig_lastUploadTaskRecord)
        if filename_cff is None or filename_reflig is None:
            return None, upload_error_message
        if output_dict is not None:
            output_dict = update_output_dict('shape_rocs_dictionary', filename_cff, 'cff_path', output_dict, False)
            output_dict = update_output_dict('shape_rocs_dictionary', filename_reflig, 'reflig_sdf_path', output_dict)
            # print('rocs',output_dict)
            return {'rocs': output_dict}, dash.no_update
        else:
            return None, dash.no_update
    else:
        return dash.no_update


##=====================update dockscore-value-setter-store======================
@app.callback(
    Output('dockscore-value-setter-store', 'data'),
    Output('dockscore-upload-modal', 'children'),
    Input('dockscore-general-input', 'children'),
    Input('vina-dockscore-input', 'children'),
    Input('glide-dockscore-input', 'children'),
    Input('dockscore-backend', 'value'),
    Input('dockscore-modal', 'okCounts'),
    State('upload-target-pdb', 'lastUploadTaskRecord'),
    State('upload-reflig-pdb', 'lastUploadTaskRecord'),
    State('upload-glide-input-file', 'lastUploadTaskRecord'),
    prevent_initial_call=True
)
def update_score_func(dockscore_general_input, vina_input, glide_input, backend, okCounts,
                      target_lastUploadTaskRecord, reflig_lastUploadTaskRecord, glide_lastUploadTaskRecord):
    upload_file_label = ['target_pdb', 'reflig_pdb', 'glide_input_file']
    if backend == 'AutoDockVina':
        vina_input = [i for i in vina_input if i['props']['label'] not in upload_file_label]

    else:
        glide_input = [i for i in vina_input if i['props']['label'] not in upload_file_label]
    if okCounts:
        output_dict = getter_value(dockscore_general_input)
        if output_dict is None:
            return None, dash.no_update
        if output_dict['backend'] == 'AutoDockVina':
            vina_dict = getter_value(vina_input)
            if vina_dict is None:
                return None, dash.no_update
            output_dict.update(vina_dict)
            filename_target = get_upload_filename(target_lastUploadTaskRecord)
            filename_reflig = get_upload_filename(reflig_lastUploadTaskRecord)
            if filename_target is None or filename_reflig is None:
                return None, upload_error_message
            output_dict = update_output_dict('', filename_target, 'cff_path', output_dict, False)
            output_dict = update_output_dict('', filename_reflig, 'reflig_sdf_path', output_dict, False)
        else:
            glide_dict = getter_value(glide_input[:1])
            if glide_dict is None:
                return None, dash.no_update
            output_dict.update(glide_dict)
            if glide_lastUploadTaskRecord and glide_lastUploadTaskRecord['taskStatus'] == 'success':
                filepath = f"{dockscore_dir}/{glide_lastUploadTaskRecord['taskId']}/{glide_lastUploadTaskRecord['fileName']}"
                data = pd.read_csv(filepath, names=['key', 'value'], header=None, sep='   ', engine='python')
                data['value'] = data['value'].apply(lambda x: x.replace('\"', '') if x is not None else x)
                if len(data.loc[data['key']=='GRIDFILE','value'])>0:
                    gridfile = data.loc[data['key']=='GRIDFILE','value'].values[0].rsplit('/', maxsplit=1)[1]
                    if gridfile:
                        output_dict.update({'grid_path': gridfile})
                    else:
                        return None, upload_error_message
                else:
                    return None, fac.AntdModal('Glide input file must contain "gridfile" information', title='Submit failure',
                                 centered=True, visible=True)

                key_index = list(data[data['key'].str.contains('\[')].index)
                if len(key_index)>0:
                    key_steps = [[key_index[i], key_index[i + 1]] for i in range(len(key_index) - 1)]
                    glide_keywords_dict = {}
                    for step in key_steps:
                        k = data.loc[step[0], 'key']
                        glide_keywords_dict[k] = {}
                        for i in range(step[0] + 1, step[1]):
                            glide_keywords_dict[k][data.loc[i, 'key']] = data.loc[i, 'value']
                    if len(glide_keywords_dict)>0:
                        output_dict.update({'glide_keywords': glide_keywords_dict})


        return {'docking': output_dict}, dash.no_update
    else:
        return dash.no_update, dash.no_update


##=====================update sample-value-setter-store by glide dockscore======================
# =====================upload file server===========================
for id_name in ['upload-target-molfile', 'upload-qsar-models', 'upload-cff-file',
                'upload-target-pdb', 'upload-glide-input-file']:
    @app.callback(
        Output(f"{id_name}-progress", 'children', allow_duplicate=True),
        Input(id_name, 'lastUploadTaskRecord'),
        prevent_initial_call=True
    )
    def show_upload_status(lastUploadTaskRecord):
        if lastUploadTaskRecord['taskStatus'] == 'success':
            return fac.AntdProgress(percent=100, style={'width': 200})
        else:
            return fac.AntdMessage(content='Upload Error', type='error')

for id_name in ['upload-reflig-sdf-file', 'upload-reflig-pdb']:
    @app.callback(
        Output(f"{id_name}-progress", 'children', allow_duplicate=True),
        Input(id_name, 'lastUploadTaskRecord'),
        prevent_initial_call=True
    )
    def show_upload_status(lastUploadTaskRecord):
        if lastUploadTaskRecord['taskStatus'] == 'success':
            return fac.AntdProgress(percent=100, style={'width': 200})
        else:
            return fac.AntdMessage(content='Upload Error', type='error')


for name in ["similarities", "activity", "shape", "dockscore"]:
    @app.callback(
        Output(f"{name}-modal", 'okCounts'),
        Output(f"{name}-button", 'nClicks'),
        Input('app-tabs', 'value')
    )
    def setter_nClicks(value):
        if value == 'tab1':
            return None, None
        else:
            return dash.no_update
