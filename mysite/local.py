import requests

import requests

URL = "https://query1.finance.yahoo.com/v1/finance/search?q=reli&lang=en-US&region=US&quotesCount=6&newsCount=2&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&researchReportsCount=2"
r = requests.get(url=URL, headers={'User-agent': 'Mozilla/5.0'})
data = r.json()

print(data)
