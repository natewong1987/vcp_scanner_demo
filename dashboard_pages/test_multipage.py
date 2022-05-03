import streamlit as st
import numpy as np
import pandas as pd

def strdate2date(str_date):
    import datetime
    return datetime.datetime.strptime(str_date,'%Y-%m-%d').date()

def app():
    st.write('hello world')
    from utils.load_data import load_time_series_data
    import plotly.graph_objects as go
    df = load_time_series_data('NVDA')

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