import dash
import pandas as pd
import numpy as np
import pathlib
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from util.helpers import (make_dash_table, create_plot,
                          extract_text_from_url,
                          gen_summary_from_text,
                          gen_summary_from_sentences)
from app import app


DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath("data").resolve()

DATA_FILE = DATA_PATH.joinpath("test.txt")




layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Enter an url or text to start exploring ",
                            className="text-center "), className="mb-5 mt-5")]),

        html.Br(),
        # Textarea box for entering url for text extraction
        html.Div([
            dcc.Textarea(
                id='textarea-url',
                value='https://en.wikipedia.org/wiki/Topic_model',
                style={'width': '100%', 'height': '100%'},
            ),

            #html.Div(id='textarea-url-output', style={'whiteSpace': 'pre-line'})
        ],
            className="app__url_enter_box",
        ),
        html.Div([
            html.Button('Extract', id='textarea-url-button',
                        n_clicks=0),
        ], className="app__button",
        ),
        dbc.Tooltip(  # this adds hover text on extract button
            "Long text may take a few seconds to extract",
            target="textarea-url-button",
        ),

        html.Br(),
        html.Div([
            html.Span("Text to be analyzed: "),
        ],
            className="app__subheader",
        ),

        html.Br(),
        html.Div(
            [
                html.Div(id='title-output'),
            ],
            className="app__subheader",
        ),
        html.Div(
            [
                html.Div(id='text-output'),
            ],
            className="app__text_output_box",
        ),

        html.Br(),
        html.Div([
            html.Span("Summary: "),
        ],
            className="app__subheader",
        ),
        html.Br(),
        html.Div(
            [
                html.Div(id='summary-output'),
            ],
            className="app__text_summary_box",
        ),

        html.Br(),

        html.Div([html.Span("Wordcloud: ")], className="app__subheader",),
        html.Br(),
        html.Div(
            [dcc.Graph(id="single-text-wordcloud"),],
            className="app__wordcloud"),

        html.Br(),
        html.Div([html.Span("Treemap: ")], className="app__subheader",),
        html.Br(),
        html.Div(
            [dcc.Graph(id="single-text-treemap"),],
            className="app__wordcloud"),
    ])

])


def plotly_wordcloud(text):
    """A function that returns figure data for wordcloud"""
    list_words = text.split(" ")

    if len(list_words) < 1:
        return {}

    #mask = np.array(Image.open('assets/talk.png'))
    font_path = 'assets/MilkyNice-Clean.otf'
    word_cloud = WordCloud(stopwords=set(STOPWORDS),
                        background_color="white", font_path=font_path,
                        max_words=2000, max_font_size=256,
                        random_state=42,
                        #mask=mask, width=mask.shape[1],vheight=mask.shape[0]
                        )
    word_cloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 60)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                #"range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                #"range": [-100, 450],
            },
            "margin": dict(t=2, b=2, l=2, r=2, pad=1),
            "hovermode": "closest",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}

    word_list_top = word_list[:60]
    word_list_top.reverse()
    freq_list_top = freq_list[:60]
    freq_list_top.reverse()
    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top),
        values=freq_list_top,
        marker=dict(colorscale='Blackbody'),
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}

    return wordcloud_figure_data, treemap_figure


def read_text_from_file(pth_text_file):

    text_list = []
    with open(pth_text_file) as f:
        for line in f:
            text_list.append(line)
    return " ".join(text_list)


@app.callback([
    Output("title-output", "children"),
    Output("text-output", "children"),
    Output("summary-output", "children"),
    Output("single-text-wordcloud", "figure"),
    Output("single-text-treemap", "figure"),
],
    [Input("textarea-url-button", "n_clicks")],
    [State('textarea-url', 'value')]
)
def process_input_box(n_clicks, url_values):
    """
    :params textarea-url: url link
    """
    if n_clicks > 0:

        if url_values.startswith('http'):
            # extract text from url
            title, text = extract_text_from_url(url_values)

            file = open(DATA_FILE, "w")
            file.write(text)
            #t2s = gen_sound_from_text(text, outputfile=AUDIO_FILE)
            # t2s.text2sound()
            # t2s.save_sound_2_mp3()

        else:
            text = url_values
            title = "NA"

            file = open(DATA_FILE, "w")
            file.write(text)

        summary = gen_summary_from_text(text)
        wordcloud_data, treemap_figure = plotly_wordcloud(text)

        #summary_in_html_display = []
        # for ss in list_summary:

        #    line = html.P(ss)
        #    summary_in_html_display.append(line)

        #summary = html.Div([summary_in_html_display])

        return [title, text, summary, wordcloud_data, treemap_figure]
    else:
        text = read_text_from_file(DATA_FILE)
        wordcloud_data, treemap_figure = plotly_wordcloud(text)
        return [" ", " ", " ", wordcloud_data, treemap_figure]
