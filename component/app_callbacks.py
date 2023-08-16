import sys

import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
from .common_layout import mol_dir
sys.path.append("..")
from server import app
from .app_graph import edges


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
        if len(current_nodes) > 1:
            current_nodes.remove({"data": tapNodeData})
            current_edges = [e for e in current_edges if
                             e["data"]["source"] != tapNodeData["id"] and e["data"]["target"] != tapNodeData["id"]]

        for i in range(len(current_nodes)):
            if int(current_nodes[i]["data"]["id"]) > int(tapNodeData["id"]):
                num = int(current_nodes[i]["data"]["id"]) - 1
                current_nodes[i]["data"]["id"] = str(num)
                current_nodes[i]["data"]["label"] = str(num)
        current_edges_new = []
        for i in range(len(current_edges)):
            current_edges[i]["data"]['index'] = str(i)
            if int(current_edges[i]["data"]["source"]) > int(tapNodeData["id"]):
                current_edges[i]["data"]["source"] = str(int(current_edges[i]["data"]["source"]) - 1)
                current_edges[i]["data"]["constrain_connect_node_id"] = [
                    int(tapNodeData["id"]) - 1 if node_id == int(tapNodeData["id"]) else node_id for node_id in
                    current_edges[i]["data"]["constrain_connect_node_id"]]
                current_edges[i]["data"].pop("id")
            if int(current_edges[i]["data"]["target"]) > int(tapNodeData["id"]):
                current_edges[i]["data"]["target"] = str(int(current_edges[i]["data"]["target"]) - 1)
            if current_edges[i]["data"]["source"] != current_edges[i]["data"]["target"]:
                current_edges_new.append(current_edges[i])
        current_edges = current_edges_new
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
        edge_index = max(edges_ids) + 1
        edge_data = edges[0].copy()
        edge_data["data"]["index"] = str(edge_index)
        edge_data["data"]["source"] = selectedNodeData[0]["id"]
        edge_data["data"]["target"] = selectedNodeData[1]["id"]
        current_edges.append(edge_data)
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
def define_value(select_attr, input_node_value):
    if select_attr[1] in eval_type:
        output_value = eval(input_node_value)
    else:
        output_value = input_node_value
    return output_value

def getter_graph_value_dict(current_nodes):
    output_dict = {}
    for node_data in current_nodes:
        if 'specific_nodefile' not in node_data['data']['node add'].keys():
            output_dict[node_data['data']['id']] = {'node add': node_data['data']['node add'],
                                                    'node conn': node_data['data']['node conn']}
        else:
            node_data['data']['node add']['specific_nodefile'] = f"{mol_dir}/{node_data['data']['node add']['specific_nodefile']}"
    return output_dict


@app.callback(Output("select-node", "value"),
              Output('cytoscape-elements-callbacks', 'elements', allow_duplicate=True),
              Output('cytoscape-tapNodeData-json', 'children', allow_duplicate=True),
              Output('enter-value-button', "nClicks", allow_duplicate=True),
              Output('graph-dropdown-message', 'children'),
              Output('graph-value-setter-store', 'data'),
              Input('enter-value-button', "nClicks"),
              Input('cytoscape-elements-callbacks', 'tapNodeData'),
              State("constrain-attr", "value"),
              State('constrain-value', 'value'),
              State('constrain-value2', 'checked'),
              State('cytoscape-elements-callbacks', 'elements'),
              State('graph-value-setter-store', 'data'),
              prevent_initial_call=True)
def update_node_attributes(nClicks, tapNodeData, select_attr, node_value, node_checked, elements, previous_data):
    data = previous_data
    graph_dropdown_message = []
    show_data = show_TapNodeData(tapNodeData) if tapNodeData else []
    select_node = tapNodeData["id"] if tapNodeData else "0"
    current_nodes, node_ids = get_current_nodes(elements)
    current_edges, edges_ids = get_current_edges(elements)
    if nClicks:
        if select_attr[1] != 'force_step':
            current_nodes[int(select_node)]["data"][select_attr[0]][select_attr[1]] = define_value(select_attr, node_value)
        else:
            current_nodes[int(select_node)]["data"][select_attr[0]][select_attr[1]] = node_checked
        graph_dropdown_message = fac.AntdMessage(content='Update node attribute successfully', type='success')
        tapNodeData = current_nodes[int(select_node)]['data']
        data['sample_constrain']['constrain_step_dict'].update(getter_graph_value_dict(current_nodes))
        show_data = show_TapNodeData(tapNodeData)
    return select_node, current_nodes + current_edges, show_data, 0, graph_dropdown_message, data


