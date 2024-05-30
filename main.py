from download_data import sec_api
from stock_population import sec_pop

sec_client = sec_api.SecApiClient('boblinlj@gmail.com')
cik_list = sec_pop.get_sec_ticker_mapping()

for cik in cik_list:
    result = sec_client.get_factor(cik)
    sec_api.create_staging_file(result,cik)