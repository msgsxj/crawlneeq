# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:14:56 2018

@author: msgsxj
"""

import time
import json
import re
import pandas as pd
import requests

def gethomepagedata(): # sbzs, sbcz, market = gethomepagedata()
    time_start=time.time()
    url_sbzs = 'http://www.neeq.com.cn/neeqController/getMinu.do?callback=jQuery18305096780566754533_1523369354341&_=1523370667670'
    url_sbcz = 'http://www.neeq.com.cn/neeqController/getSBCZ.do?callback=jQuery18305096780566754533_1523369354343'
    url_market = 'http://www.neeq.com.cn/nqxxController/getMarketData.do?callback=jQuery18307255220064667056_1523371119904'
    sbzs = requests.get(url_sbzs).text
    sbcz = requests.get(url_sbcz).text
    market = requests.get(url_market).text
    time_end=time.time()
    print('get home page data cost:',time_end - time_start,'s')
    return sbzs, sbcz, market

def getstockdata(): # zhang, die, cje = getstockdata()
    time_start=time.time()
    url_zhang = 'http://www.neeq.com.cn/nqhqController/nqhq.do?callback=jQuery18304718930715294276_1523372978803&page=0&type=Z&zqdm=&sortfield=hqzdf&sorttype=desc&xxfcbj=&keyword=&_=1523372983237'
    url_die = 'http://www.neeq.com.cn/nqhqController/nqhq.do?callback=jQuery18304718930715294276_1523372978803&page=0&type=Z&zqdm=&sortfield=hqzdf&sorttype=asc&xxfcbj=&keyword=&_=1523373009190'
    url_cje = 'http://www.neeq.com.cn/nqhqController/nqhq.do?callback=jQuery18304718930715294276_1523372978803&page=0&type=Z&zqdm=&sortfield=hqcjje&sorttype=desc&xxfcbj=&keyword=&_=1523373027130'
    zhang = requests.get(url_zhang).text
    die = requests.get(url_die).text
    cje = requests.get(url_cje).text
    time_end=time.time()
    print('get stock data cost:',time_end - time_start,'s')
    return zhang, die, cje

def getxyzrdata(): # xyzr = getxyzrdata()
    time_start=time.time()
    url_xyzr_1 = 'http://www.neeq.com.cn/tnqfgkcjxxController/btcjxxList.do?callback=jQuery18305672955896310246_1523373137519&page='
    url_xyzr_2 = '&btjsrq=&sortfield=hqjsrq&sorttype=desc&position=first&_=1523373148594'
    i = 0
    xyzr = []
    while(1):
        url_xyzr = url_xyzr_1 + str(i) + url_xyzr_2
        page = requests.get(url_xyzr).text
        xyzr.append(page)
        xyzr_confirm = page[-126:] # confirm "lastPage":true
        flag = re.compile(r'"lastPage":true').findall(xyzr_confirm)
        if (flag != []):
            break
        else:
            i = i + 1
    time_end=time.time()
    print('get 协议转让 data cost:',time_end - time_start,'s')
    return xyzr

def dataclean():
    DATA = {}
    DATA_zhang = []
    DATA_die = []
    DATA_cje = []
    DATA_xyzr = []
    ### get data
    sbzs, sbcz, market = gethomepagedata() 
    zhang, die, cje = getstockdata()
    xyzr = getxyzrdata()
    ### sdzs
    sbzs_pre = sbzs[41:-1] # clean head and tail 
    sbzs_json = json.loads(sbzs_pre)[-1] # last line is the latest
    DATA['SSZS_num'] = sbzs_json['SSZS']
    DATA['SSZS_rate'] = sbzs_json['ZDF']
    DATA['SSZS_date'] = sbzs_json['JSRQ']
    ### sbcz
    sbcz_pre = sbcz[41:-1] # clean head and tail 
    sbcz_json = json.loads(sbcz_pre)[-1] # last line is the latest
    DATA['SSCZ_num'] = sbcz_json['drkp']
    DATA['SSCZ_rate'] = sbcz_json['zdf']
    DATA['SSCZ_date'] = sbcz_json['jsrq']
    ### market
    market_pre = market[41:-1] # clean head and tail
    market_json = json.loads(market_pre)
    DATA['ZT_num'] = market_json[2]['hqcjje']
    DATA['JHJJ_num'] = market_json[3]['hqcjje']
    DATA['ZS_num'] = market_json[4]['hqcjje']
    DATA['CXC_num'] = market_json[6]['hqcjje']
    ### stock
    # 涨前5
    zhang_pre = zhang[41:-1] # clean head and tail
    zhang_json = json.loads(zhang_pre)[0]['content'][:5] # top 5
    for i in range(len(zhang_json)):
        temp = []
        temp.append(zhang_json[i]["hqzqdm"]) #证券代码
        temp.append(zhang_json[i]["hqzqjc"]) #证券简称
        temp.append(zhang_json[i]["hqzdf"])  #涨幅
        DATA_zhang.append(temp)
    # 跌前5 
    die_pre = die[41:-1] # clean head and tail
    die_json = json.loads(die_pre)[0]['content'][:5] # top 5
    for i in range(len(die_json)):
        temp = []
        temp.append(die_json[i]["hqzqdm"]) #证券代码
        temp.append(die_json[i]["hqzqjc"]) #证券简称
        temp.append(die_json[i]["hqzdf"])  #跌幅
        DATA_die.append(temp)
    # 成交额前5 
    cje_pre = cje[41:-1] # clean head and tail
    cje_json = json.loads(cje_pre)[0]['content'][:5] # top 5
    for i in range(len(cje_json)):
        temp = []
        temp.append(cje_json[i]["hqzqdm"]) #证券代码
        temp.append(cje_json[i]["hqzqjc"]) #证券简称
        temp.append(cje_json[i]["hqcjje"]) #成交额
        DATA_cje.append(temp)
    ### xyzr
    for pages in range(len(xyzr)):
        xyzr_pre = xyzr[pages][41:-1] # clean head and tail 
        xyzr_json = json.loads(xyzr_pre)[0]['content']
        for i in range(len(xyzr_json)):
            temp = []
            temp.append(xyzr_json[i]["hqzqdm"]) #证券代码
            temp.append(xyzr_json[i]["hqzqjc"]) #证券简称
            temp.append(xyzr_json[i]["hqcjjg"]) #成交价
            temp.append(xyzr_json[i]["hqcjsl"]) #成交量
            DATA_xyzr.append(temp)
    return DATA, DATA_zhang, DATA_die, DATA_cje, DATA_xyzr

def main():
    DATA, DATA_zhang, DATA_die, DATA_cje, DATA_xyzr = dataclean()
    writer = pd.ExcelWriter(r'neep.xlsx')
    DATA_list = list(DATA.items()) # 字典转化list再转化dataframe 
    DATA_df = pd.DataFrame(DATA_list)
    DATA_df.columns = ["英文缩写","数据"]
    DATA_df.to_excel(writer,'主页信息',index=False)
    DATA_zhang_df = pd.DataFrame(DATA_zhang)
    DATA_zhang_df.columns = ["证券代码","证券简称","涨幅"]
    DATA_zhang_df.to_excel(writer,'涨幅前5',index=False)
    DATA_die_df = pd.DataFrame(DATA_die)
    DATA_die_df.columns = ["证券代码","证券简称","跌幅"]
    DATA_die_df.to_excel(writer,'跌幅前5',index=False)
    DATA_cje_df = pd.DataFrame(DATA_cje)
    DATA_cje_df.columns = ["证券代码","证券简称","成交额(元)"]
    DATA_cje_df.to_excel(writer,'成交额前5',index=False)
    DATA_xyzr_df = pd.DataFrame(DATA_xyzr)
    DATA_xyzr_df.columns = ["证券代码","证券简称","成交价","成交量(股)"]
    DATA_xyzr_df.to_excel(writer,'协议转让',index=False)
    writer.save()
    
if __name__=="__main__":
    main()
    




