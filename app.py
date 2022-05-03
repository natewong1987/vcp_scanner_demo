import pandas as pd
import plotly.graph_objects as go
import streamlit as st

#st.write("data_series_path:", st.secrets["data_series"])
st.write("loading from secret")
#df = pd.read_csv('Data/NVDA.csv')
#url = st.secrets["data_series"]

import streamlit as st
#from gsheetsdb import connect

# Create a connection object.
#conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600,
#https://discuss.streamlit.io/t/secrets-management-unhashable-in-st-cache/15409

import requests

SIGNAL_POINTER_FILE = "signal_pointer_file.csv"
DOWNLOADED_DATA_DIR = "./Downloaded_data"
SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']

@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def download_all_data():
    print('RUNNING DOWNLOAD ALL DATA')
    from gdrive_download_utils import download_signal_pointer_file, download_all_signals
    download_signal_pointer_file(SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE)
    download_all_signals(SIGNAL_POINTER_FILE, DOWNLOADED_DATA_DIR)
    pass

@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_data():
    import pandas as pd
    nvda_df = pd.read_csv(DOWNLOADED_DATA_DIR +'/NFLX.csv')
    return nvda_df

download_all_data()
df = load_data()

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
st.plotly_chart(fig)
st.write('Enter welcome to streamlit deploy example')
txt = st.text_input(label='Enter something here')
st.write(txt)

# test streamlit tag
from streamlit_tags import st_tags
keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven',
                 'eight', 'nine', 'three',
                 'eleven', 'ten', 'four'],
    maxtags = 4,
    key='1')
#https://carpentries-incubator.github.io/python-interactive-data-visualizations/08-publish-your-app/index.html
#pip3 freeze > requirements.txt