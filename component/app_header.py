import dash_bootstrap_components as dbc
import sys
sys.path.append("..")
from server import app


button_howto = dbc.Button(
    "View Code on github",
    outline=True,
    color="primary",
    href="https://github.com/MingyuanXu/Tree-Invent/tree/main",
    id="gh-link",
    style={"text-transform": "none"},
)
button_Community = dbc.Button(
    "TreeInvent-Community",
    outline=True,
    color="primary",
    href="https://github.com/MingyuanXu/TreeInvent-Community/tree/master",
    id="gh-link2",
    style={"text-transform": "none"},
)


# Define Header Layout
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [dbc.Col(dbc.NavbarBrand("TreeInvent Website")),],
                align="center",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse(
                            dbc.Nav(
                                [dbc.NavItem(button_howto), dbc.NavItem(button_Community)],
                                className="ml-auto",
                                navbar=True,
                            ),
                            id="navbar-collapse",
                            navbar=True,
                        ),
                    ]
                ),
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
)
