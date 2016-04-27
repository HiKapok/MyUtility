#!/usr/local/bin/python35
# coding=utf-8
# -*- coding：utf-8 -*-
import urllib.request
import http.cookiejar
import re
import os
import time

##url = "http://www.baidu.com"
##data = urllib.request.urlopen(url).read()
##data = data.decode('UTF-8')
##print(data)
##urldata = urllib.parse.urlencode(data)
##print(urldata)

def getMyOpener(head):
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


header = {
    'Host': 'www.jnszxyy.com:8082',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Referer': 'http://www.jnszxyy.com:8082/?net_order?',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}
invalidTbl=[]
dateTbls = {}
responsReg = re.compile('new Array\(.+\)')
def makeOrder():
    ##params = urllib.parse.urlencode(header)
    ##url = "http://www.jnszxyy.com:8082/"
    ##with urllib.request.urlopen(url) as f:
    ##    print(f.read().decode('GBK'))
    #"http://www.jnszxyy.com:8082/"
    dateTbls.clear()
    with getMyOpener(header).open('http://www.jnszxyy.com:8082/?orderMain?') as f:
       datas=f.read().decode('GBK')
    #print(datas)
    reg = re.compile('[0-9]{2,4},\"陈健\",[0-9]{2,4}')
    strlist = reg.findall(datas)

    if strlist is None:
        print("failed to find doctor:陈健.")
        return 2
        os._exit(1)

    mat = re.search('[0-9]{2,4}',strlist[0])
    if mat is None:
        print("failed to get doctor's id.")
        with open('log.txt', 'a') as f:
            print('%s:找不到医生编号'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
        os._exit(1)
    doctorId = mat.group()
    print("doctor'id is:%s"%doctorId)
    with open('log.txt', 'a') as f:
        print('%s:医生编号：%s'%(time.strftime('%Y-%m-%d %X',time.localtime()),doctorId), file=f)
    indexReg = re.compile('[0-9]{2,4},\"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}\",'+doctorId)
    dates = indexReg.findall(datas)

    if len(dates) is 0:
        print("failed to find any valid date.")
        with open('log.txt', 'a') as f:
            print('%s:找不到有效日期'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
        os._exit(1)

    chsReg = re.compile('已约完')
    keyTbls = []
    print('可预约的日期：')
    for str in dates:
        print(str)   
        spittbl = str.split(',')
        keyReg = re.compile('[0-9]{5,7},\"[0-9]{2}:[0-9]{2} ━━ [0-9]{2}:[0-9]{2}.{0,10}\",'+spittbl[0])
        keys = keyReg.findall(datas)

        if len(keys) is 0:
            print("failed to find any work time.")
            with open('log.txt', 'a') as f:
                print('%s:找不到有效的预约时间'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
            os._exit(1)

        for substr in keys:
            #print(substr)
            if len(chsReg.findall(substr)) is 0:
                keyTbls.append(substr)
                #if dateTbls.has_key(spittbl[0]) is True:
                #    dateTbls[spittbl[0]]= spittbl[1][1:-1]
                #else:
                #elem = (spittbl[0], spittbl[1][1:-1])
                #dateTbls.append(elem)    
                #elem = (spittbl[0], spittbl[1][1:-1])
                dateTbls[spittbl[0]]= spittbl[1][1:-1]
                
                #dateTbls.append(elem)
    failedReg = re.compile('号源已用尽')
    #for key, value in dateTbls.items():
    #    print(key+value)
    for str in keyTbls:
        #print(str)
        mats = re.search('[0-9]{5,7},',str)
        if mats is None:
            continue
        keystr = mats.group()[:-1]
        if keystr in invalidTbl:
            continue
        str = re.compile(' ━━ ').sub('-',str)
        with open('log.txt', 'a') as f:
            print('%s:尝试预约：%s'%(time.strftime('%Y-%m-%d %X',time.localtime()),str), file=f)
        urls = 'http://www.jnszxyy.com:8082/?orderSave?Appoints_ID='+keystr+'&str_xingming=%CD%F5%B2%FD%B0%B2&str_yxzjhm=370481199312173854&str_phone=18366118438&str_address=%C9%BD%B6%AB%B4%F3%D1%A7%C7%A7%B7%F0%C9%BD%D0%A3%C7%F8&str_ykthm=&str_csrq=1993-12-17&str_childPname=&str_email=&str_sex=%C4%D0'
        #print(urls)
        with getMyOpener(header).open(urls) as f:
            responses=f.read().decode('GBK')
            #print(responses)    
            retTbls = responsReg.findall(responses)
            if len(retTbls) is 0:
                print("failed to get order response.")
                with open('log.txt', 'a') as f:
                    print('%s:预约响应出错'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
                    os._exit(1)
                    
            with open('log.txt', 'a') as f:
                print('%s:预约响应为：%s'%(time.strftime('%Y-%m-%d %X',time.localtime()),retTbls[0].split(',')[1][1:-1]), file=f)  
            if len(failedReg.findall(responses)) is 0:
                tempsplit = str.split(',')
                tempstr = dateTbls[tempsplit[2]] + ' ' + tempsplit[1][1:-1]
                #tempstr = re.compile(' ━━ ').sub('-',tempstr)
                with open('log.txt', 'a') as f:
                    print('%s:预约成功！时间：%s'%(time.strftime('%Y-%m-%d %X',time.localtime()),tempstr), file=f)  
                print("ok!time:%s"%tempstr)
                return 1
            else:
                invalidTbl.append(keystr)
    return 0


with open('log.txt', 'w') as f:
    print('%s:开始预约...'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
cnt = 0
while True:
    cnt+=1
    with open('log.txt', 'a') as f:
        print('%s:第%d次尝试预约...'%(time.strftime('%Y-%m-%d %X',time.localtime()),cnt), file=f)
    print('预约中...')
    res = makeOrder()
    if res is 1:
        break
    elif res is 2:
        with open('log.txt', 'a') as f:
            print('%s:无法找到医生陈健'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
        break
    time.sleep(15)
print('恭喜预约成功...')


