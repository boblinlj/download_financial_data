from sec_api_job import sec_api
from sec_api_job import sec_pop
from sec_api_job import  data_processor
import os

# sec_client = sec_api.SecApiClient('boblinlj@gmail.com')
# cik_list = sec_pop.get_sec_ticker_mapping()

# for cik in cik_list:
#     result = sec_client.get_factor(cik)
#     sec_api.create_staging_file(result,cik)

file_processor = data_processor.SecFileProcessor('2024-05-31')

sql_client = data_processor.MySqlClient(database_ip='127.0.0.1',
                                        database_port='3306',
                                        database_user='root',
                                        database_pw='Bob060443',
                                        database_name='sec')

# df = file_processor.flat_dict('staging_data/0001941536_factor_2024-05-29.txt')

# sql_client.insert_df(df, False, 'sec_facts')

directory = os.fsencode('staging_data')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    df = file_processor.flat_dict(os.path.join('staging_data',filename))
    sql_client.insert_df(df, False, 'sec_facts')