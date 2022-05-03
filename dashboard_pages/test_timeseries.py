import streamlit as st
import numpy as np
import pandas as pd


def set_up_time_series_plot(ticker, ohlcv_df):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    #import matplotlib.pyplot as plt
    import plotly.io as pio
    #plt.rcParams['figure.figsize'] = [12, 7]
    #plt.rc('font', size=14)

    pio.templates.default = "plotly_dark"

    # creating subplot, 2x1, shared x-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2, row_heights=[0.7, 0.3])

    #####################
    #####################
    colors = []
    INCREASING_COLOR = "GREEN"
    DECREASING_COLOR = "RED"
    for i in range(len(ohlcv_df.close)):
        if i != 0:
            if ohlcv_df.close[i] > ohlcv_df.close[i - 1]:
                colors.append(INCREASING_COLOR)
            else:
                colors.append(DECREASING_COLOR)
        else:
            colors.append(DECREASING_COLOR)

    # plot candles
    fig.add_trace(go.Candlestick(x=ohlcv_df['date'], open=ohlcv_df['open'], high=ohlcv_df['high'], low=ohlcv_df['low'],
                                 close=ohlcv_df['close'], name=ticker), row=1, col=1)

    # plot volume bar
    fig.add_trace(go.Bar(x=ohlcv_df['date'], y=ohlcv_df['volume'], name='volume', marker_color=colors), row=2, col=1)
    fig.add_trace(go.Scatter(x=ohlcv_df['date'], y=ohlcv_df['volume'].rolling(50).mean(), name='volume sma(50)',mode='lines'), row=2, col=1)
    return fig


def app():
    st.write('Testing load time series')
    from utils.load_data import load_time_series_data_refintiv

    ticker_universe = ['AAPL','FB','NFLX','NVDA']
    ticker = ticker_universe[0]
    from streamlit_tags import st_tags
    keywords = st_tags(
        label='',## Enter Keywords:',
        text='Press enter ticker for lookup',
        value=[ticker],
        suggestions = ticker_universe,
        maxtags = 1,
        )
    if len(keywords) > 0:
        if keywords[0] in ticker_universe:
            st.write(keywords[0])
            ticker = keywords[0].upper()
        else:
            st.write("PLEASE CHECK TICKER")
    else:
        st.write("KEYWORD LIST IS EMPTY")

    ohlcv_df = load_time_series_data_refintiv(ticker)
    fig = set_up_time_series_plot(ticker, ohlcv_df)
    st.plotly_chart(fig)