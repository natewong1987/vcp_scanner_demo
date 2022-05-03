import streamlit as st
import os
PROJECT_PATH = os.path.realpath(".")
DOWNLOADED_DATA_DIR = "./demo_Downloaded_data" #"./demo_Downloaded_data" #"./Sample_Downloaded_data" #"./Downloaded_data"

OVERRIDE_SECRET = False
if not OVERRIDE_SECRET:
    SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']
# below are files that are downloaded to local (locally @ streamlit instance)
SIGNAL_POINTER_FILE = "SIGNAL_POINTER_LIVE.csv"
OHLCV_PICKLE = os.path.join(DOWNLOADED_DATA_DIR,'OHLCVDICT.pickle')
VCP_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'LIVEVCP.csv')
RSSCORE_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'RSSCORE.csv')
SCTRSCORE_DF_PATH = os.path.abspath(os.path.join(DOWNLOADED_DATA_DIR,'SCTRSCORE.csv'))
MRSQUARE_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'MRSQUARE.csv')
STOCKBASIS_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,"STOCKBASIS.csv")

#streamlit run C:/Users/tclyu/PycharmProjects/streamlit_deploy_example/dashboard_app.py
REPORT_TEMPLATE_DIR = "./pdf_report_generator/report_templates"
VCP_REPORT_COVERPAGE_PATH = os.path.join(REPORT_TEMPLATE_DIR,"vcp_report_template.pptx")
SINGLE_POWERPOINT_PAGE_PATH = os.path.join(REPORT_TEMPLATE_DIR,"page_template.pptx")


import os
import personal_settings
PROJECT_PATH = os.path.realpath(".") #this is equal to python path in pythonpath.bat
# this is user specific
DROPBOX_USER_PATH = personal_settings.DROPBOX_USER_PATH #r"C:\Users\tclyu\Dropbox"

DROPBOX_PATH = os.path.join(DROPBOX_USER_PATH, r"thomas_home\active_portfolio_management")
HARDCOREVCP_HOME = os.path.join(DROPBOX_PATH,"HARDCOREVCP")
REPORT_OUTPUT_DIR = os.path.join(HARDCOREVCP_HOME,r"digital_products\reports")

#streamlit run C:/Users/tclyu/PycharmProjects/streamlit_deploy_example/dashboard_app.py
