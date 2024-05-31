import pandas as pd
import os

def get_sec_ticker_mapping():
    df = pd.read_table(os.path.join('ticker','ticker.txt'), 
                    header=0, 
                    names=['ticker','cik'])
    df['cik_str'] = df['cik'].apply('{:0>10}'.format)
    cik_str_lst = df['cik_str'].to_list()
    
    return cik_str_lst
