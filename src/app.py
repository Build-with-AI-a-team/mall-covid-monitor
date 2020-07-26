'''
File: app.py
File Created: 2020-07-25
Author: Parijat Khan (khanparijat@gmail.com)
-----
Copyright 2020 Parijat Khan
'''

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import time

from floorplan import makeplan

DENSITY_DETECTION = 'Density Detection'
MASK_DETECTION = 'Face-Mask Detection'

API_BASE_URL = "https://a-team-mall-api.herokuapp.com/"

def load_density_data():
    x_coords = []
    y_coords = []
    sizes = []
    density_url = API_BASE_URL + "density"
    
    r = requests.get(density_url)
    if r.status_code == 200:
        content = r.json()
        x_coords = [item['x'] for item in content]
        y_coords = [item['y'] for item in content]
        sizes = [item['count'] for item in content]

    return x_coords, y_coords, sizes

def load_mask_data():
    x_coords = []
    y_coords = []
    masks = []
    nomasks = []
    mask_url = API_BASE_URL + "mask"

    r = requests.get(mask_url)
    if r.status_code == 200:
        content = r.json()
        x_coords = [item['x'] for item in content]
        y_coords = [item['y'] for item in content]
        masks = [item['mask'] for item in content]
        nomasks = [item['nomask'] for item in content]

    return x_coords, y_coords, masks, nomasks


st.title('Mall-monitor by <A-Team>')
st.header('')

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Choose Application',
    (DENSITY_DETECTION, MASK_DETECTION)
)

fig = go.Figure()
mask_fig = go.Figure()

if add_selectbox == DENSITY_DETECTION:
    makeplan(fig)

    # size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40, 60, 20, 10, 5]
    x_coords, y_coords, sizes = load_density_data()

    fig.add_trace(go.Scatter(
        # x=[10, 10, 10, 40, 70, 97, 97, 90, 63, 30, 40, 40, 70, 70],
        # y=[10, 25, 40, 45, 45, 40, 20, 5, 5, 5, 20, 30, 20, 30],
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=sizes,
            sizemode='area',
            sizeref=2.*max(sizes)/(40.**2),
            sizemin=4
        )
    ))

    fig.update_shapes(dict(xref='x', yref='y'))

    fig.update_layout(
        autosize=False,
        width=735,
        height=350,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        showlegend=False
    )

elif add_selectbox == MASK_DETECTION:
    x_coords, y_coords, masks, nomasks = load_mask_data()

    fig.add_trace(go.Bar(x=["ST" + str(i+1) for i in range(len(x_coords))], y=masks, name='Mask'))
    fig.add_trace(go.Bar(x=["ST" + str(i+1) for i in range(len(x_coords))], y=nomasks, name='No Mask'))

    fig.update_layout(
        barmode='stack',
        autosize=False,
        width=735,
        height=350,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        )
    )

st.plotly_chart(fig)        
st.button("Refresh")
    # print(fig.data[-1])

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)

