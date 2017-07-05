# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
import json
from django.shortcuts import render
from elasticsearch import Elasticsearch
import elasticsearch.helpers



# Create your views here.
es=Elasticsearch("10.2.1.13:9200")

def home(request):
    return render(request,'index.html')

def get_results(request):

    keywords=request.POST.get('keywords')
    _query_all = {
        'query': {
            'match_phrase': {'ocrResult':keywords}
        }
    }
    res=es.search(index='xuebajun', doc_type='feed', body=_query_all)
    hits=res['hits'].get('hits',None)
    if len(hits)==0:
        hits=None
    result={'hits':hits,'keywords':keywords}
    #return JsonResponse(result, safe=False)
    return render(request, 'matrix.html', result)