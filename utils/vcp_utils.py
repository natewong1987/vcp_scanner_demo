def make_multiselect_summary_table(vcp_df_pretty, default_selections_rows):
    from st_aggrid import AgGrid
    from st_aggrid.shared import GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(vcp_df_pretty)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True,
                                min_column_width=100)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True, pre_selected_rows=default_selections_rows)
    gridOptions = gb.build()

    selected_data = AgGrid(vcp_df_pretty,
                           width='1000',
                           height=1000,
                           # theme='dark',
                           fit_columns_on_grid_load=True,
                           gridOptions=gridOptions,
                           enable_enterprise_modules=True,
                           allow_unsafe_jscode=True,
                           update_mode=GridUpdateMode.SELECTION_CHANGED)
    default_ticker = vcp_df_pretty['ticker'][0]
    return selected_data, default_ticker

def make_summary_table(vcp_df_pretty):
    from st_aggrid import AgGrid
    from st_aggrid.shared import GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(vcp_df_pretty)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True,
                                min_column_width=100)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gridOptions = gb.build()

    selected_data = AgGrid(vcp_df_pretty,
                           width='1000',
                           #height=1000,
                           # theme='dark',
                           fit_columns_on_grid_load=True,
                           gridOptions=gridOptions,
                           enable_enterprise_modules=True,
                           allow_unsafe_jscode=True,
                           update_mode=GridUpdateMode.SELECTION_CHANGED)
    default_ticker = vcp_df_pretty['ticker'][0]
    return selected_data, default_ticker

def build_vcp_summary_table(vcp_df_pretty):
    selected_data, default_ticker = make_summary_table(vcp_df_pretty)
    return selected_data, default_ticker

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

def display_contractions_df_grid(contractions_df):
    # show contractions
    import streamlit as st
    import pandas as pd
    con_df = contractions_df.copy()

    con_df['duration (days)'] = (pd.to_datetime(contractions_df['end_dt_index']) - pd.to_datetime(contractions_df['start_dt_index']))
    con_df['duration (days)'] = con_df['duration (days)'].apply(lambda x: x.days)
    column_names=['start_dt_index','end_dt_index','duration (days)','contraction_pct','resis_price','support_price']

    con_df = con_df.reindex(columns=column_names)
    con_df['contraction_pct'] = con_df['contraction_pct'].apply(lambda x:str(round(float(x)*100, 2)))
    con_df['resis_price'] = con_df['resis_price'].apply(lambda x: str(round(x, 2)))
    con_df['support_price'] = con_df['support_price'].apply(lambda x: str(round(x, 2)))
    con_df.rename({'start_dt_index':'start_dt','end_dt_index':'end_dt','support_price':"Support",'resis_price':"Resistance", 'contraction_pct':"Contraction %"},inplace=True)

    st.table(con_df)
    pass