from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests as req
import matplotlib.pyplot as plt
import re
import time
from datetime import date
from fake_useragent import UserAgent

#HTMLの取得
def get_html(url, useragent):
    headers = {"User-Agent":useragent}
    res = req.get(url,headers=headers)
    return res

#文字列から日付を作成
def create_date(string_date):
    string_date_list = string_date.split("/")
    format_date = date(int(string_date_list[0]), int(string_date_list[1]), int(string_date_list[2]))
    return format_date

#3ヶ月前の1日を取得
def create_three_months_ago():
    today = date.today()
    three_months_ago = ""
    if today.month <= 3:
        if today.month == 1:
            three_months_ago = date(today.year - 1, 10, 1)
        elif today.month == 2:
            three_months_ago = date(today.year - 1, 11, 1)
        else:
            three_months_ago = date(today.year - 1, 12, 1)
    else:
        three_months_ago = date(today.year, today.month - 3, 1)
    return three_months_ago

#商品一覧作成処理
def createItemList(items, itemList, res_listing_num, three_months_ago_date):
    #商品ID
    item_id = ""
    #商品url
    item_url = ""
    #注文数
    order_num = 0
    #注文日
    order_date = ""
    #商品を取得
    for item in items:
        #指名レスポンス出品判定
        if item.find(class_="buyeritem_info"):
            item_id = "指名レスポンス出品" + str(res_listing_num)
            item_url = ""
            order_num = re.sub("\\D", "", item.find(class_="buyeritemtable_info").findAll("p")[2].text)
            order_date = item.find(class_="buyeritemtable_info").findAll("p")[3].text.split("：")[1]
        else:
            item_id = item.find(class_="buyeritem_name").find("a").get("href").split("/")[2]
            item_url = "https://www.buyma.com/" + item.find(class_="buyeritem_name").find("a").get("href")
            order_num = re.sub("\\D", "", item.find(class_="buyeritemtable_info").findAll("p")[1].text)
            order_date = item.find(class_="buyeritemtable_info").findAll("p")[2].text.split("：")[1]
        
        #日付型に作り直し
        format_order_date = create_date(order_date)
        
        if format_order_date < three_months_ago_date:
            return 1
        
        #リストに追加
        itemList.append({
            #商品ID
            "item_id":item_id,
            #商品画像
            "picture":item.find(class_="buyeritemtable_img").find("img").get("src"),
            #商品名
            "item_name":item.find(class_="buyeritem_name").text.replace("\n", "").replace("\t", "").strip(),
            #出品日
            "listing_date":"20" + item.find(class_="buyeritemtable_img").find("img").get("src").split("/")[5],
            #注文数
            "order_num":order_num,
            #注文日
            "order_date":format_order_date,
            #商品url
            "item_url":item_url,
            #合計注文数
            "total_order_num":0,
        })
    return 0

def detail(detail_sp, item_id):
    #アクセス数
    access_count = 0
    #ほしいもの登録
    favorite_count = 0
    #レビュー口コミ数
    review_count = 0
    #お問い合わせ数
    contact_count = 0
    #ブランド
    brand_name = ""
    #カテゴリーリスト
    category_list = []
    #カテゴリー
    category = ""
    #シーズン
    season = ""
    #価格
    price = ""
    #買付地
    purchase_country = ""

    # 商品情報がある場合
    if detail_sp.find(id="s_brand"):
            
        access_count = int(re.sub("\\D", "", detail_sp.find(class_="ac_count").text))
        favorite_count = int(re.sub("\\D", "", detail_sp.find(class_="fav_count").text))
        review_count = int(detail_sp.find(id="tabmenu_revcnt").text)
        contact_count = int(detail_sp.find(id="tabmenu_inqcnt").text)
        brand_name = detail_sp.find(id="s_brand").findAll("a")[0].text.replace("\n", "").replace("\t", "").strip()
        #カテゴリーリスト作成
        for category_a in detail_sp.find(id="s_cate").findAll("a"):
            category_list.append(category_a.text)
        category = "|".join(category_list)
        #シーズン有無
        if detail_sp.find(id="s_season"):
            season = detail_sp.find(id="s_season").find(class_="ulinelink").text
        price = int(re.sub("\\D", "", detail_sp.find(class_="price_txt").text))
        purchase_country = detail_sp.find(id="s_buying_area").find("a").text
        
    return{
        #商品ID
        "item_id":item_id,
        #アクセス数
        "access_count":access_count,
        #ほしいもの登録
        "favorite_count":favorite_count,
        #レビュー口コミ数
        "review_count":review_count,
        #お問い合わせ数
        "contact_count":contact_count,
        #ブランド
        "brand_name":brand_name,
        #カテゴリー
        "category":category,
        #シーズン
        "season":season,
        #価格
        "price":price,
        #買付地
        "purchase_country":purchase_country,

    }

def detail_non_url(item_id):
    return{
        #商品ID
        "item_id":item_id,
        #アクセス数
        "access_count":0,
        #ほしいもの登録
        "favorite_count":0,
        #レビュー口コミ数
        "review_count":0,
        #お問い合わせ数
        "contact_count":0,
        #ブランド
        "brand_name":"",
        #カテゴリー
        "category":"",
        #シーズン
        "season":"",
        #価格
        "price":"",
        #買付地
        "purchase_country":"",
    }

def get_item_research_json(user_url):
    print("get_item_research_json：呼び出し成功")
    #UserAgentの作成
    ua = UserAgent()
    useragent = ua.random
    
    print("商品一覧作成開始")
    #商品一覧
    itemList = []
    #3ヶ月前の1日
    three_months_ago_date = create_three_months_ago()
    #ブレイクフラグ
    break_flg = 0
    #HTML取得
    res = get_html(user_url, useragent)
    #HTMLの整形
    soup = bs(res.content, "html.parser")
    #最大ページ数
    page_num = int(re.sub("\\D", "", soup.find(class_="paging fab-design-pg--t5").findAll("a")[-1].get("href").split("/")[-1]))
    #最大ページ数分繰り返し
    res_listing_num = 1
    for _ in range(page_num):
        #HTML取得
        res = get_html(user_url, useragent)
        #HTMLの整形
        soup = bs(res.content, "html.parser")
        #商品一覧情報を取得
        #data_line0
        items = soup.find(id="buyeritemtable").findAll(class_="data_line0")
        #data_line1
        items[len(items):len(items)] = soup.find(id="buyeritemtable").findAll(class_="data_line1")
        #商品一覧の作成
        break_flg = createItemList(items, itemList, res_listing_num, three_months_ago_date)
        if break_flg == 1:
            break
        res_listing_num = res_listing_num + 1
        if soup.find(class_="paging fab-design-pg--t5").findAll("a")[-2].find(class_="pagecount"):
            #次へボタンが存在する場合
            #次ページのurlを取得
            user_url = "https://www.buyma.com" + soup.find(class_="paging fab-design-pg--t5").findAll("a")[-2].get("href")
        else:
            if soup.find(class_="paging fab-design-pg--t5").findAll("a")[-1].find(class_="pagecount"):
                #次へボタンが存在する場合
                #次ページのurlを取得
                user_url = "https://www.buyma.com" + soup.find(class_="paging fab-design-pg--t5").findAll("a")[-1].get("href")
            else:
                break
    print("商品一覧作成終了")
    #商品一覧DataFrameの作成
    items_df = pd.DataFrame(itemList)
    #データフレームの並び変え
    items_df = items_df.reindex(columns=['item_id', 'picture', 'item_name', 'listing_date', 'order_num', 'order_date', 'item_url', 'total_order_num'])
    item_id_size_list = items_df.groupby('item_id').size()
    
    for idx, item_id_size in zip(item_id_size_list.index, item_id_size_list):
        items_df.loc[items_df['item_id'] == idx, ['total_order_num']] = item_id_size
    
    print("商品詳細作成開始")
    #商品詳細一覧
    itemDetailList = []
    
    #商品詳細一覧を作成
    i = 0
    for detail_url, item_id in zip(items_df.item_url, items_df.item_id):
        print(detail_url)
        if len(detail_url) != 0:
            #商品詳細HTMLを取得
            detail_res = get_html(detail_url, useragent)
            #HTMLの整形
            detail_sp = bs(detail_res.content, "html.parser")
            #商品詳細の取得
            detail_result = detail(detail_sp, item_id)
            #商品詳細一覧の設定
            itemDetailList.append(detail_result)
        else:
            detail_result = detail_non_url(item_id)
            itemDetailList.append(detail_result)
            
        if i % 1000 == 0:
            time.sleep(1)
        i = i + 1
    print("商品詳細作成終了")
    #商品詳細DataFrameを作成
    detail_df = pd.DataFrame(itemDetailList)
    #DataFrameのmerge
    items_detail_df = pd.merge(items_df, detail_df, left_index=True, right_index=True)
    items_detail_df_sort = items_detail_df.sort_values(['total_order_num', 'order_date'], ascending=[False, False])
    return items_detail_df_sort.to_json()