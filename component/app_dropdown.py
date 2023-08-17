import os
import sys
import uuid

import dash
import feffery_antd_components as fac
from dash import html, dcc
from dash.dependencies import Input, Output, State
from rdkit import Chem

from .common_layout import number_style, mol_dir

sys.path.append("..")
from server import app

node_constrain_dict = {
    'node add':{
        'max_ring_num_per_node': 10,
        'min_ring_num_per_node': 0,
        'max_aromatic_rings': 10,
        'min_aromatic_rings': 0,
        'min_branches':0,
        'max_branches':10,
        'max_heavy_atoms': 100,
        'min_heavy_atoms': 0,
        'max_anum_per_atomtype': {'C':100,'N':100,'O':100,'F':100,'P':100,'S':100,'Cl':100,'Br':100,'I':100},
        'min_anum_per_atomtype': {'C':0,'N':0,'O':0,'F':0,'P':0,'S':0,'Cl':0,'Br':0,'I':0},
        'force_step': False,
        'specific_nodefile': ''
    },
    "node conn": {
        'saturation_atomid_list': [],
        # 'constrain_connect_node_id': [],
        'constrain_connect_atom_id': [[]],
        'constrain_connect_bond_type': [0,1,2],
        'constrain_connect_atomic_type': [6,7,8,9,15,16,17,35,53],
        'anchor_before': -1
    }
}

node_add_default_list = ["specific_nodefile", "max_ring_num_per_node", "min_ring_num_per_node", "max_aromatic_rings",
                         "min_aromatic_rings", "min_branches", "max_branches",
                         "max_anum_per_atomtype", "min_anum_per_atomtype", "max_heavy_atoms",
                         "min_heavy_atoms", "force_step"]
node_conn_default_list = ["saturation_atomid_list",
                          "constrain_connect_atom_id", 'constrain_connect_bond_type',
                          "constrain_connect_atomic_type", "anchor_before"]
constrain_attr_node_add = {
    'value': 'node add',
    'label': 'node attribute',
    'children': [{'value': i, 'label': i} for i in node_add_default_list],
}

def define_node_conn(node_conn_list):
    return {
        'value': 'node conn',
        'label': 'node connect',
        'children': [{'value': i, 'label': i} for i in node_conn_list]
    }


dropdown_card = fac.AntdCollapse(
    title='Input constrain value for the current node',
    isOpen=True,
    style={
    'width': 700,
    'marginBottom': 10,
    'display': 'block'
    },
    children=[
    fac.AntdForm(
        id='node-dropdown-input',
        children=[
            fac.AntdFormItem(fac.AntdAlert(message='If you want to add multiple constraints to the selected nodes, '
                                  'please choose different constraints and input constraint values many times, '
                                  'and submit multiple times',
                            type='warning',showIcon=True)),
            fac.AntdFormItem(fac.AntdInput(id="select-node", defaultValue="0", disabled=True,style={'width': 500}),
                             label="current node"),
            fac.AntdFormItem(html.Div(id='atom-index'), id='display-atom-index', style={'display': 'none'}),
            fac.AntdFormItem(
                fac.AntdCascader(id="constrain-attr",
                    placeholder='select', style={'width': 500},
                    options=[
                        constrain_attr_node_add,
                        define_node_conn(node_conn_default_list)
                        ]
                    ),
                label="constrain"
            ),
            dcc.Store(id='atom-index-value-setter-store', data={}),
            fac.AntdFormItem(id="constrain-item",
                             children=fac.AntdInput(id='constrain-value', placeholder="Input value"),
                             label="constrain_value", style={'display':'block'}),
            fac.AntdFormItem(id="constrain-item2",
                             children=fac.AntdSwitch(id='constrain-value2', checked=True),
                             label="constrain_value", style={'display':'none'}),
            fac.AntdButton('Update value', id='enter-value-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle')),
            html.Div(id='graph-dropdown-message')

        ],
        labelCol={'span': 4},
        # wrapperCol={'span': 20},
        labelAlign='left',
    ),
    html.Div(id='test-output')
    ]
)


##====================constrain-value input layout=====================
@app.callback(
    Output('constrain-item', 'children'),
    Output('constrain-item', 'style'),
    Output('constrain-item2', 'style'),
    Input("constrain-attr", "value"),
    prevent_initial_call=True
)
def setter_constrain_value_layout(value):
    if value[1] in ['max_ring_num_per_node', 'min_ring_num_per_node', 'max_aromatic_rings', 'min_aromatic_rings',
                    'min_branches', 'max_branches', 'max_heavy_atoms', 'min_heavy_atoms', 'anchor_before']:
        return fac.AntdInputNumber(id='constrain-value', placeholder="Input value", style=number_style), \
               {'display':'block'}, {'display':'none'}
    elif value[1] == 'force_step':
        return fac.AntdSwitch(id='constrain-value', checked=True), {'display':'none'}, {'display':'block'}
    else:
        return fac.AntdInput(id='constrain-value', placeholder="Input value"), \
               {'display':'block'}, {'display':'none'}





##=======================show jsme=========================
@app.callback(
    Output("jsme-modal", "is_open"),
    Input("constrain-attr", "value"),
    Input('jsme-button', 'n_clicks')
)
def toggle_modal(value, nClicks):
    ctx = dash.callback_context
    action = ctx.triggered[0]['prop_id']
    if value == ['node add', 'specific_nodefile'] and not action.startswith('jsme-button'):
        return True
    else:
        return False

@app.callback(
    Output('constrain-value', 'disabled'),
    Input("constrain-attr", "value"),
)
def toggle_modal(value):
    if value == ['node add', 'specific_nodefile']:
        return True
    else:
        return False

##=======================draw smile callback=========================

@app.callback(
    Output('constrain-value', 'value'),
    # Output('atom-index', 'children'),
    Output('atom-index-value-setter-store', 'data'),
    Input('jsme-button', 'n_clicks'),
    State('select-node', 'value'),
    State('jsme-graph', 'eventSmiles'),
    State('atom-index-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_value(jsme_nClicks, select_node, input_smiles, atom_index_data):
    ctx = dash.callback_context
    action = ctx.triggered[0]['prop_id']
    # print('input_smiles', input_smiles, 'action', action)
    if action.startswith('jsme-button') and input_smiles:
        glide_uploadId = str(uuid.uuid1())
        os.makedirs(f"{mol_dir}/{glide_uploadId}")
        output_path = f"{mol_dir}/{glide_uploadId}/specific_nodefile.sdf"
        mol = Chem.MolFromSmiles(input_smiles)
        num_atoms = mol.GetNumHeavyAtoms()
        atom_index = ','.join([str(i[0]) for i in mol.GetSubstructMatches(Chem.MolFromSmiles('*'))])
        atom_index_data.update({select_node: {'specific_nodefile': f"{glide_uploadId}/specific_nodefile.sdf",
                                              'num_atoms': num_atoms, 'atom_index': atom_index}})
        with Chem.SDWriter(output_path) as f:
            f.write(mol)
        return f"{glide_uploadId}/specific_nodefile.sdf", atom_index_data

    else:
        return dash.no_update, dash.no_update

##=========================display-atom-index==========================
@app.callback(
    Output('atom-index', 'children'),
    Output('display-atom-index', 'style'),
    Input('select-node', 'value'),
    Input('atom-index-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_value(select_node, atom_index_data):
    if select_node in atom_index_data.keys():
        atom_index_message = fac.AntdAlert(
            message=f"There are {atom_index_data[select_node]['num_atoms']} atoms in the molecule, "
                    f"the connected site of the molecule: {atom_index_data[select_node]['atom_index']}", type='info')

        return atom_index_message, {'display':'block'}
    else:
        return [], {'display':'none'}


##====================clear constrain input===================
@app.callback(
    Output('constrain-value', 'value', allow_duplicate=True),
    Input('enter-value-button', "nClicks"),
    prevent_initial_call=True
)
def toggle_modal(nClicks):
    if nClicks:
        return None
    else:
        return dash.no_update

##==============setter constrain-arr====================
# node_conn_list = ["saturation_atomid_list","constrain_connect_atom_id", 'constrain_connect_bond_type',
#                   "constrain_connect_atomic_type", "anchor_before"]

@app.callback(
    Output('constrain-attr', 'options'),
    Input('select-node', 'value'),
    Input('graph-value-setter-store', 'data'),
    prevent_initial_call=True
)
def toggle_modal(select_node, data):
    # print('data', data)
    select_node_specific_nodefile = 'specific_nodefile' in data['sample_constrain']['constrain_step_dict'][select_node]['node add'].keys()
    if 'constrain_connect_node_id' in data['sample_constrain']['constrain_step_dict'][select_node]['node conn'].keys():
        parent_node = str(data['sample_constrain']['constrain_step_dict'][select_node]['node conn']['constrain_connect_node_id'][0])
    else:
        parent_node = False
    # print('select_node', select_node, 'parent_node', parent_node)
    if parent_node == False:
        #select_node=='0'
        if select_node_specific_nodefile:
            # print('#0 yes#')
            node_conn_list = ['saturation_atomid_list']
            options = [constrain_attr_node_add, define_node_conn(node_conn_list)]
        else:
            # print('#0 no#')
            options = [constrain_attr_node_add]
    else:
        # select_node!='0'
        if select_node_specific_nodefile:
            if 'specific_nodefile' in data['sample_constrain']['constrain_step_dict'][parent_node]['node add'].keys():
                # print('#1 yes, 0 yes#')
                options = [constrain_attr_node_add, define_node_conn(node_conn_default_list)]
            else:
                # print('#1 yes, 0 no#')
                node_conn_list = ["constrain_connect_bond_type", "constrain_connect_atomic_type", "anchor_before"]
                options = [constrain_attr_node_add, define_node_conn(node_conn_list)]
        else:
            if 'specific_nodefile' in data['sample_constrain']['constrain_step_dict'][parent_node]['node add'].keys():
                # print('#1 no, 0 yes#')
                node_conn_list = ["constrain_connect_atom_id", 'constrain_connect_bond_type', "constrain_connect_atomic_type"]
                options = [constrain_attr_node_add, define_node_conn(node_conn_list)]
            else:
                # print('#1 no, 0 no#')
                node_conn_list = ['constrain_connect_bond_type']
                options = [constrain_attr_node_add, define_node_conn(node_conn_list)]

    return options






