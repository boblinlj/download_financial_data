import  requests
import xmltodict
import pandas as pd

url = "https://www.sec.gov/Archives/edgar/xbrl-inline.rss.xml"
# url = 'https://www.sec.gov/Archives/edgar/xbrlrss.all.xml'
def fetch_filings_from_rss(url):
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
    

rss_str = fetch_filings_from_rss(url)



