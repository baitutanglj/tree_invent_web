from dash import html, dcc
import dash_bootstrap_components as dbc
from server import app
from component.app_header import header
from component.app_train import train_layout
from component.app_sample import sample_layout
import component.app_callbacks
import component.app_train
import component.app_graph


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '12px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#808b96',
    'color': 'white',
    'padding': '6px'
}


app.layout = html.Div([
    header,
    dcc.Tabs(
        id="app-tabs",
        value="tab1",
        className="custom-tabs",
        children=[
            dcc.Tab(
                id="train-tab",
                label='Generate json file for model training',
                value="tab1",
                className="custom-tab",
                selected_className="custom-tab--selected",
                style=tab_style,
                selected_style=tab_selected_style,
                children=dbc.Container(train_layout)


            ),
            dcc.Tab(
                id="sample-tab",
                label='Generate json file for model sampling',
                value="tab2",
                className="custom-tab",
                selected_className="custom-tab--selected",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[sample_layout]
            ),

        ]),
])

if __name__ == '__main__':
    app.run(debug=True, port=8008)