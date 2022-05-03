'''
1. run the VCP stream lit and see which ticker got VCP
2. note down those ticker name
3. run this code on the above ticker on the ./Downloaded_data folder then it will onyl retain data for those ticker
'''
import os
import pandas as pd
import pickle

'''
step 2: paste vcp ticker here from step 1
'''
#vcp_ticker_list = ['ESTE', 'EXLS','FPI','FRO','HLT','HST','LRN','MAR','MGPI','MIME','MUSA','PLD','QLYS','REXR','RHP','TWI','XOM']
vcp_ticker_list = ['ABM', 'ACHC', 'ACRE', 'AKAM', 'ALKS', 'AMGN', 'AMH', 'ARMK', 'ASH', 'ATEN', 'AVGO', 'AVNW', 'AZO', 'AZPN', 'BAH', 'BBSI', 'BFS', 'CASY', 'CC', 'CDK', 'CHE', 'CHEF', 'CHRW', 'CI', 'CPB', 'CXW', 'DAR', 'DCO', 'DG', 'DNOW', 'DRH', 'DRQ', 'EHC', 'ENSG', 'ENV', 'ESTE', 'EXEL', 'EXLS', 'FCFS', 'FCN', 'FLT', 'FPI', 'FRO', 'GCO', 'GDDY', 'GES', 'GPC', 'HAYN', 'HCC', 'HE', 'HHC', 'HII', 'HLT', 'HST', 'HUM', 'HURN', 'INCY', 'IONS', 'IRWD', 'J', 'JAZZ', 'KELYA', 'KEX', 'KHC', 'KNSL', 'KSS', 'LOPE', 'LRN', 'LTC', 'LUV', 'LW', 'LYB', 'MANT', 'MAR', 'MET', 'MGEE', 'MGPI', 'MIME', 'MMC', 'MMI', 'MRK', 'MUSA', 'MYE', 'NBIX', 'NEU', 'NHC', 'NLSN', 'NOC', 'NOV', 'NTCT', 'OAS', 'ODP', 'ORA', 'PAYX', 'PCG', 'PEB', 'PFGC', 'PFIS', 'PK', 'PLD', 'PNW', 'POST', 'PPL', 'PRA', 'PRDO', 'PRGS', 'PSB', 'PSMT', 'QLYS', 'REXR', 'RHP', 'RLI', 'ROCC', 'RSG', 'SANM', 'SCI', 'SEB', 'SENEA', 'SHO', 'SIGI', 'SM', 'SON', 'STRA', 'STZ', 'SYY', 'TAP', 'TGT', 'TMUS', 'TMX', 'TTMI', 'TWI', 'UE', 'UFCS', 'ULTA', 'USFD', 'USPH', 'UTL', 'UVV', 'VMI', 'WABC', 'WEX', 'WM', 'WRK', 'WWE', 'XHR', 'XOM', 'ZEN']

original_data_folder = r"C:\Users\david506hk\Documents\gitKaren_home\streamlit_deploy_example-main\Downloaded_data"
output_data_folder = r"C:\Users\david506hk\Documents\gitKaren_home\streamlit_deploy_example-main\demo_Downloaded_data"

livevcp_df_path = os.path.join(original_data_folder, 'LIVEVCP.csv')
ohlcvdict_df_path = os.path.join(original_data_folder, 'OHLCVDICT.pickle')
stockbasis_df_path = os.path.join(original_data_folder, 'STOCKBASIS.csv')

filtered_livevcp_df_path = os.path.join(output_data_folder, 'LIVEVCP.csv')
filtered_ohlcvdict_df_path = os.path.join(output_data_folder, 'OHLCVDICT.pickle')
filtered_stockbasis_df_path = os.path.join(output_data_folder, 'STOCKBASIS.csv')

livevcp_df = pd.read_csv(livevcp_df_path,index_col=0)
ohlcvdict_df = pd.read_pickle(ohlcvdict_df_path)
stockbasis_df = pd.read_csv(stockbasis_df_path,index_col=0)

#filter out the liveVCP
print("livevcp_df = ",livevcp_df)
filtered_livevcp_df = livevcp_df[livevcp_df['ticker'].isin(vcp_ticker_list)]

#filter out the ohlcvdict
from dotted_dict import DottedDict
filtered_ohlcvdict_df = DottedDict()
for cur_key in ohlcvdict_df.keys():
    cur_df = ohlcvdict_df[cur_key]
    print("cur_df.columns = ",cur_df.columns)
    cur_filtered_df = cur_df[vcp_ticker_list]
    filtered_ohlcvdict_df[cur_key] = cur_filtered_df
    pass
print("filtered_ohlcvdict_df = ",filtered_ohlcvdict_df)

#filter out the stockbasis
filtered_stockbasis_df = stockbasis_df[stockbasis_df.index.isin(vcp_ticker_list)]


#output_filtered dataframe
filtered_livevcp_df.to_csv(filtered_livevcp_df_path)
with open(filtered_ohlcvdict_df_path, 'wb') as handle:
    pickle.dump(filtered_ohlcvdict_df, handle)
filtered_stockbasis_df.to_csv(filtered_stockbasis_df_path)


print("filtered_livevcp_df.shape = ",filtered_livevcp_df.shape)
print("filtered_ohlcvdict_df.open.shape = ",filtered_ohlcvdict_df.open.shape)
print("filtered_stockbasis_df.shape = ",filtered_stockbasis_df.shape)