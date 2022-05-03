import streamlit as st
import numpy as np
import pandas as pd


def strdate2date(str_date):
    import datetime
    return datetime.datetime.strptime(str_date,'%Y-%m-%d').date()


def get_signal_description(signal):

    return "THIS IS " + signal

def app():
    signal_list = ['Momentum', 'Value', 'Size']
    option = st.selectbox(
    'Select factor',(signal_list))
    st.write(option)

    # load signal description
    st.write("## Description")

    # backtest results

    # display split left right top, bottom 10




def app2():
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import pandas as pd
    import streamlit as st
    from st_aggrid import AgGrid
    from st_aggrid.shared import GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder

    #st.set_page_config(page_title="Netflix Shows", layout="wide")
    st.title("Netflix shows analysis")

    shows = pd.read_csv("netflix_titles.csv")
    gb = GridOptionsBuilder.from_dataframe(shows)

    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()

    #AgGrid(shows, gridOptions=gridOptions, enable_enterprise_modules=True)
    data = AgGrid(shows,
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED)

    st.write(data)
    st.write('=====================')
    #st.write(type(data['selected_rows']))
    #st.json(data['selected_rows'])

    df_to_export = pd.DataFrame.from_dict(data['selected_rows'], orient='columns')

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_to_export)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='df_to_export.csv',
        mime='text/csv',
    )

    st.dataframe(df_to_export)

if __name__ == '__main__':
    app()