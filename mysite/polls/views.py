from django.http import HttpResponse
from django.shortcuts import render
from .models import Names
from django.http import JsonResponse
import requests


def index(request):
    return render(request, 'index.html')


def get_data(request):
    # search = request.GET.get('search')
    URL = "https://query1.finance.yahoo.com/v1/finance/search?q=reli&lang=en-US&region=US&quotesCount=6&newsCount=2&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&researchReportsCount=2"
    response = requests.get(url=URL, headers={'User-agent': 'Mozilla/5.0'})

    payload = []
    if response:
        data = response.json()
        for x in data['quotes']:
            if 'symbol' in x:
                print('---x', x['symbol'])
                payload.append({
                    'symbol': x['symbol']
                })
    return JsonResponse({
        'status': True,
        'payload': payload
    })