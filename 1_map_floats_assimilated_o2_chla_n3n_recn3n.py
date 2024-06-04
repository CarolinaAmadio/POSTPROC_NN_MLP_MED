print('export ONLINE_REPO=/g100_work/OGS_devC/camadio/ONLINE_REPO/')
print('export ONLINE_REPO=/g100_work/OGS_devC/camadio/ONLINE_REPO/')
print('export ONLINE_REPO=/g100_work/OGS_devC/camadio/ONLINE_REPO/')

import numpy as np
import basins.OGS as OGS
from instruments import float_ppcon
from instruments.var_conversions import FLOATVARS
from commons.time_interval import TimeInterval
from commons import timerequestors
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import datetime as datetime
from basins.region import Region, Rectangle
import basins.V2 as basV2
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from basins_CA import cross_Med_basins

def col_to_dt(df,name_col):
    """ from object to datetime --> name_col
    """
    df['date'] = pd.to_datetime(df[name_col]).dt.date
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['date'] = pd.to_datetime(df['date'])
    return(df)

def col_to_basin(df,lon_col_name='lon', lat_col_name='lat'):
    df['Basin'] = np.nan
    for III in range(0,len(df)):
        tmp_lat = df.iloc[III,:][lat_col_name]
        tmp_lon = df.iloc[III,:][lon_col_name]
        ARGO       = Rectangle(np.float64(tmp_lon ) , np.float64( tmp_lon) , np.float64(tmp_lat) , np.float64(tmp_lat))
        NAME_BASIN , BORDER_BASIN = cross_Med_basins(ARGO)
        df['Basin'].iloc[III] = NAME_BASIN
    return (df)

# dynamic inputs
RUN, run   = 'MedBFM4.2_Q24_v3' , 'MedBFM4.2_Q24_v3'

#static inputs
VARLIST    = ['N3n','P_l','O2o']
df         = pd.read_csv('Float_assimilated_'+ RUN    +'.csv' , index_col=0)
df_CHLA    = df[['P_l_LON', 'P_l_LAT', 'P_l_DATE', 'P_l_NAME',]]
df_O2o     = df[['O2o_LON', 'O2o_LAT', 'O2o_DATE', 'O2o_NAME',]]

# la somma di len(N3n) + len(N3n_rec) = len(df)
NAMEVAR  = 'N3n'
strings=df.columns
LIST_sliced_df = [string for string in strings if NAMEVAR in string]
df_N3N=df[LIST_sliced_df]
df_N3N.dropna(how='all', inplace=True)
LIST_COL         =  ['lon','lat','DATE','NAME']
df_N3N.columns = LIST_COL

# insert qc list in n3n dataframe 
df_N3N.NAME     = df_N3N.NAME.astype(int) #
df_N3N  = col_to_dt(df_N3N,'DATE')
df_N3N['Qc']    = np.nan

TI_3  = timerequestors.TimeInterval(starttime='20190101', endtime='20200101', dateformat='%Y%m%d')
Profilelist=float_ppcon.FloatSelector(None  ,TI_3, OGS.med)

LIST_REJECTED=[]
from functools import reduce

for p in Profilelist:
    wmo=p._my_float.wmo
    tmp= df_N3N[df_N3N.NAME==int(wmo)]
    # if p is assimilated should be in df_N3N argmisdat dataframe 
    # check if the entire float is assimilated
    # check if profile is assimialted matching profilelist and armisdatfile 
    if int(wmo) in list(df_N3N.NAME):
       if np.around(np.float64(p.lat),3) in np.around((np.array(tmp.lat)),3): # same lar
            INDEX= np.where( np.around((np.array(df_N3N.lat)),3) == np.around(np.float64(p.lat),3))
            if np.around(np.float64(p.lon),3) in np.around((np.array(tmp.lon)),3): # same lon
               INDEX1= np.where( np.around((np.array(df_N3N.lon)),3) == np.around(np.float64(p.lon),3))
               if pd.Timestamp(p.time.date()) in tmp.date.tolist(): #same date 
                   INDEX2= np.array(np.where(np.in1d(df_N3N.date.tolist()  , pd.Timestamp(p.time.date()) ))).flatten()
                   # find 1  common element (if )
                   IDX = reduce(np.intersect1d, ( INDEX, INDEX1, INDEX2 ))
                   if len(IDX) ==1:  
                       flag =p._my_float.status_profile('NITRATE')
                       # fill the information in the dataframe 
                       df_N3N.Qc.iloc[np.array(IDX).flatten()] = flag 
                   else:  
                       raise TypeError("More than 1 float in a lat lon time position seems to be assimilated ") 



df_final         = col_to_basin(df_N3N)
df_final.to_csv('Float_assimilated_' + run + '_N3nqc.csv')

df_CHLA.columns  = LIST_COL
df_CHLA          = col_to_basin(df_CHLA)
df_O2o.columns   = LIST_COL
df_O2o           = col_to_basin(df_O2o)
