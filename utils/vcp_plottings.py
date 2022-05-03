import datetime
import streamlit as st
def set_up_time_series_plot(ticker, ohlcv_df):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import plotly.io as pio

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


def add_contraction_lines(fig, merged_contractions):
    # plot horizontal lines for contraction
    import datetime

    horizontal_line_length = 10
    line_width = 2
    line_colour = "white"
    text_colour = line_colour
    for idx, con_ in merged_contractions.iterrows():
        constraction_start_dt = datetime.datetime.strptime(con_.start_dt_index, '%Y-%m-%d')
        constraction_end_dt = datetime.datetime.strptime(con_.end_dt_index, '%Y-%m-%d')


        resis_date_on_plot_line_start_index = constraction_start_dt - datetime.timedelta(days=horizontal_line_length)
        resis_date_on_plot_line_end_index = constraction_start_dt + datetime.timedelta(days=horizontal_line_length)

        fig.add_shape(type='line', x0=resis_date_on_plot_line_start_index,
                      x1=resis_date_on_plot_line_end_index, y0=con_.resis_price, y1=con_.resis_price,
                      line_width=line_width, line_color=line_colour)

        delta_t_days = (constraction_end_dt - constraction_start_dt).days
        fig.add_annotation(x=resis_date_on_plot_line_start_index, y=con_.resis_price,
                           text=str(round(con_.contraction_pct * 100, 2)) + '%,' + str(delta_t_days), showarrow=True,
                           arrowhead=1,font=dict(
        #family="sans serif",
        size=13,
        color=text_colour,
        ))

        support_date_on_plot_line_start_index = constraction_end_dt - datetime.timedelta(days=horizontal_line_length)
        support_date_on_plot_line_end_index = constraction_end_dt + datetime.timedelta(days=horizontal_line_length)

        fig.add_shape(type='line', x0=support_date_on_plot_line_start_index,
                      x1=support_date_on_plot_line_end_index, y0=con_.support_price,
                      y1=con_.support_price, line_width=line_width, line_color=line_colour)
    return fig

def clean_up_axis(fig, ticker, date_str,use_title=True,range_slide_on=True):
    if use_title:
        generate_title = "TICKER=" + ticker + ",DATE=" + date_str  # + ",volume_slope=" + str(
    else:
        generate_title=""
    # https://plotly.com/python/time-series/#hiding-weekends-and-holidays
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), ])  # hide weekends
    fig.update_layout(title_text=generate_title)
    fig.update_layout(
        autosize=True,
        width=1000,
        height=600,
        margin=dict(l=20, r=50, t=30, b=20),
        title_text=generate_title,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.01, gridcolor='Black', automargin=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='Black', automargin=False)
    fig.update(layout_xaxis_rangeslider_visible=range_slide_on)
    return fig

def get_contractions_from_vcp_df(vcp_slice):
    import pandas as pd
    # given a vcp slice this function generates the contraction df
    try:
        merged_df = []
        vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]

        num_contractions = vcp_slice_dict['number_of_consolidations']

        for x in range(num_contractions):
            tmp_dict = {"end_dt_index": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_end_dt"],
                        "support_price": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_support_price"],
                        "start_dt_index": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_start_dt"],
                        "resis_price": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_resis_price"],
                        "contraction_pct": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_contraction_pct"]}
            merged_df.append(tmp_dict)
        contractions_df = pd.DataFrame(merged_df)
        return contractions_df

    except Exception as e:
        print(e)
        return pd.DataFrame()


def NEW_generate_VCP_plot_for_timeslice(ticker, ohlcv_df, vcp_slice):
    import datetime
    near_field_range = -1

    current_scan_date = vcp_slice.iloc[0]['datetime']

    # subset data
    ohlcv_df_tmp = ohlcv_df.reset_index().copy()
    #data_end_date = datetime.datetime.strptime(current_scan_date, '%Y-%m-%d')
    #subset_ohlcv_df = ohlcv_df_tmp[ohlcv_df_tmp['date'] <= data_end_date]

    #fig = set_up_time_series_plot(ticker, subset_ohlcv_df)
    fig = set_up_time_series_plot(ticker, ohlcv_df_tmp)

    merged_contractions = get_contractions_from_vcp_df(vcp_slice)
    if not merged_contractions.empty:
        fig = add_contraction_lines(fig, merged_contractions)

    fig, clean_up_axis(fig, ticker, current_scan_date)
    # return volume_slope, contraction_slope, merged_contractions, near_field_range
    return fig, near_field_range

