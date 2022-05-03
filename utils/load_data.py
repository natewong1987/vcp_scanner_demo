import streamlit as st
import datetime

@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_time_series_data(ticker):
    import pandas as pd
    from streamlit_project_settings import DOWNLOADED_DATA_DIR
    ts_df = pd.read_csv(DOWNLOADED_DATA_DIR +'/'+ ticker.upper() +'.csv')
    return ts_df

@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_time_series_data_refintiv(ticker):
    print('load_time_series_data_refintiv:: runnnig '+ ticker)
    import pandas as pd
    from streamlit_project_settings import OHLCV_PICKLE
    ts_df = pd.read_pickle(OHLCV_PICKLE)
    ticker_specific_df = convert_single_equity_2_df(ts_df, ticker)
    ticker_specific_df.reset_index(inplace=True)
    return ticker_specific_df


def convert_single_equity_2_df(ohlcv_btg_format, symbol):
    import logging
    try:
        import pandas as pd
        '''
        # this functioon converts a single symbol from ohlc_btg_format (dotted dict) to ohlcv for backtrader

                                  open        high         low       close        volume
        date                                                                    
        2007-01-03    3.081786    3.092143    2.925000    2.992857  1.238320e+09
        2007-01-04    3.001786    3.069643    2.993572    3.059286  8.472604e+08
        2007-01-05    3.063214    3.078571    3.014286    3.037500  8.347416e+08
        2007-01-08    3.070000    3.090357    3.045714    3.052500  7.971068e+08
        '''

        single_equity_df = pd.DataFrame(
            [ohlcv_btg_format.open[symbol], ohlcv_btg_format.high[symbol], ohlcv_btg_format.low[symbol],
             ohlcv_btg_format.close[symbol], ohlcv_btg_format.volume[symbol]]).T

        single_equity_df.columns = ['open', 'high', 'low', 'close', 'volume']
        return single_equity_df

    except Exception as e:

        logging.error('convert_single_equity:: error in converting ohlcv_btg_format to dataframe')
        logging.error('convert_single_equity')
        logging.error(str(e))

        return pd.DataFrame()


@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_vcp_df(snapshot_date = datetime.datetime.now().date()):
    print('load_vcp_df:: running ')
    import pandas as pd
    from streamlit_project_settings import VCP_DF_PATH
    vcp_df = pd.read_csv(VCP_DF_PATH)
    vcp_df = vcp_df.drop(['MM_Stage2Filtered','RSSCORE', 'SCTRSCORE', 'MRSQUARE'], axis=1, errors='ignore')

    return vcp_df

"""
@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_RSSCORE_df(snapshot_date = datetime.datetime.now().date()):
    print('load_RSSCORE_df:: running ')
    import pandas as pd
    from streamlit_project_settings import RSSCORE_DF_PATH
    rs_score_df = pd.read_csv(RSSCORE_DF_PATH,parse_dates=True,index_col='date')
    rs_score_df_df5 = rs_score_df.diff(periods=5)
    return rs_score_df, rs_score_df_df5, rs_score_df.diff(periods=10)

@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_MRSQUARE_df(snapshot_date = datetime.datetime.now().date()):
    print('load_MRSQUARE_df:: running ')
    import pandas as pd
    from streamlit_project_settings import MRSQUARE_DF_PATH
    mrsquare_score_df = pd.read_csv(MRSQUARE_DF_PATH, parse_dates=True,index_col='date')
    return mrsquare_score_df,  mrsquare_score_df.diff(periods=5), mrsquare_score_df.diff(periods=10)

@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_SCTRSCORE_df(snapshot_date = datetime.datetime.now().date()):
    print('load_SCTRSCORE_df:: running ')
    import pandas as pd
    from streamlit_project_settings import SCTRSCORE_DF_PATH
    sctr_score_df = pd.read_csv(SCTRSCORE_DF_PATH,parse_dates=True,index_col='date')
    return sctr_score_df, sctr_score_df.diff(periods=5), sctr_score_df.diff(periods=10)
"""


@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_STOCKBASIS(snapshot_date = datetime.datetime.now().date()):
    print('load_SCTRSCORE_df:: running ')
    import pandas as pd
    from streamlit_project_settings import STOCKBASIS_DF_PATH
    stockbasis_df = pd.read_csv(STOCKBASIS_DF_PATH,index_col=[0])
    return stockbasis_df

import datetime
@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def prepare_fullframe_vcp_data():
    print('prepare_fullframe_vcp_data:: running ')
    from utils.load_data import load_vcp_df, load_STOCKBASIS
    vcp_df = load_vcp_df()
    stockbasis_df = load_STOCKBASIS()
    vcp_df_full = vcp_df.join(stockbasis_df,on=['ticker'],how='inner')
    vcp_df_full = vcp_df_full.drop('Unnamed: 0',axis=1,errors ='ignore')
    return vcp_df_full
