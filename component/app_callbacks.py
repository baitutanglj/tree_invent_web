import sys

import dash
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State

from .common_layout import mol_dir, constrain_number_type, constrain_list_type, constrain_list_list_type, \
    constrain_dict_type, error_message

sys.path.append("..")
from server import app


def get_current_nodes(elements):
    """Returns nodes that are present in Cytoscape"""
    # get current graph nodes
    current_nodes = [ele for ele in elements if 'source' not in ele['data']]
    current_edges = [ele for ele in elements if 'source' in ele['data']]
    for i, n in enumerate(current_nodes):
        constrain_connect_node_id = [int(edge['data']['source']) for edge in current_edges if
                                     edge['data']['target'] == n['data']['id']]
        if constrain_connect_node_id != []:
            current_nodes[i]['data']['node conn']['constrain_connect_node_id'] = constrain_connect_node_id

    node_ids = {int(n['data']['id']) for n in current_nodes}

    return current_nodes, node_ids


def get_current_edges(elements):
    current_edges = [ele for ele in elements if 'source' in ele['data']]
    edges_ids = {int(n['data']['index']) for n in current_edges}

    return current_edges, edges_ids


##===================add/remove node by tapNodeData=======================
@app.callback(Output('cytoscape-elements-callbacks', 'elements'),
              Input('btn-add-node', 'n_clicks_timestamp'),
              Input('btn-remove-node', 'n_clicks_timestamp'),
              State('cytoscape-elements-callbacks', 'tapNodeData'),
              State('cytoscape-elements-callbacks', 'elements'),
              prevent_initial_call=True)
def update_elements(btn_add, btn_remove, tapNodeData, elements):
    current_nodes, node_ids = get_current_nodes(elements)
    current_edges, edges_ids = get_current_edges(elements)
    if int(btn_add) > int(btn_remove) and tapNodeData is not None:
        node_id = max(node_ids) + 1
        node_data = {'data': {'id': str(node_id), 'label': str(node_id), 'node add': {},
                              'node conn': {'constrain_connect_node_id': tapNodeData["id"]}}}
        current_nodes.append(node_data)

        edge_index = max(edges_ids) + 1 if len(edges_ids) > 0 else 0
        edge_data = {"data": {"index": str(edge_index), "source": tapNodeData["id"], "target": str(node_id)}}
        current_edges.append(edge_data)

    elif int(btn_remove) > int(btn_add) and tapNodeData is not None:
        print('current_nodes', current_nodes)
        print('current_edges', current_edges)
        print('tapNodeData', tapNodeData)
        current_nodes.remove({"data": tapNodeData})
        current_edges = [e for e in current_edges if
                         e["data"]["source"] != tapNodeData["id"] and e["data"]["target"] != tapNodeData["id"]]

        current_edges_new = []
        for i, edge in enumerate(current_edges):
            edge = edge.copy()
            edge["data"]['index'] = str(i)
            edge["data"].pop("id") if 'id' in edge['data'].keys() else edge["data"]
            if int(edge["data"]["source"]) > int(tapNodeData["id"]):
                edge["data"]["source"] = str(int(edge["data"]["source"]) - 1)
            if int(edge["data"]["target"]) > int(tapNodeData["id"]):
                edge["data"]["target"] = str(int(edge["data"]["target"]) - 1)
            if edge["data"]["source"] != edge["data"]["target"]:
                current_edges_new.append(edge)

        current_nodes_new = []
        for i, node in enumerate(current_nodes):
            if int(node["data"]["id"]) > int(tapNodeData["id"]):
                node['data']['node conn'].pop('constrain_connect_node_id') if 'constrain_connect_node_id' in \
                                                                              node['data'][
                                                                                  'node conn'].keys() else node['data'][
                    'node conn']
                num = int(node["data"]["id"]) - 1
                node["data"]["id"] = str(num)
                node["data"]["label"] = str(num)
                constrain_connect_node_id = [edge['data']['source'] for edge in current_edges if
                                             edge['data']['target'] == node["data"]["id"]]
                if len(constrain_connect_node_id) > 0:
                    node["data"]['node conn']['constrain_connect_node_id'] = constrain_connect_node_id

            current_nodes_new.append(node)

        current_nodes, current_edges = current_nodes_new, current_edges_new

    return current_nodes + current_edges


##===================add edge by tapEdgeData / remove edge by selectedNodeData=======================
@app.callback(
    Output('cytoscape-elements-callbacks', 'elements', allow_duplicate=True),
    Input('btn-add-edge', 'n_clicks_timestamp'),
    Input('btn-remove-edge', 'n_clicks_timestamp'),
    State('cytoscape-elements-callbacks', 'tapEdgeData'),
    State('cytoscape-elements-callbacks', 'selectedNodeData'),
    State('cytoscape-elements-callbacks', 'elements'),
    prevent_initial_call=True)
def del_edges(btn_add, btn_remove, tapEdgeData, selectedNodeData, elements):
    current_nodes, node_ids = get_current_nodes(elements)
    current_edges, edges_ids = get_current_edges(elements)
    if int(btn_remove) > int(btn_add) and tapEdgeData is not None:
        current_edges = [e for e in current_edges if e["data"]["index"] != tapEdgeData["index"]]
        for i in range(len(current_edges)):
            current_edges[i]["data"]['index'] = str(i)

    elif int(btn_add) > int(btn_remove) and selectedNodeData is not None:
        if ('constrain_connect_node_id' in selectedNodeData[0]['node conn'].keys()) and (
                'constrain_connect_node_id' not in selectedNodeData[1]['node conn'].keys()):
            edge_index = max(edges_ids) + 1
            edge_data = {"data": {"index": str(edge_index),
                                  "source": selectedNodeData[0]["id"],
                                  "target": selectedNodeData[1]["id"]}}
            current_edges.append(edge_data)

        elif ('constrain_connect_node_id' not in selectedNodeData[0]['node conn'].keys()) and (
                'constrain_connect_node_id' in selectedNodeData[1]['node conn'].keys()):
            edge_index = max(edges_ids) + 1
            edge_data = {"data": {"index": str(edge_index),
                                  "source": selectedNodeData[1]["id"],
                                  "target": selectedNodeData[0]["id"]}}
            current_edges.append(edge_data)

        elif ('constrain_connect_node_id' not in selectedNodeData[0]['node conn'].keys()) and (
                'constrain_connect_node_id' not in selectedNodeData[1]['node conn'].keys()):
            edge_index = max(edges_ids) + 1
            edge_data = {"data": {"index": str(edge_index),
                                  "source": selectedNodeData[0]["id"],
                                  "target": selectedNodeData[1]["id"]}}
            current_edges.append(edge_data)
        else:
            pass

    return current_nodes + current_edges


##===================enter value==========================
def show_TapNodeData(data):
    return fac.AntdDescriptions(
        [
            fac.AntdDescriptionItem(
                data['id'],
                label='node'
            ),
            fac.AntdDescriptionItem(
                str(data['node add']),
                label='node add'
            ),
            fac.AntdDescriptionItem(
                str(data['node conn']),
                label='node conn'
            ),
        ],
        # title='描述列表示例',
        bordered=True,
        layout='vertical',
        labelStyle={
            'fontWeight': 'bold'
        }
    )


##========================update node value===============================
eval_type = [
    "max_anum_per_atomtype", "min_anum_per_atomtype",
    "constrain_connect_node_id", "saturation_atomid_list", "constrain_connect_atom_id",
    'constrain_connect_bond_type', "constrain_connect_atomic_type"]

# constrain_number_type, constrain_list_type, constrain_list_list_type, constrain_dict_type


import ast


def define_value(select_attr, input_node_value):
    k, v = select_attr[1], input_node_value
    if k in constrain_number_type:
        return v

    elif k in constrain_list_list_type:
        if v.startswith("[["):
            try:
                v = ast.literal_eval(v)
            except:
                v = None
        else:
            v = None

    elif k in constrain_list_type:
        if v.startswith("["):
            try:
                v = ast.literal_eval(v)
            except:
                v = None
        else:
            return None

    elif k in constrain_dict_type:
        if v.startswith('{'):
            try:
                v = ast.literal_eval(v)
            except:
                v = None
        else:
            return None

    return v


# def define_value(select_attr, input_node_value):
#     if select_attr[1] in eval_type:
#         try:
#             output_value = eval(input_node_value)
#         except:
#             return None
#     else:
#         output_value = input_node_value
#
#     if select_attr[1] in constrain_number_type and not isinstance(output_value, int) and not isinstance(output_value, float):
#         return None
#     elif select_attr[1] in constrain_list_type and not isinstance(output_value, list):
#         return None
#     elif select_attr[1] in constrain_list_list_type and not isinstance(output_value, list) and isinstance(output_value[0], list):
#         return None
#     elif select_attr[1] in constrain_dict_type and not isinstance(output_value, dict):
#         return None
#     else:
#         return output_value

def getter_graph_value_dict(current_nodes):
    output_dict = {}
    for node_data in current_nodes:
        output_dict[node_data['data']['id']] = {'node add': node_data['data']['node add'],
                                                'node conn': node_data['data']['node conn']}
        if 'specific_nodefile' in node_data['data']['node add'].keys():
            if mol_dir not in node_data['data']['node add']['specific_nodefile']:
                node_data['data']['node add']['specific_nodefile'] = f"{mol_dir}/{node_data['data']['node add']['specific_nodefile']}"
    return output_dict


@app.callback(Output("select-node", "value"),
              Output('cytoscape-elements-callbacks', 'elements', allow_duplicate=True),
              Output('cytoscape-tapNodeData-json', 'children', allow_duplicate=True),
              Output('enter-value-button', "nClicks", allow_duplicate=True),
              Output('graph-dropdown-message', 'children'),
              Output('constrain-item', 'validateStatus'),
              # Output('constrain-value', 'value', allow_duplicate=True),
              # Output('constrain-attr', 'value'),
              Input('enter-value-button', "nClicks"),
              Input('cytoscape-elements-callbacks', 'tapNodeData'),
              State("constrain-attr", "value"),
              State('constrain-value', 'value'),
              State('constrain-value2', 'checked'),
              State('constrain-state', 'value'),
              State('cytoscape-elements-callbacks', 'elements'),
              prevent_initial_call=True)
def update_node_attributes(nClicks, tapNodeData, select_attr, node_value, node_checked, constrain_state, elements):
    graph_dropdown_message = []
    constrain_value_state = None
    show_data = show_TapNodeData(tapNodeData) if tapNodeData else []
    select_node = tapNodeData["id"] if tapNodeData else "0"
    current_nodes, node_ids = get_current_nodes(elements)
    current_edges, edges_ids = get_current_edges(elements)
    # print('current_nodes', current_nodes)
    if nClicks:
        if select_attr is not None:
            if constrain_state=='add':
                if select_attr[1] != 'force_step':
                    update_node_value = define_value(select_attr, node_value)
                    if update_node_value is not None:
                        current_nodes[int(select_node)]["data"][select_attr[0]][select_attr[1]] = update_node_value
                        graph_dropdown_message = fac.AntdMessage(content='Add node attribute successfully', type='success')
                        constrain_value_state = 'success'
                    else:
                        graph_dropdown_message = error_message
                        # graph_dropdown_message = fac.AntdModal(content='Please enter the correct constrain value!',
                        #                                        title='Update value error')
                        constrain_value_state = 'error'
                else:
                    current_nodes[int(select_node)]["data"][select_attr[0]][select_attr[1]] = node_checked
                    graph_dropdown_message = fac.AntdMessage(content='Add node attribute successfully', type='success')

            else:
                if select_attr[1] in current_nodes[int(select_node)]["data"][select_attr[0]].keys():
                    current_nodes[int(select_node)]["data"][select_attr[0]].pop(select_attr[1])
                    graph_dropdown_message = fac.AntdMessage(content='Delete node attribute successfully', type='success')
                else:
                    graph_dropdown_message = fac.AntdMessage(
                        content=f"Constrain attribute:{select_attr[1]} not in current node", type='error')
        else:
            graph_dropdown_message = fac.AntdMessage(content='Please select a constrain!', type='error')
            return select_node, dash.no_update, show_data, 0, graph_dropdown_message, constrain_value_state

        tapNodeData = current_nodes[int(select_node)]['data']
        show_data = show_TapNodeData(tapNodeData)
    return select_node, current_nodes + current_edges, show_data, 0, graph_dropdown_message, constrain_value_state


##===================update graph-value-setter-store=====================
@app.callback(
    Output('graph-value-setter-store', 'data'),
    Input('cytoscape-elements-callbacks', 'elements'),
    State('graph-value-setter-store', 'data'),
    prevent_initial_call=True
)
def update_graph_value(elements, previous_data):
    data = previous_data
    current_nodes, node_ids = get_current_nodes(elements)
    data['sample_constrain']['constrain_step_dict'].update(getter_graph_value_dict(current_nodes))
    return data



