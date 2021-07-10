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
import plotly.express as px
import pandas as pd
import math

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

    # complete object has the following fields: 
    # - datafile

    def __init__(self, root):
        self.datafile = os.path.join(root, "summary_total_uses.txt")

    def get_unchecked_indexing(self):
        if is_empty_datafile(self.datafile):
            exit("Datafile is empty, need to generate results for Figure 7/Table 3 before visualizing")

        df = open(self.datafile)
        #self.data = dict()
        self.direct_ui = dict()
        self.indirect_ui = dict()
        #self.total_deps = dict()
        #self.deps_w_ui = dict()

        for line in df: 
            cols = line.split()
            print(cols)
            assert len(cols) == 5
            #    "Direct UI": cols[1], 
            #    "Indirect UI": cols[2], 
            #    "Total Deps": cols[3],
            #    "Deps w UI": cols[4]
            self.direct_ui[cols[0]] = cols[1]
            self.indirect_ui[cols[0]] = cols[2]
            #self.total_deps[cols[0]] = cols[3]
            #self.deps_w_ui[cols[0]] = cols[4]
            #self.data[cols[0]] = [cols[1], cols[2]] #, cols[3], cols[4]]

def get_overview_layout(rp):
    fig_ui = go.Figure(data=[
        go.Bar(name='Direct', 
            x=list(rp.direct_ui.keys()), 
            y=list(rp.direct_ui.values())),
        go.Bar(name='Indirect', 
            x=list(rp.direct_ui.keys()), 
            y=list(rp.indirect_ui.values())),
    ])
    fig_ui.update_layout(barmode='stack')

    layout = html.Div([
        html.Br(),
        html.H3('Unchecked Indexing Usage in Popular Rust Applications'),
        html.Br(),
        dcc.Graph(
            id='ui_usage',
            figure=fig_ui
        ),
        html.Br(),
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
        pathname = '/passOverview'
    if pathname == '/passOverview':
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
        dcc.Link('Results Overview', href='/passOverview'),
        html.Br(),
        html.Div(id='page_content')
    ])
    print(dash.__version__)
    print(plotly.__version__)

    app.run_server(debug=False, host='0.0.0.0', port=port)

