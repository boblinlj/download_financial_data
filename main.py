from download_data import download_from_sec_api

# cik = get_sec_ticker_mapping()[100]
# url = build_url(cik)
# print(url)
# request_api(url)

download_from_sec_api.write_json_to_file('text','test')