import pandas as pd
import datetime as dt
import sqlite3
import numpy as np
import math
import traceback

class FundsData:
    def __init__(self,dt_start,dt_end):
        conn = sqlite3.connect('./data/fund-data.db')
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.dates = conn.execute("select distinct trade_date from fundValue where trade_date > '%s' and trade_date < '%s' order by trade_date asc" % (dt_start.strftime('%Y-%m-%d'), dt_end.strftime('%Y-%m-%d')))\
                .fetchall()
            
    def get_df(self,codes:list):
        conn = sqlite3.connect('./data/fund-data.db')
        dt_start = self.dt_start
        dt_end = self.dt_end
        dates = self.dates
        
        dfs = []
        for code in codes:
            sql = "select trade_date, net_val from fundValue where code ='%d' and trade_date > '%s' and trade_date < '%s' order by trade_date asc" % \
                (code, dt_start.strftime('%Y-%m-%d'), dt_end.strftime('%Y-%m-%d'))
            rst = conn.execute(sql).fetchall()
            df = pd.DataFrame(rst,columns=['date','net_val'])
            if len(df) == 0:
                df = df.append({'date':dates[0][0],'net_val':1.0},ignore_index=True)
            df = df.set_index('date')
            df.index = df.index.astype('datetime64')
            dfs.append(df)

        

        df = dfs[0]
        idx = 1
        while idx < len(dfs):
            df = pd.merge(df,dfs[idx],how='outer',left_index=True,right_index=True,suffixes=('','_%d' % idx))
            idx += 1

        df_dates = pd.DataFrame(dates,columns=['dates']).set_index('dates')
        df = pd.merge(df_dates,df,how='left',left_index=True,right_index=True,suffixes=('',''))
        df.fillna(method='ffill',inplace=True)
        df.fillna(method='bfill',inplace=True)
        return df