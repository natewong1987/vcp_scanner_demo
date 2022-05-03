import datetime
import streamlit as st
# we want filter vcp to make sense before VCPs before displaying
def in_house_filter_vcp_df(vcp_df):
    inhouse_filtered_vcp_df = vcp_df.copy(deep=True)
    inhouse_filtered_vcp_df = inhouse_filtered_vcp_df[(inhouse_filtered_vcp_df['total_duration']>30) &\
        (inhouse_filtered_vcp_df['first_contraction_pct'] >= 0.15) & (inhouse_filtered_vcp_df['first_contraction_pct'] <= 0.45)  &\
    (inhouse_filtered_vcp_df['latest_contraction_pct'] <= 0.15) &\
    (inhouse_filtered_vcp_df['RSSCORE'] >= 60) &\
    (inhouse_filtered_vcp_df['SCTRSCORE'] >= 60) &\
    (inhouse_filtered_vcp_df['MRSQUARE'] >= 60) &\
    (inhouse_filtered_vcp_df['SW_stage2']==True) & \
    (inhouse_filtered_vcp_df['volume_contraction_condition']) & (inhouse_filtered_vcp_df['latest_contraction_price'] >= 10) & \
    (inhouse_filtered_vcp_df['is_break_out_latest_contraction'] >= True)  & \
        (inhouse_filtered_vcp_df['is_break_out_first_contraction'] >= True)]

    inhouse_filtered_vcp_df.reset_index(inplace=True)
    return inhouse_filtered_vcp_df

@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def prepare_vcp_df(vcp_df):
    print("********************  RUNNING PREPARE VCP")
    inhouse_filtered_vcp_df = in_house_filter_vcp_df(vcp_df)
    from deploy_pages.new_vcp_page import make_pertty_vcp_summary
    vcp_df_pretty = make_pertty_vcp_summary(inhouse_filtered_vcp_df)
    return vcp_df_pretty


def app():
    import pandas as pd
    import os
    import datetime
    import streamlit as st
    from utils.load_data import load_time_series_data_refintiv, load_vcp_df, load_STOCKBASIS
    from utils.load_data import prepare_fullframe_vcp_data

    from utils.vcp_utils import build_vcp_summary_table, get_contractions_from_vcp_df, display_contractions_df_grid
    from utils.vcp_plottings import NEW_generate_VCP_plot_for_timeslice, clean_up_axis

    vcp_full_frame = prepare_fullframe_vcp_data()
    stockbasis_df = load_STOCKBASIS()

    vcp_df_pretty = prepare_vcp_df(vcp_full_frame)
    data, default_ticker = build_vcp_summary_table(vcp_df_pretty)

    if not data['selected_rows']:
        ticker = default_ticker
    else:
        ticker = data['selected_rows'][0]['ticker']

    ohlcv_df = load_time_series_data_refintiv(ticker)

    #st.dataframe(vcp_df)

    vcp_slice = vcp_full_frame[vcp_full_frame["ticker"] == ticker]
    contractions_df = get_contractions_from_vcp_df(vcp_slice)

    col1, col2= st.columns([2.5,1])
    vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]

    with col1:
        fig, near_field = NEW_generate_VCP_plot_for_timeslice(ticker, ohlcv_df, vcp_slice)
        fig, clean_up_axis(fig, ticker,str(vcp_slice_dict['datetime']))
        st.plotly_chart(fig, width=1200, height=900)

    with col2:
        st.write("# "+ticker)
        st.write("Industry:\t" + vcp_slice_dict["TR.GICSINDUSTRY"])
        st.write("Industry Group:\t" +vcp_slice_dict["TR.GICSINDUSTRYGROUP"])
        st.write("Sector:\t" + vcp_slice_dict["TR.GICSSECTOR"])
        st.write('-------')
        st.write("# VCP info")
        st.write("Footprint:\t" +vcp_df_pretty[vcp_df_pretty["ticker"] == ticker].iloc[0]["footprint"])
        st.write("Total duration:\t",vcp_slice_dict["total_duration"])
        st.write("N contractions:\t", vcp_slice_dict["number_of_consolidations"])
        st.write("Max contraction (%):\t",round(vcp_slice_dict["max_consolidations_pct"]*100,2))

        st.write("### VCP status")
        st.write("Earliest scanned on :\t",vcp_slice_dict["earliest_vcp_scanned_date"])
        st.write("is breakout latest contraction :\t",vcp_slice_dict["is_break_out_latest_contraction"])
        st.write("is breakout latest contraction :\t",vcp_slice_dict["is_break_out_first_contraction"])
        st.write("SL :\t",contractions_df.iloc[-1]['support_price'])
        entry_price = vcp_slice_dict['latest_contraction_price']
        st.write("2R :\t", round(entry_price*(1+2*vcp_slice_dict['latest_contraction_pct']),2))

    # step 2 plot factors
    col1, col2, col3 = st.columns(3)
    col1.metric("Relative Strength", round(stockbasis_df.loc[ticker]['RSSCORE'],2), delta=round(stockbasis_df.loc[ticker]['RSSCORE_D1'],2))
    col2.metric("SCTR", round(stockbasis_df.loc[ticker]['SCTRSCORE'],2), delta=round(stockbasis_df.loc[ticker]['SCTRSCORE_D1'],2))
    col3.metric("MRSQUARE", round(stockbasis_df.loc[ticker]['MRSQUARE'],2), delta=round(stockbasis_df.loc[ticker]['SCTRSCORE_D1'],2))


    st.write("## Contractions info")
    display_contractions_df_grid(contractions_df)
