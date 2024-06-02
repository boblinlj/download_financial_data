import requests
import pandas as pd
from pyrate_limiter import Duration, Limiter, Rate
import xmltodict

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

class SecApiClient():
    def __init__(self, email) -> None:
        self.email_for_user_agent = email
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": self.email_for_user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Host": "data.sec.gov",
            }
        )

    def build_url(self, cik):
        base_url = "https://data.sec.gov/api/xbrl"
        company_facts = f"/companyfacts/CIK{cik}.json"
        
        return base_url + company_facts  
    
    @limiter(limiter_mapping)
    def request_api(self, url):
        r =  self._session.get(url = url)
        
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            
        return r.text

    def get_factor(self, cik):
        url = self.request_api(cik)
        return self.request_api(url)

class SecRSSClient():
    def fetch_filings_from_rss(self, url):
        exit_data = dict()
        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0'})
        r = s.get(url)
        feed = xmltodict.parse(r.content)
        pubDate = feed['rss']['channel']['pubDate'].replace(" EDT","")
        title =  feed['rss']['channel']['title']
        for item in feed['rss']['channel']['item']:
            formType = item['edgar:xbrlFiling'].get('edgar:formType')
            cikNumber = item['edgar:xbrlFiling'].get('edgar:cikNumber')
            companyName = item['edgar:xbrlFiling'].get('edgar:companyName')
            filingDate = item['edgar:xbrlFiling'].get('edgar:filingDate')
            fiscalYearEnd = item['edgar:xbrlFiling'].get('edgar:fiscalYearEnd')
            exit_data[cikNumber]=[formType, pubDate, title, companyName, filingDate, fiscalYearEnd]

        df = pd.DataFrame.from_dict(exit_data, 
                                    orient='index',
                                    columns=['formType', 'pubDate', 'title', 'companyName', 'filingDate', 'fiscalYearEnd']
                                    )
        df.reset_index(inplace=True)
        df.rename(columns={'index':'cik'},inplace=True)
        df['pubDate'] = pd.to_datetime(df['pubDate'])
        df['filingDate'] = pd.to_datetime(df['filingDate'])
        
        return df

if __name__ == '__main__':
    pass