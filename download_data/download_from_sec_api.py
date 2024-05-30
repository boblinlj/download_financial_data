import requests
import pathlib
import os
import pandas as pd
from sqlalchemy import create_engine
from pyrate_limiter import Duration, Limiter, Rate
from datetime import date

# 10 requests per second rate limit set by SEC:
# https://www.sec.gov/os/webmaster-faq#developers
SEC_THROTTLE_LIMIT_RATE = Rate(10, Duration.SECOND)

# Wait up to 60 seconds for the rate-limiter bucket to refill.
# If the bucket does NOT refill, an exception will be raised.
limiter = Limiter(
    SEC_THROTTLE_LIMIT_RATE, raise_when_fail=True, max_delay=60_000
).as_decorator()


def limiter_mapping(*args):
    return "sec_edgar_api_rate_limit", 1

HEADER ={'user-agent': 'boblinlj@gmail.com',
         'accept-encoding':'gzip, deflate',
         'host':'data.sec.gov',
         }

@limiter(limiter_mapping)
def request_api(url):
    s = requests.Session()
    s.headers.update(HEADER)
    r =  s.get(url = url)

    return r.text

def build_url(cik):
    base_url = "https://data.sec.gov/api/xbrl"
    company_facts = f"/companyfacts/CIK{cik}.json"
    
    return base_url + company_facts

def get_sec_ticker_mapping():
    cwd = pathlib.Path.cwd()
    df = pd.read_table(os.path.join(cwd,'ticker.txt'), 
                       header=0, 
                       names=['ticker','cik'])
    df['cik_str'] = df['cik'].apply('{:0>10}'.format)
    cik_str_lst = df['cik_str'].to_list()
    
    return cik_str_lst

def write_text_file(text_input, output_file):
    f = open(output_file, "w")
    f.write(text_input)
    f.close()
    return None

if __name__ == '__main__':
    # cik = get_sec_ticker_mapping()[100]
    # url = build_url(cik)
    # print(url)
    # request_api(url)
    
    write_json_to_file('text','test')