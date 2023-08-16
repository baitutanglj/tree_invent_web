import json
import re
import sys

import feffery_antd_components as fac
from dash import html

sys.path.append("..")
mol_dir = '/home/linjie/projects/dash_projects/tree_invent_web/upload_mol'
upload_dir = '/home/linjie/projects/dash_projects/tree_invent_web/upload'
card_style = {
    'width': 700,
    'marginBottom': 10,
    'display': 'block'
}
card_style_hide = {
    'width': 700,
    'marginBottom': 10,
    'display': 'none'
}
card_style2 = {
    'width': 670,
    'marginBottom': 10,
    'display': 'block'
}
card_style2_hide = {
    'width': 670,
    'marginBottom': 10,
    'display': 'none'
}
form_style = {
    'width': '600px',
    # 'margin': '0 auto'
}
number_style = {
    'width': '350px'
}


train_dict = {
    "model": {
        "device": "cuda",
        "mlp1_hidden_dim": 1000,
        "mlp2_hidden_dim": 1000
    },

    "train": {
        "batchsize": 1000,
        "epochs": 1000,
        "initlr": 0.0001,
        "dataset_path": "./datasets",
        "nmols_per_epoch": 25000,
        "rearrange_molgraph_mode": "random"
    },

    "system": {
        "max_atoms": 38,
        "max_cliques": 0.95,
        "max_rings": 8,
        "max_ring_size": 34,
        "max_ring_states": 62,
        "max_node_add_states": 42,
        "max_node_connect_states": 42,
        "ring_cover_rate": 0.97
    },
}

sample_constrain_dict = {
    'sample_constrain': {
        'max_node_steps': 5,
        'max_ring_nodes': 100,
        'temp': 1.0,
        'ring_check_mode': 'easy',
        'constrain_step_dict': {
            '0': {'node add': {}, 'node conn': {}},
            '1': {'node add': {}, 'node conn': {'constrain_connect_node_id': [0]}}
        }
    }
}




model_input = fac.AntdCollapse(
    title='model',
    isOpen=True,
    style=card_style,
    children=fac.AntdForm(
        id='model-input',
        children=[
            fac.AntdFormItem(fac.AntdInput(id="device", value="cuda", disabled=True), label="device"),
            fac.AntdFormItem(fac.AntdInputNumber(id="mlp1_hidden_dim", value=1000, style=number_style),
                             label="mlp1_hidden_dim"),
            fac.AntdFormItem(fac.AntdInputNumber(id="mlp2_hidden_dim", value=1000, style=number_style),
                             label="mlp2_hidden_dim"),
            fac.AntdButton('Update value', id='model-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle')),
            # dcc.Store(id='model-value-setter-store', data={'model': train_dict['model']})
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

train_input = fac.AntdCollapse(
    title='train',
    isOpen=False,
    style=card_style,
    children=fac.AntdForm(
        id='train-input',
        children=[
            fac.AntdFormItem(fac.AntdInputNumber(id="batchsize", value=1000, style=number_style), label="batchsize"),
            fac.AntdFormItem(fac.AntdInputNumber(id='epochs', value=1000, style=number_style), label='epochs'),
            fac.AntdFormItem(fac.AntdInputNumber(id='initlr', value=0.0001, step=0.0001, style=number_style),
                             label='initlr'),
            fac.AntdFormItem(fac.AntdInput(id='dataset_path', value='./datasets'), label='dataset_path'),
            fac.AntdFormItem(fac.AntdInputNumber(id='nmols_per_epoch', value=25000, style=number_style),
                             label='nmols_per_epoch'),
            fac.AntdFormItem(fac.AntdRadioGroup(
                id='rearrange_molgraph_mode',
                options=[{'label': i, 'value': i} for i in ['random', 'fix']],
                defaultValue='random'
            ),
                label='rearrange_molgraph_mode'),
            fac.AntdButton('Update value', id='train-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle')),
            # dcc.Store(id='train-value-setter-store', data={'train': train_dict['train']})
        ],
        labelCol={'span': 10},
        style=form_style
    )
)
system_input = fac.AntdCollapse(
    title='system',
    isOpen=False,
    style=card_style,
    children=fac.AntdForm(
        id='system-input',
        children=[
            fac.AntdFormItem(fac.AntdInputNumber(id="max_atoms", value=38, disabled=True, style=number_style),
                             label="max_atoms"),
            fac.AntdFormItem(
                fac.AntdInputNumber(id='max_cliques', value=0.95, disabled=True, step=0.01, style=number_style),
                label='max_cliques'),
            fac.AntdFormItem(fac.AntdInputNumber(id='max_rings', value=8, disabled=True, style=number_style),
                             label='max_rings'),
            fac.AntdFormItem(fac.AntdInputNumber(id='max_ring_size', value=34, disabled=True, style=number_style),
                             label='max_ring_size'),
            fac.AntdFormItem(fac.AntdInputNumber(id='max_ring_states', value=62, disabled=True, style=number_style),
                             label='max_ring_states'),
            fac.AntdFormItem(fac.AntdInputNumber(id="max_node_add_states", value=42, disabled=True, style=number_style),
                             label="max_node_add_states"),
            fac.AntdFormItem(
                fac.AntdInputNumber(id='max_node_connect_states', value=42, disabled=True, style=number_style),
                label='max_node_connect_states'),
            fac.AntdFormItem(
                fac.AntdInputNumber(id='ring_cover_rate', value=0.97, step=0.01, disabled=True, style=number_style),
                label='ring_cover_rate'),
            fac.AntdButton('Update value', id='system-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle'), disabled=True),
            # dcc.Store(id='system-value-setter-store', data={'system': train_dict['system']})
        ],
        labelCol={'span': 10},
        style=form_style
    )
)

sample_constrain_input = fac.AntdCollapse(
    title='sample_constrain',
    isOpen=False,
    style=card_style,
    children=fac.AntdForm(
        id='sample_constrain-input',
        children=[
            fac.AntdFormItem(fac.AntdInputNumber(id="max_node_steps", value=42, style=number_style),
                             label="max_node_steps"),
            fac.AntdFormItem(fac.AntdInputNumber(id='max_ring_nodes', value=100, style=number_style),
                             label='max_ring_nodes'),
            fac.AntdFormItem(fac.AntdInputNumber(id='temperature', value=1.0, style=number_style), label='temperature'),
            fac.AntdFormItem(fac.AntdRadioGroup(
                id='ring_check_mode',
                options=[{'label': i, 'value': i} for i in ['only ring', 'easy']],
                defaultValue='only ring'
            ), label='ring_check_mode'),
            fac.AntdButton('Update value', id='sample_constrain-button', type='primary',
                           icon=fac.AntdIcon(icon='antd-check-circle')),
            html.Div(id='sample_constrain-message')
        ],
        labelCol={'span': 10},
        style=form_style
    )
)


def apply_value(value, character):
    value = re.split(',|，', re.split(character, value)[1])
    value = [i.strip() for i in value]
    value = [float(i) for i in value] if value[0][0] in "1234567890" else value
    return value


def getter_value(input_data):
    output_dict = {}
    for i in range(len(input_data)):
        k = input_data[i]['props']['label']
        v = input_data[i]['props']['children']['props']['value'] if 'value' in input_data[i]['props']['children'][
            'props'].keys() else input_data[i]['props']['children']['props']['checked']
        if isinstance(v, str) and v.startswith('['):
            v = apply_value(v, '\[|\]')
        elif isinstance(v, str) and v.startswith('('):
            v = apply_value(v, '\(|\)')
            v = tuple(v)
        elif isinstance(v, str) and v.startswith('{'):
            v = json.loads(v)
        output_dict[k] = v
    return output_dict



def getter_rl_general_value(input_data):
    output_dict = {}
    for i in range(len(input_data)):
        k = input_data[i]['props']['label']
        v = input_data[i]['props']['children']['props']['value'] if 'value' in input_data[i]['props']['children'][
            'props'].keys() else input_data[i]['props']['children']['props']['checked']
        if isinstance(v, str) and v.startswith('['):
            v = apply_value(v, '\[|\]')
        elif isinstance(v, str) and v.startswith('('):
            v = apply_value(v, '\(|\)')
            v = tuple(v)
        elif isinstance(v, str) and v.startswith('{'):
            v = json.loads(v)
        output_dict[k] = v
    return output_dict
