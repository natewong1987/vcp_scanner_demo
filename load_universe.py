if __name__ == "__main__":
    import pandas as pd
    path = r"C:\Users\tclyu\Dropbox\thomas_home\active_portfolio_management\data\universe\refinitiv_Russell3000_20220402.csv"


    signal_path = r"C:\Users\tclyu\PycharmProjects\streamlit_deploy_example\Downloaded_data\RSSCORE.csv"
    universe_df = pd.read_csv(path,usecols=["TR.TICKERSYMBOL","TR.GICSINDUSTRY","TR.GICSINDUSTRYGROUP","TR.GICSSECTOR"])
    #universe_df.columns = universe_df.columns.str.replace('TR.', '')
    universe_df.set_index(['TR.TICKERSYMBOL'],inplace=True)


    import time
    to=time.time()
    signal_df = pd.read_csv(signal_path,parse_dates=True,index_col=['date'])
    rank_within_sector_df = pd.DataFrame().reindex(index=signal_df.index, columns=signal_df.columns)
    rank_within_industry_df = pd.DataFrame().reindex(index=signal_df.index, columns=signal_df.columns)

    for idx, row in signal_df.iterrows():
        q = pd.concat([row.to_frame(), universe_df], axis=1)
        q['rank_within_sector'] = q.groupby("TR.GICSSECTOR").rank(ascending=False)[idx] # the higher the better
        q['rank_within_industry'] = q.groupby("TR.GICSINDUSTRY").rank(ascending=False)[idx]
        rank_within_sector_df.loc[idx] = q['rank_within_sector']
        rank_within_industry_df.loc[idx] = q['rank_within_industry']

        #index_ = signal_df.iloc[0].name

        #q = pd.concat([row.to_frame(), universe_df], axis=1)
        # q = pd.concat([signal_df.iloc[0].to_frame(),universe_df],axis=1)
        #q['rank_within_sector'] = q.groupby("TR.GICSSECTOR").rank(ascending=False)[index_] # the higher the better
        #q['rank_within_industry'] = q.groupby("TR.GICSINDUSTRY").rank(ascending=False)[index_]

    print(time.time()-to)
    #q.groupby("TR.GICSSECTOR")[index_].mean()
    print('here')
    #signal_df.T
    #universe_df["rank"] = universe_df.groupby("group_ID")["value"].rank("dense", ascending=False)
    #print(universe_df)TR.GICSINDUSTRY
if __name__ == "____":
    import pandas as pd
    from utils.load_data import load_time_series_data_refintiv
    #load_time_series_data_refintiv
    from streamlit_project_settings import OHLCV_PICKLE
    ts_df = pd.read_pickle(OHLCV_PICKLE)

    print('here')