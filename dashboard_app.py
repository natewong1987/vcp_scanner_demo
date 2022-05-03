import streamlit as st

# Custom imports
from multipage import MultiPage

st.set_page_config(layout="wide")
#import login_with_secret
# Create an instance of the app
app = MultiPage()

# Title of the main page
#display = Image.open('Logo.png')
#display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
#col1, col2 = st.columns(2)
#col1.image(display, width = 400)
#col2.title("Brite advisors board")

#########################################
#########################################

import datetime
@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def download_all_data_new(snapshot_date = datetime.datetime.now().date()):
    try:

        from streamlit_project_settings import DOWNLOADED_DATA_DIR, SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE
        from gdrive_download_utils import download_all_signals, download_file_from_google_drive_sharables
        print('running download all data')
        st.info('running download all data')
        st.info('download signal pointer file')
        st.info(SIGNAL_POINTER_FILE_ID)
        st.info(SIGNAL_POINTER_FILE)
        download_file_from_google_drive_sharables(SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE)
        download_all_signals(SIGNAL_POINTER_FILE, DOWNLOADED_DATA_DIR)

        return True

    except Exception as e:

        st.exception(e)
        return False

# download all data here
from utils.load_data import prepare_fullframe_vcp_data
# download_all_data_new()
prepare_fullframe_vcp_data()

if "vcpable_universe" not in st.session_state:
    from utils.load_universe_info import get_vcpable_universe
    st.session_state.vcpable_universe = get_vcpable_universe()
    #st.info(st.session_state)
    #print(st.session_state.vcpable_universe)

if "ticker_universe" not in st.session_state:
    from utils.load_universe_info import get_time_series_data_refintiv_universe
    st.session_state.ticker_universe = get_time_series_data_refintiv_universe()

# this variable stores where the data is as of
if "data_as_of_date" not in st.session_state:
    import pandas as pd
    from streamlit_project_settings import OHLCV_PICKLE
    ts_df = pd.read_pickle(OHLCV_PICKLE)
    st.session_state.data_as_of_date = ts_df.adjclose.index[-1]
    #st.info(st.session_state)


##########################################
##########################################

def strink_sidebar():
    #https://github.com/streamlit/streamlit/issues/2058

    st.markdown(
    f"""
    <style>
    .appview-container .main .block-container{{
            padding-top: {{padding_top}}rem;    }}
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
    width: 200px;
    }}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {{
    width: 200px;
    margin-left: -200px;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

#Add all your application here
# from dashboard_pages import test_multipage, test_multipage2, test_multipage3, factor_explorer, vcp_page, test_timeseries
#from deploy_pages import askgod, vcp_page, askgod_stockbasis
from deploy_pages import  askgod_stockbasis ,new_vcp_page, recent_breakout#, generate_report_gui
# app.add_page("Report GUI", generate_report_gui.app)
# app.add_page("Recent breakout", recent_breakout.app)
# app.add_page("Momentum lookup",askgod_stockbasis.app)
app.add_page("VCP setup", new_vcp_page.app)

# The main app
app.run()