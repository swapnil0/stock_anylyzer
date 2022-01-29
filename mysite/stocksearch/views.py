from traceback import print_tb
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from matplotlib.pyplot import text
import requests
import pandas as pd
from pymongo import MongoClient
import io 
from django.template import Context, Template, loader
import datetime
import time
def index(request):
    return render(request, 'index.html')


def get_data(request, symbol):
    URL = "https://query1.finance.yahoo.com/v1/finance/search?q={}&lang=en-US&region=US&quotesCount=6&newsCount=2&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&researchReportsCount=2".format(symbol)
    response = requests.get(url=URL,headers={'User-agent': 'Mozilla/5.0'})
    print(response.json())
    payload = []
    if response:
        data = response.json()
        for x in data['quotes']:
            if 'symbol' in x:
                payload.append({
                    'shortname': x['shortname'],
                    'symbol': x['symbol']
                })
    return JsonResponse({
        'status': True,
        'payload': payload
    })
def load_data(request,symbol):
    start_datetime = datetime.datetime(1970, 1, 1, 10, 20)
    end_datetime = datetime.datetime.now()
    start_datetime = int(time.mktime(start_datetime.timetuple()))
    end_datetime =int(time.mktime(end_datetime.timetuple()))
    client = MongoClient('localhost:27017')
    db=client['Stock']
    FILE_URL="https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true".format(symbol,start_datetime,end_datetime)
    response = requests.get(url=FILE_URL, headers={'User-agent': 'Mozilla/5.0'})
    df=pd.read_csv(io.StringIO(response.text), sep=",")
    data=df.to_dict(orient='records')
    db[symbol].insert_many(data)
    df=df.set_index(df['Date'])
    df=df.drop("Date",axis=1)
    return HttpResponse("<head> <meta charset='UTF-8'> <title>Stock Analyser</title> <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3' crossorigin='anonymous'> <script src='https://unpkg.com/@trevoreyre/autocomplete-js'></script> <link rel='stylesheet' href='https://unpkg.com/@trevoreyre/autocomplete-js/dist/style.css'/> <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css'> <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js'> <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'> <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'> </script> <script src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js'> </script> <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js'> </script> <link rel='stylesheet' href='https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css'> <script src='https://cdn.datatables.net/1.10.23/js/jquery.dataTables.min.js'> </script> <link href='https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css' rel='stylesheet' ></head>"+df.to_html(classes='table table-striped text-center display', justify='center',)+"<script>$(document).ready( function (){$('.table').DataTable();});</script>")
