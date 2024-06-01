from sec_api_job import sec_api
from sec_api_job import sec_pop
from sec_api_job import data_processor
from sec_api_job import util
import os
import time

# sec_client = sec_api.SecApiClient('boblinlj@gmail.com')
# cik_list = sec_pop.get_sec_ticker_mapping()

# for cik in cik_list:
#     result = sec_client.get_factor(cik)
#     sec_api.create_staging_file(result,cik)



# df = file_processor.flat_dict('staging_data/0001941536_factor_2024-05-29.txt')

# sql_client.insert_df(df, False, 'sec_facts')

def run_job(filename):
    file_processor = data_processor.SecFileProcessor('2024-05-31')

    sql_client = data_processor.MySqlClient(database_ip='127.0.0.1',
                                            database_port='3306',
                                            database_user='root',
                                            database_pw='Bob060443',
                                            database_name='sec')
    start = time.time()
    filename = os.fsdecode(filename)
    df = file_processor.flat_dict(os.path.join('staging_data',filename))
    finish1 = time.time()
    sql_client.insert_df(df, False, 'sec_facts')
    finish2 = time.time()
    
    print(f"{filename} - {finish1-start} - {finish2 - finish1}")

directory = os.fsencode('staging_data')
# f = open('timer.log', 'a')
file_list = os.listdir(directory)
util.parallel_process(file_list, run_job, n_jobs=30, front_num=3, use_tqdm=True)
    
# f.close()