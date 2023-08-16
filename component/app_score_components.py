import dash
from dash import html, dcc
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
import json
import uuid
import os
from flask import request
import sys
sys.path.append("..")
from server import app
from .common_layout import card_style2, form_style, number_style, getter_value, upload_dir


@app.server.route('/upload/', methods=['POST'])
def upload():
    uploadId = request.values.get('uploadId')
    filename = request.files['file'].filename
    try:
        os.mkdir(os.path.join(upload_dir, uploadId))
    except FileExistsError:
        pass

    with open(os.path.join(upload_dir, uploadId, filename), 'wb') as f:
        # 流式写出大型文件，这里的10代表10MB
        for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
            f.write(chunk)

    return {'filename': filename}


##======================score_components=========================
similarities_layout = fac.AntdCard(
    id='similarities-Collapse',
    title='similarities',
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
            fac.AntdFormItem(fac.AntdInput(id='target_smiles', value='["CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F"]'), label="target_smiles"),
            fac.AntdFormItem(fac.AntdInput(id='target_molfile', value='./target_molfile.smi'), label="target_molfile"),
            fac.AntdFormItem(fac.AntdInputNumber(value=0.7, step=0.1, style=number_style), label="tanimoto_k"),
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

activity_layout = fac.AntdCard(
    id='activity-Collapse',
    title='activity',
    headStyle={'display': 'none'},
    style=card_style2,
    children=fac.AntdForm(
        id='activity-input',
        children=[
            fac.AntdFormItem(fac.AntdInput(value="./activity/SVC.pickle"), label="qsar_models_path"),
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

shape_layout = fac.AntdCard(
    id='shape-Collapse',
    title='rocs',
    headStyle={'display': 'none'},
    style=card_style2,
    children=fac.AntdForm(
        id='shape-input',
        children=[
            fac.AntdFormItem(fac.AntdInput(value="./6w8i_ligand.cff"), label="cff_path"),
            fac.AntdFormItem(fac.AntdInput(value="./6w8i_ligand.sdf"), label="reflig_sdf_path"),
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
        fac.AntdFormItem(fac.AntdInput(value="target.pdb"), label="AutoDockVina"),
        fac.AntdFormItem(fac.AntdInput(value="target.pdb"), label="target_pdb"),
        fac.AntdFormItem(fac.AntdInput(value="reflig.pdb"), label="reflig_pdb"),
        fac.AntdFormItem(fac.AntdInput(value="./Tree_Invent/envs/autodock_vina_1_1_2_linux_x86/bin"), label="vina_bin_path"),

    ],
)

glide_layout = html.Div(
    id='glide-dockscore-input',
    style={'display': 'none'},
    children=[
        fac.AntdFormItem(fac.AntdInput(value="{}"), label="glide_flags"),
        fac.AntdFormItem(fac.AntdInput(value="2017"), label="glide_ver"),
        fac.AntdFormItem(fac.AntdInput(value="glide-grid_4OW0_min.zip"), label="grid_path"),
        fac.AntdFormItem(
            fac.AntdUpload(
                id='upload-glide-keywords-json',
                apiUrl='/upload/',
                fileMaxSize=1,
                fileTypes=['json'],
                buttonContent='upload glide keywords json file',
                uploadId=str(uuid.uuid1()),
                locale='en-us',
                showUploadList=False,
                # showSuccessMessage=False,
                # showErrorMessage=False
            ),
        label='glide_keywords'
        ),
        html.Div(id='glide-upload-callback'),
    ],
)


dockscore_layout = fac.AntdCard(
    id='dockscore-Collapse',
    title='dockscore',
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
                fac.AntdFormItem(fac.AntdInput(value="./input"), label="dock_input_path"),
                fac.AntdFormItem(fac.AntdInput(value="./Tree_Invent/envs/DockStream"), label="dockstream_root_path"),
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
    Output('target_smiles', 'disabled'),
    Output('target_molfile', 'disabled'),
    Input('target_type', 'value'),
)
def modify_similarities_input(target_type):
    if target_type == 'target_smiles':
        return False, True
    else:
        return True, False

##====================select score components callback===================
for name in ["similarities", "activity", "shape", "dockscore"]:
    @app.callback(
        Output(f"{name}-weight", 'disabled'),
        Output(f"{name}-button", 'disabled'),
        Input(f"{name}-checkbox", 'checked'),
        prevent_initial_call=True
    )
    def score_components_callback(checked):
        disabled = False if checked else True
        return disabled, disabled

    @app.callback(
        Output(f"{name}-modal", 'visible'),
        Input(f"{name}-button", 'nClicks'),
        prevent_initial_call=True
    )
    def score_components_callback(nClicks):
        return True


@app.callback(
    Output('vina-dockscore-input', 'style'),
    Output('glide-dockscore-input', 'style'),
    Input('dockscore-backend', 'value'),
    prevent_initial_call=True
)
def update_dockscore_backend(backend):
    if backend=='AutoDockVina':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}

##=====================update similarities-value-setter-store======================
@app.callback(
    Output('similarities-value-setter-store', 'data'),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('similarities-input', 'children'),
    Input('similarities-modal', 'okCounts'),
    prevent_initial_call=True
)
def update_score_func(input_data, okCounts):
    if okCounts:
        output_dict = getter_value(input_data)
        if output_dict['target_type']=='target_smiles':
            output_dict.pop('target_molfile')
        else:
            output_dict.pop('target_smiles')
        # print('similarities_data', output_dict)
        return {'rl': output_dict}, fac.AntdMessage(content='Submit Successfully!', type='success')
    else:
        return dash.no_update, []

##=====================update activity-value-setter-store======================
@app.callback(
    Output('activity-value-setter-store', 'data'),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('activity-input', 'children'),
    Input('activity-modal', 'okCounts'),
    prevent_initial_call=True
)
def update_score_func(input_data, okCounts):
    if okCounts:
        output_dict = getter_value(input_data)
        # print('activity_data',output_dict)
        return {'rl': output_dict}, fac.AntdMessage(content='Submit Successfully!', type='success')
    else:
        return dash.no_update, []

##=====================update shape-value-setter-store======================
@app.callback(
    Output('shape-value-setter-store', 'data'),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('shape-input', 'children'),
    Input('shape-modal', 'okCounts'),
    prevent_initial_call=True
)
def update_score_func(input_data, okCounts):
    if okCounts:
        output_dict = getter_value(input_data)
        # print('rocs',output_dict)
        return {'rocs': output_dict}, fac.AntdMessage(content='Submit Successfully!', type='success')
    else:
        return dash.no_update, []

##=====================update dockscore-value-setter-store======================
@app.callback(
    Output('dockscore-value-setter-store', 'data'),
    Output('glide-Collapse-callback', 'children'),
    Output('samlpe-layout-update-value-message', 'children', allow_duplicate=True),
    Input('dockscore-general-input', 'children'),
    Input('vina-dockscore-input', 'children'),
    Input('glide-dockscore-input', 'children'),
    Input('dockscore-modal', 'okCounts'),
    State('upload-glide-keywords-json', 'uploadId'),
    State('upload-glide-keywords-json', 'lastUploadTaskRecord'),
    State('upload-glide-keywords-json', 'listUploadTaskRecord'),
    prevent_initial_call=True
)
def update_score_func(dockscore_general_input,vina_input, glide_input, okCounts, uploadId, lastUploadTaskRecord, listUploadTaskRecord):
    if okCounts:
        output_dict = getter_value(dockscore_general_input)
        if output_dict['backend']=='AutoDockVina':
            for k in ['glide_flags', 'glide_ver', 'grid_path', 'glide_keywords']:
                output_dict.pop(k) if k in output_dict.keys() else output_dict

            vina_dict = getter_value(vina_input)
            output_dict.update(vina_dict)
        else:
            for k in ['AutoDockVina', 'target_pdb', 'reflig_pdb', 'vina_bin_path']:
                output_dict.pop(k) if k in output_dict.keys() else output_dict
            glide_dict = getter_value(glide_input[:3])
            if lastUploadTaskRecord and lastUploadTaskRecord['taskStatus']=='success':
                print(f"{upload_dir}/{uploadId}/{lastUploadTaskRecord['fileName']}")
                with open(f"{upload_dir}/{uploadId}/{lastUploadTaskRecord['fileName']}", 'r') as f:
                    content = json.load(f)
                    glide_dict['glide_keywords'] = content
            else:
                return dash.no_update, fac.AntdModal('Please upload glide keywords json file', title='submit failure', centered=True, visible=True)
            output_dict.update(glide_dict)
        # print(output_dict)
        return {'docking': output_dict}, dash.no_update, fac.AntdMessage(content='Submit Successfully!', type='success')
    else:
        return dash.no_update, dash.no_update, []

##=====================update sample-value-setter-store by glide dockscore======================
#=====================upload file server by glide dockscore===========================
@app.callback(
    Output('glide-upload-callback', 'children'),
    Input('upload-glide-keywords-json', 'lastUploadTaskRecord'),
    prevent_initial_call=True
)
def show_upload_status(lastUploadTaskRecord):
    if lastUploadTaskRecord['taskStatus']=='success':
        return fac.AntdProgress(percent=100, style={'width': 200, 'left':'40%'})
    else:
        return fac.AntdMessage(content='Upload Error', type='error')



for name in ["similarities", "activity", "shape", "dockscore"]:
    @app.callback(
        Output(f"{name}-modal", 'okCounts'),
        Input('app-tabs', 'value')
    )
    def setter_nClicks(value):
        if value=='tab1':
            return None
        else:
            return dash.no_update



