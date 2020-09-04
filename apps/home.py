import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to Pitti ",
                            className="text-center main_title"), className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H4(
                children='A personal research topic library builder '), className="text-center sub_title")
        ]),

        html.Br(),
        html.Br(),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H5(children='Single Article Explore',
                                               className="text-center"),
                                       dbc.Button("Click",
                                                  href="/single_article",
                                                  color="primary",
                                                  className="mt-3 home_button"),
                                       ],
                             body=True, color="dark", outline=True, className="home_click_box"), width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H5(children='Single Topic Explore',
                                               className="text-center"),
                                       dbc.Button("Click",
                                                  href="/home",
                                                  color="primary",
                                                  className="mt-3 home_button"),
                                       ],
                             body=True, color="dark", outline=True, className="home_click_box"), width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H5(children='Library Explore',
                                               className="text-center"),
                                       dbc.Button("Click",
                                                  href="/home",
                                                  color="primary",
                                                  className="mt-3 home_button"),

                                       ],
                             body=True, color="dark", outline=True, className="home_click_box"), width=4, className="mb-4 ")
        ], className="mb-5"),


    ])

])


# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
