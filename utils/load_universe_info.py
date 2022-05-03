import streamlit as st
import datetime

# returns all tickers for time series universe
@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def get_time_series_data_refintiv_universe():
    print('load_time_series_data_refintiv_universe:: running ')
    import pandas as pd
    from streamlit_project_settings import OHLCV_PICKLE
    ts_df = pd.read_pickle(OHLCV_PICKLE)
    return ts_df.close.columns.to_list()

# returns all tickers for time series universe
@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def get_vcp_data_universe():
    print('get_vcp_data_universe:: running ')
    import pandas as pd
    from streamlit_project_settings import VCP_DF_PATH
    vcp_tickers_universe = pd.read_csv(VCP_DF_PATH,usecols=['ticker'])['ticker'].to_list()
    return vcp_tickers_universe


def get_vcpable_universe():
    print('get_vcpable_universe:: running ')
    # finds the interaction between VCP and ticker universe
    time_series_universe = get_time_series_data_refintiv_universe()
    vcp_tickers_universe = get_vcp_data_universe()
    vcpable_universe = sorted(list(set(time_series_universe).intersection(set(vcp_tickers_universe))))
    return vcpable_universe