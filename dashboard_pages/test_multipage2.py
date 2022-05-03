import streamlit as st
import numpy as np
import pandas as pd


def strdate2date(str_date):
    import datetime
    return datetime.datetime.strptime(str_date,'%Y-%m-%d').date()


def plot_time_series(df):
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])

    fig.update_layout(
        autosize=False,
        width=800,
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),

    )
    fig.update_xaxes(showgrid=True, gridwidth=0.01, gridcolor='Black',automargin=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='Black',automargin=False)
    st.plotly_chart(fig)
    pass


def display_signals(ticker, this_ticker_signals):
    import plotly.express as px
    import streamlit as st
    st.write("## Factor Profile")
    fig = px.bar(this_ticker_signals.T, orientation='h', labels={'index': 'factor name', 'value':'factor ranks'}, width=800)
    fig.update_layout(
        showlegend=False,
        title={
            'text': "factor rank for " + ticker,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.write(fig)
    pass

def get_this_ticker_factors():
    fake_factors_df = pd.DataFrame()
    fake_factors_df['Momentum'] = [100]
    fake_factors_df['Value'] = [50]
    fake_factors_df['Quality'] = [30]
    fake_factors_df['Size'] = [10]
    fake_factors_df['Vol'] = [20]
    fake_factors_df['1'] = [100]
    fake_factors_df['2'] = [50]
    fake_factors_df['3'] = [30]
    fake_factors_df['4'] = [10]
    fake_factors_df['5'] = [20]
    fake_factors_df['12'] = [100]
    fake_factors_df['22'] = [50]
    fake_factors_df['32'] = [30]
    fake_factors_df['42'] = [10]
    fake_factors_df['52'] = [20]
    fake_factors_df['12'] = [100]
    fake_factors_df['22'] = [50]
    fake_factors_df['32'] = [30]
    fake_factors_df['42'] = [10]
    fake_factors_df['52'] = [20]
    return fake_factors_df


def export_signals(ticker, this_ticker_signals):
    df_to_export = pd.DataFrame(this_ticker_signals.copy(deep=True))
    df_to_export['ticker'] = ticker
    df_to_export.set_index(['ticker'],inplace=True)
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_to_export)
    import datetime
    st.download_button(
        label="Export " + ticker +" signals as csv",
        data=csv,
        file_name=ticker.upper()+'_signals_'+datetime.datetime.today().strftime("%Y-%m-%d")+'.csv',
        mime='text/csv',
    )


def app():
    st.write('hello world 2')
    from utils.load_data import load_time_series_data, load_static_data

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

    df = load_time_series_data(ticker)
    this_ticker_signals = get_this_ticker_factors()

    static_data_df = load_static_data(ticker)

    # step 1 plot historical time series
    plot_time_series(df)

    def display_stat_data(static_data_df):

        st.dataframe(static_data_df)
        st.write("## Description")

        st.write(static_data_df['DESCRIPTION'][0])
        pass

    display_stat_data(static_data_df)

    # step 2 display signals
    display_signals(ticker, this_ticker_signals)

    # step 3 allow for signal
    export_signals(ticker, this_ticker_signals)

    #st.write('Enter welcome to streamlit deploy example')
    #txt = st.text_input(label='Enter something here')
    #st.write(txt)

    #static_data = pd.Series()
    #static_data['Name'] = ticker
    #st.write(static_data)