# Python 3
#
# Natalie Popescu (Adapted from Ziyang Xu)
# Jan 22, 2021
#
# Present results in HTML

import argparse
import os
import json
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go
from subprocess import call

# some setting for plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# helper for checking if a datafile has no data
def is_empty_datafile(filepath):
    handle = open(filepath, 'r')
    for line in handle: 
        if line[:1] == '#':
            continue
        else:
            return False
    return True

class ResultProvider:

    def __init__(self, root):
        self.datafile = os.path.join(root, "summary_total_uses.txt")

    def get_unchecked_indexing(self):
        if os.path.exists(self.datafile) or is_empty_datafile(self.datafile):
            exit("Datafile is empty, need to generate results for Figure 7/Table 3 before visualizing")

        df = open(self.datafile)
        self.app_names = dict()
        self.direct_ui = dict()
        self.indirect_ui = dict()
        self.total_deps = dict()
        self.deps_w_ui = dict()

        for line in df: 
            cols = line.split()
            assert len(cols) == 5

            if cols[0] == 'brotli-decompressor': 
                name = 'brotli-decompressor'
            else: 
                name = cols[0].rsplit('-', 1)[0]

            self.app_names[cols[0]] = name
            self.direct_ui[cols[0]] = cols[1]
            self.indirect_ui[cols[0]] = cols[2]
            self.total_deps[cols[0]] = cols[3]
            self.deps_w_ui[cols[0]] = cols[4]

def get_overview_layout(rp):
    fig = go.Figure(data=[
        go.Bar(name='Direct', 
            x=list(rp.app_names.values()), 
            y=list(rp.direct_ui.values())),
        go.Bar(name='Indirect', 
            x=list(rp.app_names.values()), 
            y=list(rp.indirect_ui.values())),
    ])
    fig.update_layout(barmode='stack')
    call(['orca', 'graph', 
        '-o', 'figure7', 
        '-f', 'pdf', 
        '--width', '900', 
        '--height', '700',
        json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)])

    table = go.Figure(data=[
        go.Table(
            header=dict(values=[
                'Application Name', 
                '# Direct UI',
                '# Indirect UI',
                'Total # Dependencies',
                '# Dependencies with any UI'
            ]),
            cells=dict(values=[
                list(rp.app_names.values()),
                list(rp.direct_ui.values()),
                list(rp.indirect_ui.values()),
                list(rp.total_deps.values()),
                list(rp.deps_w_ui.values())
            ])
        )
    ])
    call(['orca', 'graph', 
        '-o', 'table3', 
        '-f', 'pdf', 
        '--width', '800', 
        '--height', '800',
        json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)])

    layout = html.Div([
        html.Br(),
        html.H3('Unchecked Indexing Usage in Popular Rust Applications'),
        html.Br(),
        dcc.Graph(
            figure=fig
        ),
        html.Br(),
        dcc.Graph(
            figure=table
        )
    ])
    return layout

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", "-r",
            metavar="path",
            type=str,
            required=False,
            default="./criterion_rev_deps/",
            help="root path of scraped crates directory with benchmark results; "\
            "default is ./criterion_rev_deps/")
    parser.add_argument("-p", "--port",
            metavar="num",
            type=str,
            required=False,
            default="8050",
            help="port for Dash server to run; 8050 or 8060 on AWS")
    args = parser.parse_args()
    return args.root, args.port

@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if not pathname:
        return 404
    if pathname == '/':
        layout = get_overview_layout(app._result_provider)
        return layout
    else:
        return 404

if __name__ == '__main__':
    root, port = parseArgs()
    app._result_provider = ResultProvider(root)
    app._result_provider.get_unchecked_indexing()

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Br(),
        html.Div(id='page_content')
    ])
    print(dash.__version__)
    print(plotly.__version__)

    app.run_server(debug=False, host='0.0.0.0', port=port)

