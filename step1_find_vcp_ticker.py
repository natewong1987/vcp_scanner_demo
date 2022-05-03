from utils.load_data import load_vcp_df
from utils.load_data import prepare_fullframe_vcp_data


def in_house_filter_vcp_df(vcp_df):
    inhouse_filtered_vcp_df = vcp_df.copy(deep=True)
    inhouse_filtered_vcp_df = inhouse_filtered_vcp_df[(inhouse_filtered_vcp_df['total_duration']>30) &\
        (inhouse_filtered_vcp_df['first_contraction_pct'] >= 0.15) & (inhouse_filtered_vcp_df['first_contraction_pct'] <= 0.45)  &\
    (inhouse_filtered_vcp_df['latest_contraction_pct'] <= 0.15) &\
    (inhouse_filtered_vcp_df['RSSCORE'] >= 60) &\
    (inhouse_filtered_vcp_df['SCTRSCORE'] >= 60) &\
    (inhouse_filtered_vcp_df['MRSQUARE'] >= 60) &\
    (inhouse_filtered_vcp_df['SW_stage2']==True) & \
    (inhouse_filtered_vcp_df['volume_contraction_condition']) & (inhouse_filtered_vcp_df['latest_contraction_price'] >= 10)]

    inhouse_filtered_vcp_df.reset_index(inplace=True)
    return inhouse_filtered_vcp_df

# this determines what colums are shown in the VCP summary table
def make_pertty_vcp_summary(vcp_df):
    import pandas as pd
    vcp_df_pretty = pd.DataFrame()
    vcp_df_pretty['ticker'] = vcp_df['ticker']
    vcp_df_pretty['scanned date'] = vcp_df['datetime']
    vcp_df_pretty['first detected date'] = vcp_df['earliest_vcp_scanned_date']
    # this is the VCP footprint that MM uses
    vcp_df_pretty['footprint'] = (vcp_df['total_duration'].fillna(0)/ 5).round().astype(str) + "W-" +\
                                 vcp_df['contraction_ratio'].round(2).astype(str)+ '-'+vcp_df['number_of_consolidations'].astype(str) + 'T'

    vcp_df_pretty['total duration (days)'] = vcp_df['total_duration'].astype('int32')
    vcp_df_pretty['1st contraction (%)'] = round(vcp_df['first_contraction_pct'].astype('float')*100,1)
    vcp_df_pretty['1st contraction (days)'] = vcp_df['first_contraction_duration'].astype('int32')
    vcp_df_pretty['Latest contraction (%)'] = round(vcp_df['latest_contraction_pct'].astype('float')*100,1)
    vcp_df_pretty['latest contraction (days)'] = vcp_df['latest_contraction_duration'].astype('int32')
    vcp_df_pretty['SW stage2'] = vcp_df['SW_stage2'].astype('str')
    vcp_df_pretty['MM Trend filtered'] = vcp_df['MM_Stage2Filtered'].astype('str')
    vcp_df_pretty['Volume contraction'] = vcp_df['volume_contraction_condition'].astype('str')
    vcp_df_pretty['RSSCORE'] = round(vcp_df['RSSCORE'],0)
    vcp_df_pretty['SCTR'] = round(vcp_df['SCTRSCORE'],0)
    vcp_df_pretty['MSQUARE'] = round(vcp_df['MRSQUARE'],0)
    vcp_df_pretty['is_break_out_latest_contraction'] = vcp_df['is_break_out_latest_contraction'].astype('str')
    vcp_df_pretty['is_break_out_first_contraction'] = vcp_df['is_break_out_first_contraction'].astype('str')
    vcp_df_pretty['support_mrsquare'] = vcp_df['support_mrsquare']
    vcp_df_pretty['support_slope'] = vcp_df['support_slope']
    vcp_df_pretty['resis_mrsquare'] =vcp_df['resis_mrsquare']
    vcp_df_pretty['resis_slope'] = vcp_df['resis_slope']

    return vcp_df_pretty

def prepare_vcp_df(vcp_df):
    print("********************  RUNNING PREPARE VCP")
    inhouse_filtered_vcp_df = in_house_filter_vcp_df(vcp_df)
    vcp_df_pretty = make_pertty_vcp_summary(inhouse_filtered_vcp_df)
    return vcp_df_pretty


vcp_df = load_vcp_df()
print("vcp_df.head() = ",vcp_df.head())
print("vcp_df.columns = ",vcp_df.columns)
print("vcp_df.shape = ",vcp_df.shape)
vcp_full_frame = prepare_fullframe_vcp_data()
vcp_df_pretty = prepare_vcp_df(vcp_full_frame)


print("vcp_df_pretty = ",vcp_df_pretty)
print("vcp_full_frame.shape = ",vcp_full_frame.shape)
print("vcp_df_pretty.shape = ",vcp_df_pretty.shape)

# filtered_vcp_raw_df = vcp_full_frame[vcp_full_frame['ticker'].isin(list(vcp_df_pretty['ticker'].values))]
# second_vcp_df_pretty = prepare_vcp_df(filtered_vcp_raw_df)
'''
step 1: find all ticker which have prettry VCP
        then paste it to step 2
'''
#find all ticker which have prettry VCP
print(list(vcp_df_pretty['ticker'].values))

# from utils.load_universe_info import get_vcpable_universe
# vcp_universe_df = get_vcpable_universe()
# print("vcp_universe_df = ",vcp_universe_df)