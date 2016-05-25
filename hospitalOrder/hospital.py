#!/usr/local/bin/python35
# coding=utf-8
# -*- coding：utf-8 -*-
import urllib.request
import http.cookiejar
import re
import os
import time
import smtplib
import imaplib
import datetime
import email.mime.multipart
from email.mime.text import MIMEText

##url = "http://www.baidu.com"
##data = urllib.request.urlopen(url).read()
##data = data.decode('UTF-8')
##print(data)
##urldata = urllib.parse.urlencode(data)
##print(urldata)

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


header = {
    'Host': 'www.jnszxyy.com:8082',
    'Connection': 'keep-alive',
    #'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Referer': 'http://www.jnszxyy.com:8082/?net_order?',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}

header_next={
    'Host': 'www.jnszxyy.com:8082',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}
invalidTbl=[]
dateTbls = {}
responsReg = re.compile('new Array\(.+\)')
cnt = 0
def makeOrder(num,ampmreg,timereg,requeststring):
    ##params = urllib.parse.urlencode(header)
    ##url = "http://www.jnszxyy.com:8082/"
    ##with urllib.request.urlopen(url) as f:
    ##    print(f.read().decode('GBK'))
    #"http://www.jnszxyy.com:8082/"
    dateTbls.clear()
    #print(num)
    #if num == 1:    
    with getMyOpener(header).open('http://www.jnszxyy.com:8082/?orderMain?') as f:
        datas=f.read().decode('GBK')
    #else:
    #    with getMyOpener(header_next).open('http://www.jnszxyy.com:8082/?orderMain?') as f:
    #       datas=f.read().decode('GBK')
    #print(datas)
    reg = re.compile('[0-9]{2,4},\"陈健\",[0-9]{2,4}')
    strlist = reg.findall(datas)

    if strlist is None:
        print("failed to find doctor:陈健.")
        return 2,'无法找到医生陈健.'
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
    #indexReg = re.compile('[0-9]{2,4},\"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}\",'+doctorId)
    indexReg = re.compile(timereg+doctorId)
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
        #am and pm
        #keyReg = re.compile('[0-9]{5,7},\"[0-9]{2}:[0-9]{2} ━━ [0-9]{2}:[0-9]{2}.{0,10}\",'+spittbl[0])
        #am
        keyReg = re.compile(ampmreg+spittbl[0])
        #pm
        #keyReg = re.compile('[0-9]{5,7},\"1[3-7]:[0-9]{2} ━━ 1[3-7]:[0-9]{2}.{0,10}\",'+spittbl[0])
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
            
        #print(keystr)
        urls = 'http://www.jnszxyy.com:8082/?orderSave?Appoints_ID='+keystr+requeststring
        #os._exit(1)
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
                return 1,'恭喜您预约成功！时间：'+tempstr+'\r\n'+retTbls[0].split(',')[1][1:-1]+'\r\n网络预约查询网址：'+"http://www.jnszxyy.com:8082/?orderSearch?"
            else:
                invalidTbl.append(keystr)
    return 0,''

name=''
sex=''
addr=''
idnum=''
phonenum=''
timerange=''
am_or_pm=''
mailaddr=''

with open('configure.txt', 'r') as f:
    namestr = f.readline().strip().split('%')[-1]
    print('姓名：%s'%namestr)
    #name = namestr.split('%')[-1].encode('GB2312')
    #bb='123'.encode('GB2312')
    for byte in namestr.encode('GB2312'):
        #print(byte)
        name=name+'%{0:X}'.format(byte)
    #print(name)
    sexstr = f.readline().strip().split('%')[-1]
    print('性别：%s'%sexstr)
    for byte in sexstr.encode('GB2312'):
        sex=sex+'%{0:X}'.format(byte)
    idnumstr = f.readline()
    idnum = idnumstr.strip().split('%')[-1]
    print('身份证号：%s'%idnum)
    phonenumstr = f.readline()
    phonenum = phonenumstr.strip().split('%')[-1]
    print('手机号：%s'%phonenum)
    addrstr = f.readline().strip().split('%')[-1]
    for byte in addrstr.encode('GB2312'):
        #print(byte)
        if byte<123:
            addr=addr+'{0:c}'.format(byte)
        else:
            addr=addr+'%{0:X}'.format(byte)
    
    timerangestr = f.readline()
    timerange = timerangestr.strip().split('%')[-1]
    am_or_pm_str = f.readline()
    am_or_pm = am_or_pm_str.strip().split('%')[-1]
    mailstr = f.readline()
    mailaddr = mailstr.strip().split('%')[-1]
    print('邮箱：%s'%mailaddr)

inputstr = input("请输入ok以确认以上信息正确：")
if inputstr != 'ok':
    os._exit(1)
    
##print(name)
##print(idnum)
##print(phonenum)
##print(addr)
##print(am_or_pm)
##print(timerange)
##print(mailaddr)

##print(idnum[6:10])
##print(idnum[10:12])
##print(idnum[12:14])
requeststr='&str_xingming='+name+'&str_yxzjhm='+idnum+'&str_phone='+phonenum+\
            '&str_address='+addr+'&str_ykthm=&str_csrq='+idnum[6:10]+'-'+\
            idnum[10:12]+'-'+idnum[12:14]+'&str_childPname=&str_email=&str_sex='+\
            sex

timereg='[0-9]{2,4},\\"[0-9]{4}-[0-9]{1,2}-[0-9]['+timerange+']\\",'
ampmreg=''
if am_or_pm=='a':
    ampmreg='[0-9]{5,7},\\"[01][8-9|0-2]:[0-9]{2} ━━ [01][8-9|0-2]:[0-9]{2}.{0,10}\\",'
elif am_or_pm=='b':
    ampmreg='[0-9]{5,7},\\"1[3-7]:[0-9]{2} ━━ 1[3-7]:[0-9]{2}.{0,10}\\",'
else:
    ampmreg='[0-9]{5,7},\\"[0-9]{2}:[0-9]{2} ━━ [0-9]{2}:[0-9]{2}.{0,10}\\",'

##print(requeststr)
##print(timereg)
##print(ampmreg)

def mail_login(username,passwd):
    print("登陆邮箱...")
    while True:
        try:
            imap = imaplib.IMAP4_SSL('imap.aliyun.com')
            d = imap.login(username, passwd)
            print("登陆成功:%s"%d[-1])
        except Exception as e:
            print(str(e))     
        break

def sendEmailMIME(username,password,destination,subject,message,file):
    plainTxt = MIMEText(message,_subtype='plain',_charset='gb2312')
    msg = email.mime.multipart.MIMEMultipart()
    attachs = MIMEText(open(file, 'rb').read(), 'base64', 'gb2312')
    attachs["Content-Type"] = 'application/octet-stream'
    attachs["Content-Disposition"] = 'attachment; filename="order_log.txt"'
    msg['to'] = destination
    msg['from'] = username
    msg['subject'] = subject
    msg['Date'] = datetime.datetime.now().strftime("%H:%M:%S %d-%b-%Y")
    msg.attach(plainTxt)
    msg.attach(attachs)
    try:
        smtp = smtplib.SMTP('smtp.aliyun.com',25)
        smtp.ehlo()
        #smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(msg['from'], msg['to'], msg.as_string())
        return True
    except smtplib.SMTPException as e:
        print(str(e))
        return False
	
	
def sendEmail(username,password,destination,subject,message):
    content = MIMEText(message,_subtype='plain',_charset='gb2312') 
    content['Subject'] = subject
    content['From'] = username
    content['To'] = destination
    content['Date'] = datetime.datetime.now().strftime("%H:%M:%S %d-%b-%Y")
    #content['Date'] = formatdate(localtime=True)
    try:
        smtp = smtplib.SMTP('smtp.aliyun.com',25)
        smtp.ehlo()
        #smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(username, destination, content.as_string())
        return True
    except smtplib.SMTPException as e:
        print(str(e))
        return False
		        
with open('log.txt', 'w') as f:
    print('%s:开始预约...'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)

while True:
    cnt+=1
    with open('log.txt', 'a') as f:
        print('%s:第%d次尝试预约...'%(time.strftime('%Y-%m-%d %X',time.localtime()),cnt), file=f)
    print('预约中...')
    res,strings = makeOrder(cnt,ampmreg,timereg,requeststr)
    if res is 1:
        break
    elif res is 2:
        with open('log.txt', 'a') as f:
            print('%s:无法找到医生陈健'%time.strftime('%Y-%m-%d %X',time.localtime()), file=f)
        break
    time.sleep(10)
if res is 1:
    if mailaddr != '':
        mail_login("python_program@aliyun.com","")
        sendEmailMIME("python_program@aliyun.com","",mailaddr,"中心医院自动预约结果通知",strings,'log.txt')
    
print('恭喜预约成功...')


