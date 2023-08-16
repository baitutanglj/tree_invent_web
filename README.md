# The web version of the [Tree-Invent](https://github.com/MingyuanXu/Tree-Invent/tree/main) program is used

## Conda environment Dependencies
 - dash >= 2.11.1
 - dash-bio >=1.0.2
 - dash-bootstrap-components >= 1.4.1
 - dash-core-components >= 2.0.0
 - dash-cytoscape >= 0.3.0
 - dash-html-components >=2.0.0
 - feffery-antd-components >= 0.2.8
 - rdkit >= 2021.09.1
 - waitress >=2.1.2
 - flask >=2.1.3

## Start the server
note: Make mol_dir and upload_dir variables in the component/common_layout.py file before starting the server
```
method 1: python app.py
method 2: waitress-serve --port=8008 app:app.server
```