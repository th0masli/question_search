# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
import json
from django.shortcuts import render
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import pymysql
import re


# Create your views here.
es=Elasticsearch("elastic:changeme@106.75.36.191:8001", verify_certs=True)#10.2.1.13
question_bank_conn=pymysql.connect(host='10.10.118.78',port=3306,
                                   user='rd',password='mTUzu4DnD4tjASGmohYhyPQn6TrYeveb',
                                   db='question_bank_clean0605',charset='utf8')#线上环境

# question_bank_conn=pymysql.connect(host='10.2.1.106',port=3306,
#                                    user='wenba',password='4g5tg4e65ywt5u7h6b8iu798',
#                                    db='question_bank_clean0816',charset='utf8')
def home(request):
    return render(request,'index.html')

def get_results(request):

    keywords=request.POST.get('keywords')
    _query_all = {
        'query': {
            'match_phrase': {'ocrResult':keywords}
        }
    }
    res=es.search(index='xbj_index', doc_type='xbj_type', body=_query_all,request_timeout=30)
    hits=res['hits'].get('hits',None)
    if len(hits)==0:
        hits=None
    result={'hits':hits,'keywords':keywords}
    #return JsonResponse(result, safe=False)
    return render(request, 'feed.html', result)

def get_question(request, question_id):
    question_id=int(question_id)
    cursor=question_bank_conn.cursor()
    sql='select stem_html, hint, answer, remark from questions where id=%s;' % question_id
    row_num=cursor.execute(sql)
    data={}
    question_list=[]
    data['question_id']=question_id
    data['message']='ok'
    if row_num != 0:
        question={}
        row=cursor.fetchone()
        question['item_content'] = \
            re.sub('/question\_bank',
                   'http://7o4zgy.com2.z0.glb.qiniucdn.com/question_bank',
                   row[0]).strip()
        question['answer'] = \
            re.sub('/question\_bank',
                   'http://7o4zgy.com2.z0.glb.qiniucdn.com/question_bank',
                   row[2]).strip()
        question['hint'] = \
            re.sub('/question\_bank',
                   'http://7o4zgy.com2.z0.glb.qiniucdn.com/question_bank',
                   row[1]).strip()
        question['remark'] = \
            re.sub('/question\_bank',
                   'http://7o4zgy.com2.z0.glb.qiniucdn.com/question_bank',
                   row[3]).strip()
        question_list.append(question)
    data['question_list'] = question_list
    # 每页显示5题
    data['question_num'] = len(question_list)
    return render(request,'matrix.html',data)





