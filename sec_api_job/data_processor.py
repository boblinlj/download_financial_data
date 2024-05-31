import os
import json
from datetime import date
from sec_api_job import util
import pandas as pd
from sqlalchemy import create_engine


def create_staging_file(json, cik):
        file=os.path.join('staging_data',f'{cik}_factor_{date.today()}.txt')
        util.write_text_file(json, file)
        return None

class SecFileProcessor():
    
    def __init__(self, updated_dt) -> None:
        self.updated_dt =  updated_dt
    
    def _read_file_to_json(self, file_name) -> dict:
        f = open(file_name, 'r')
        try:
            json_data = json.load(f)
            return json_data
        except json.decoder.JSONDecodeError as e:
            print(e)
            return None
    
    def flat_dict(self, file_name) -> dict:
        json_data = self._read_file_to_json(file_name)
        # if json_data is None, return an empty dataframe
        if json_data is None: return pd.DataFrame()
        cik = json_data['cik']
        facts = json_data['facts']
        stock_data = []
        for fact in facts:
            for taxonomy in json_data['facts'][fact]:
                for unit in json_data['facts'][fact][taxonomy]['units']:
                    data = json_data['facts'][fact][taxonomy]['units'][unit]
                    df = pd.DataFrame.from_dict(data)
                    df['unit'] = unit
                    df['taxonomy'] = taxonomy
                    df['fact'] = fact
                    df['cik'] = cik
                    df['updated_date']= self.updated_dt
                    stock_data.append(df)
        
        if len(stock_data) > 0:
            stock_df = pd.concat(stock_data, axis=0)
            stock_df.to_csv('check.csv',index=False)
            return stock_df
        else:
            return pd.DataFrame()

class MySqlClient():
    def __init__(self, 
                 database_ip,
                 database_port,
                 database_user,
                 database_pw,
                 database_name
                 ) -> None:
        self.database_ip = database_ip
        self.database_port = database_port
        self.database_user = database_user
        self.database_pw = database_pw
        self.database_name = database_name
        
        self.cnn = create_engine(
                    f"""mysql+mysqlconnector://{self.database_user}"""
                    f""":{self.database_pw}"""
                    f"""@{self.database_ip}"""
                    f""":{self.database_port}"""
                    f"""/{self.database_name}""",
                    pool_size=20,
                    max_overflow=0
                    )
    
    def insert_df(self, df, insert_index, table):
        df.to_sql(name=table,
                  con=self.cnn,
                  if_exists='append',
                  index=insert_index,
                  method='multi',
                  chunksize=1)