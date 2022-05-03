import streamlit as st


def select_ticker():
    ticker = st.session_state.ticker_universe[0].upper()

    from streamlit_tags import st_tags
    keywords = st_tags(
        label='',## Enter Keywords:',
        text='Press enter ticker for lookup',
        value=[ticker],
        suggestions = st.session_state.ticker_universe,
        maxtags = 1,
        )
    if len(keywords) > 0:
        if keywords[0].upper() in st.session_state.ticker_universe:
            #st.write(keywords[0])
            ticker = keywords[0].upper()
        else:
            st.write("PLEASE CHECK TICKER")
            return ticker
    else:
        st.write("KEYWORD LIST IS EMPTY")
    return ticker


def app():
    import pandas as pd
    import datetime
    import streamlit as st

    from utils.load_data import load_STOCKBASIS
    from utils.load_data import load_time_series_data_refintiv
    stockbasis_df = load_STOCKBASIS()

    col1, col2 = st.columns([2.5,1])

    with col1:
        import datetime
        ticker = select_ticker()

        df = load_time_series_data_refintiv(ticker)
        #st.write(df)
        default_date = st.session_state.data_as_of_date
        selected_date = st.date_input("Select Date", default_date, min_value = df.iloc[0]['date'], max_value=df.iloc[-1]['date'])

        st.write('Selected date:', selected_date)

        dt = datetime.datetime(year=selected_date.year, month=selected_date.month,day=selected_date.day)

        # step 1 plot historical time series
        from utils.vcp_plottings import set_up_time_series_plot, clean_up_axis
        # note we subset datahere.
        #todo this is not fast enough (need to cache and speed it up
        df_in = df[(df['date'] >= dt-datetime.timedelta(days=500)) & (df['date'] <= dt)]
        df_in.reset_index(inplace=True)

        fig = set_up_time_series_plot(ticker, df_in)
        fig, clean_up_axis(fig, ticker, str(selected_date))
        st.plotly_chart(fig)

    with col2:
        st.write("# "+ticker)
        st.write("Industry: " + stockbasis_df.loc[ticker]["TR.GICSINDUSTRY"])
        st.write("Industry Group: " + stockbasis_df.loc[ticker]["TR.GICSINDUSTRYGROUP"])
        st.write("Sector: " + stockbasis_df.loc[ticker]["TR.GICSSECTOR"])
        st.write('-------')

    # step 2 plot factors
    col1, col2, col3 = st.columns(3)
    col1.metric("Relative Strength", round(stockbasis_df.loc[ticker]['RSSCORE'],2), delta=round(stockbasis_df.loc[ticker]['RSSCORE_D1'],2))
    col2.metric("SCTR", round(stockbasis_df.loc[ticker]['SCTRSCORE'],2), delta=round(stockbasis_df.loc[ticker]['SCTRSCORE_D1'],2))
    col3.metric("MRSQUARE", round(stockbasis_df.loc[ticker]['MRSQUARE'],2), delta=round(stockbasis_df.loc[ticker]['SCTRSCORE_D1'],2))

    st.write('-------')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### RS score sector")
        st.write("Rank within sector: ", round(stockbasis_df.loc[ticker]["RSSCORE_SECTOR_RANK"], 2))
        st.write("Sector median: ", round(stockbasis_df.loc[ticker]["RSSCORE_SECTOR_MEDIAN"], 2))
        st.write("Highest rank in sector: ", stockbasis_df.loc[ticker]["RSSCORE_SECTOR_BEST"])

        tmp_df1 = stockbasis_df.loc[ticker][
            ["RSSCORE_D1", "RSSCORE_D5", "RSSCORE_D10", "RSSCORE_D15", "RSSCORE_D20"]]

        st.table(tmp_df1)
        tmp_df1.index = [-1, -5, -10, -15, -20]
        col1.bar_chart(tmp_df1, height=500)

    with col2:
        st.write("### SCTR score sector")
        st.write("Rank within sector: ", round(stockbasis_df.loc[ticker]["SCTRSCORE_SECTOR_RANK"], 2))
        st.write("Sector median: ", round(stockbasis_df.loc[ticker]["SCTRSCORE_SECTOR_MEDIAN"], 2))
        st.write("Highest rank in sector: ", stockbasis_df.loc[ticker]["SCTRSCORE_SECTOR_BEST"])
        tmp_df2 = stockbasis_df.loc[ticker][["SCTRSCORE_D1", "SCTRSCORE_D5", "SCTRSCORE_D10", "SCTRSCORE_D15", "SCTRSCORE_D20"]]
        st.table(tmp_df2)
        tmp_df2.index=[-1,-5,-10,-15,-20]
        col2.bar_chart(tmp_df2,height=500)

    with col3:
        st.write("### MRSQUARE score sector")
        st.write("Rank within sector: ", round(stockbasis_df.loc[ticker]["MRSQUARE_SECTOR_RANK"], 2))
        st.write("Sector median: ", round(stockbasis_df.loc[ticker]["MRSQUARE_SECTOR_MEDIAN"], 2))
        st.write("Highest rank in sector: ", stockbasis_df.loc[ticker]["MRSQUARE_SECTOR_BTEST"])
        #tmp_df3 = stockbasis_df.loc[ticker][["MRSQUARE", "MRSQUARE_D1", "MRSQUARE_D5", "MRSQUARE_D10", "MRSQUARE_D15", "MRSQUARE_D20"]]
        tmp_df3 = stockbasis_df.loc[ticker][
            ["MRSQUARE_D1", "MRSQUARE_D5", "MRSQUARE_D10", "MRSQUARE_D15", "MRSQUARE_D20"]]
        st.table(tmp_df3)
        tmp_df3.index=[-1,-5,-10,-15,-20]
        col3.bar_chart(tmp_df3,height=500)

    st.write('-------')