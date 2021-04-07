# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np
import requests as req
import matplotlib.pyplot as plt
import re
import time
from bs4 import BeautifulSoup as bs
from datetime import date
from fake_useragent import UserAgent

#HTMLの取得
def get_html(url, useragent):
    headers = {"User-Agent":useragent}
    res = req.get(url,headers=headers)
    return res

#バイヤー一覧作成処理
def createBuyerList(items, itemList):
    #商品を取得
    for item in items:
        #リストに追加
        itemList.append({
            #バイヤーID
            "buyer_id":item.find(class_="product_Buyer").find("a").get("href").split("/")[2].replace(".html", ""),
            #バイヤー名
            "buyer_name":item.find(class_="product_Buyer").text.replace("\n", ""),
            #バイヤーurl
            "buyer_url":"https://www.buyma.com" + item.find(class_="product_Buyer").find("a").get("href"),
            #バイヤー表示数
            "buyer_disp_num":0,
        })

def detail(detail_sp, buyer_id):
    #出品数
    buyer_item_num = int(detail_sp.find(class_="selling").find("span").text)
    #注文実績
    buyer_order_num = 0
    for buyer_eva_text in detail_sp.findAll(class_="buyer_eva_text"):
        #件が含まれる場合
        if "件" in buyer_eva_text.text:
            buyer_order_num = int(buyer_eva_text.text.strip().replace("件", ""))
    
    #差分
    diff = abs(buyer_order_num - buyer_item_num)
    #優良フラグ
    excellent_flg = 0
    #注文実績が出品数より多い場合
    if buyer_order_num > buyer_item_num:
        excellent_flg = 1
    else:
        excellent_flg = 0

    return{
        #バイヤーID
        "buyer_id":buyer_id,
        #出品数
        "buyer_item_num":buyer_item_num,
        #注文実績
        "buyer_order_num":buyer_order_num,
        #差分
        "diff":diff,
        #優良フラグ
        "excellent_flg":excellent_flg,
    }

# 検索URL
category_url = sys.argv[1]

#UserAgentの作成
ua = UserAgent(use_cache_server=False)
useragent = ua.random
print("サブプロセス呼び出し")
print("サブプロセス待機")
time.sleep(30)
print("サブプロセス待機終了")