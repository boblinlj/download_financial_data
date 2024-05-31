import os
import json
from datetime import date
from sec_api_job import util
import pandas as pd


def create_staging_file(self, json, cik):
        file=os.path.join('staging_data',f'{cik}_factor_{date.today()}.txt')
        util.write_text_file(json, file)
        return None

class SecFileProcessor():
    
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
            for item in json_data['facts'][fact]:
                for unit in json_data['facts'][fact][item]['units']:
                    data = json_data['facts'][fact][item]['units'][unit]
                    df = pd.DataFrame.from_dict(data)
                    df['unit'] = unit
                    df['item'] = item
                    df['fact'] = fact
                    df['cik'] = cik
                    stock_data.append(df)
        
        if len(stock_data) > 0:
            stock_df = pd.concat(stock_data, axis=0)
            return stock_df
        else:
            return pd.DataFrame()

