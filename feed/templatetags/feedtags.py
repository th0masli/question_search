# -*- coding: utf-8 -*-

from django import template
import time
register = template.Library()

#模板中不能出现下划线
def get_source(value):
    return value.get('_source','')

def source_fid(value):
    return value.get('_id','')

def source_uid(value):
    return value.get('_source','').get('uid')

def source_ocrResult(value):
    return value.get('_source','').get('ocrResult')

def source_time(value):
    createTime= value.get('_source','').get('createTime')
    createTime=time.localtime(createTime)
    return time.strftime('%Y-%m-%d %H:%M:%S',createTime)

def source_searchResult(value):
    srs=value.get('_source','').get('searchResult')
    ids=[]
    for sr in srs:
        ids.append(sr.get('id'))
    return ids

register.filter('get_source',get_source)
register.filter('source_fid',source_fid)
register.filter('source_uid',source_uid)
register.filter('source_time',source_time)
register.filter('source_ocrResult',source_ocrResult)
register.filter('source_searchResult',source_searchResult)