# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np
import requests as req
import matplotlib.pyplot as plt
import re
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
    
#バイヤー一覧
itemList = []
for _ in range(5):
    #HTML取得
    res = get_html(category_url, useragent)
    #HTMLの整形
    soup = bs(res.content, "html.parser")
    #商品一覧情報を取得
    items = soup.findAll(class_="product")
    #バイヤー一覧の作成
    createBuyerList(items, itemList)
    if soup.find(class_="paging"):
        if soup.find(class_="paging").findAll("a")[-2].text == "次へ":
            #次へボタンが存在する場合
            #次ページのurlを取得
            user_url = "https://www.buyma.com" + soup.find(class_="paging").findAll("a")[-2].text
        else:
            break
    else:
        break

#バイヤー一覧DataFrameの作成
items_df = pd.DataFrame(itemList)

#データフレームの並び変え
items_df = items_df.reindex(columns=['buyer_id', 'buyer_name', 'buyer_url', 'buyer_disp_num'])

#バイヤーの表示数の取得
buyer_id_size_list = items_df.groupby('buyer_id').size()

#バイヤーの表示数の設定
for idx, buyer_id_size in zip(buyer_id_size_list.index, buyer_id_size_list):
    items_df.loc[items_df['buyer_id'] == idx, ['buyer_disp_num']] = buyer_id_size
    
#重複の削除
items_df = items_df.drop_duplicates(subset='buyer_id')

#バイヤー実績一覧
itemDetailList = []

#バイヤー実績一覧を作成
i = 0
for detail_url, buyer_id in zip(items_df.buyer_url, items_df.buyer_id):
    if len(detail_url) != 0:
        #バイヤー実績HTMLを取得
        detail_res = get_html(detail_url, useragent)
        #HTMLの整形
        detail_sp = bs(detail_res.content, "html.parser")
        #バイヤー実績の取得
        detail_result = detail(detail_sp, buyer_id)
        #バイヤー実績一覧の設定
        itemDetailList.append(detail_result)
    else:
        continue

#バイヤー実績DataFrameを作成
detail_df = pd.DataFrame(itemDetailList)

#DataFrameのmerge
buyer_detail_df = pd.merge(items_df, detail_df, on='buyer_id', how='inner')
buyer_detail_df[buyer_detail_df["excellent_flg"] == 1].sort_values('diff', ascending=False)
ex_buyer_detail_df_sort = buyer_detail_df[buyer_detail_df["excellent_flg"] == 1].sort_values('diff', ascending=False)
sys.displayhook(ex_buyer_detail_df_sort.to_json())