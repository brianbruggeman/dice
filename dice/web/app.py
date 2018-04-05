#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time

import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
from flask import Flask, render_template, request

from dice.parser import parse

app = Flask(__name__)


now = time


# Create the main plot
def create_data(formula, count=1, seed=None):
    start = now()
    formula = f'{count}x{formula}'  # much faster than a list comprehension
    data = pd.DataFrame(parse(formula, seed=seed), columns=['rolls'])
    end = now()
    counts = data[['rolls']].groupby(['rolls']).size()
    counting = now()
    duration = end - start
    print(f'data created in: {duration:>.3f} sec')
    return counts


def create_figure(data_frame, current_feature_name, bins):
    p = Histogram(
        data_frame,
        current_feature_name,
        title=current_feature_name,
        color='Species',
        bins=bins,
        legend='top_right',
        width=600,
        height=400
    )

    # Set the x axis label
    p.xaxis.axis_label = current_feature_name

    # Set the y axis label
    p.yaxis.axis_label = 'Count'
    return p


@app.route('/')
def index():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name is None:
        current_feature_name = "Sepal Length"

    counts = create_data('3d6', count=5000, seed=None)
    import pdb; pdb.set_trace()

    # Create the plot
    plot = create_figure(counts, current_feature_name, 10)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template(
        "index.html",
        title="test1",
        script=script,
        div=div,
        feature_names=['Blah'],
        current_feature_name=current_feature_name
    )


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)
