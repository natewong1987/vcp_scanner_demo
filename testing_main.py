import streamlit as st
import pandas as pd

from streamlit_project_settings import VCP_DF_PATH
print("VCP path = ",VCP_DF_PATH)

livevcp_df = pd.read_csv(VCP_DF_PATH)

print("VCP path = ",VCP_DF_PATH)
print("livevcp_df = ",livevcp_df)
st.write(livevcp_df)