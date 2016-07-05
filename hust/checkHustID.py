#!/usr/local/bin/python35
# coding=utf-8
# -*- coding：utf-8 -*-
import urllib.request
import http.cookiejar
import re
import os
import time
import urllib.parse


##'Accept': '*/*'
##'Accept-Language': 'zh-CN'
##'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'
##'Accept-Encoding': 'gzip, deflate'
##'Connection': 'Keep-Alive'
##'Host': 'freshman.hust.edu.cn:8080'

header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://freshman.hust.edu.cn:8080/yxxt/zzyx/xsLogin_initMm.do',
        'Accept-Language': 'zh-CN',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
        'Connection': 'Keep-Alive',
        'Content-Length': '75',
        'Host': 'freshman.hust.edu.cn:8080',
        'Pragma': 'no-cache',
	#'Cache-Control': 'max-age=0',
	#'Upgrade-Insecure-Requests': '1',
}


def getMyOpener(head):
	#print(head)
	cookies = http.cookiejar.CookieJar()
	processor = urllib.request.HTTPCookieProcessor(cookies)
	opener = urllib.request.build_opener(processor)
	header = []
	for key, value in head.items():
		elem = (key, value)
		header.append(elem)
	#print(header)
	opener.addheaders = header
	return opener

def makePost(url,data):
        datas=urllib.parse.urlencode(data)
        req=urllib.request.Request(url, datas.encode('gb2312'))
        with getMyOpener(header).open(req) as pages:
                response=pages.read().decode()
        #print(response)
        return response

def getContents(url):
        with getMyOpener(header).open('http://www.jnszxyy.com:8082/?orderMain?') as pages:
                response=pages.read().decode()
        return response

def makeGet(url,data):
        datas=urllib.parse.urlencode(data)  
        req=urllib.request.Request(url+"?"+datas)
        with getMyOpener(header).open(req) as pages:
                response=pages.read().decode()
        return response

startId = 1600000
tagetUrl="http://freshman.hust.edu.cn:8080/yxxt/zzyx/xsLogin_cshMm.do"


while True:
        startId+=1
        print(startId)
        values["content"]='xm='+ '%d'%startId +''
             
        rep = makePost(tagetUrl,values)
        if(rep.find('fail')<1):
                print(values)
                print(rep)
                break;
        if(startId>1607000):
                break;
        


