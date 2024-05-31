from sec_api_job import sec_api
from sec_api_job import sec_pop
from sec_api_job import  data_processor

# sec_client = sec_api.SecApiClient('boblinlj@gmail.com')
# cik_list = sec_pop.get_sec_ticker_mapping()

# for cik in cik_list:
#     result = sec_client.get_factor(cik)
#     sec_api.create_staging_file(result,cik)

file_processor = data_processor.SecFileProcessor()

file_processor.flat_dict('staging_data/0001944977_factor_2024-05-29.txt')