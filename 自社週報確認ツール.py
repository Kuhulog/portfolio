#!/usr/bin/env python
# coding: utf-8
"""
自社のブログから各社員の週報を確認するツール
"""

import sys
import datetime
import os
import csv
import re
import MTV #自社URLにログインするためのモジュール
from selenium.webdriver.support import expected_conditions as EC

#今日の日付
today = datetime.datetime.today().strftime("%Y-%m-%d")

#csvファイルパス取得
#個人のアカウント情報パスワードや対象者のマイページにアクセスする際に使用する情報を記載
csv_path = os.getcwd() + r"\csv\週報.csv"
print(os.getcwd())

#配列宣言
Account = []
PW = []
Member = []
#アカウント、PW、メンバー情報を配列に格納
with open(csv_path, "r", encoding = "utf-8-sig") as f:
    reader = csv.reader(f)
    for row in reader:
        Account.append(row[0])
        PW.append(row[1])
        Member.append(row[2])

#ログイン＆ドライバー取得
mtv = MTV.MTV("社員の週報が掲載されている自社のURL", Account[1], PW[1])
driver = mtv.login()
blog_text = f'{today}.txt'
blog_folder = "ブログタイトル"
#テキスト格納用フォルダがなければ新規作成
if os.path.isdir(blog_folder):
    pass
else:
    os.mkdir(blog_folder)

os.chdir(blog_folder)

if os.path.isfile(blog_text):
    os.remove(blog_text)
    
for member in Member:
    #最初の行はカラム名なので無視する
    if re.compile("メンバー").search(member):
        continue
        
    driver.find_element_by_link_text("ユーザ検索").click()

    #ユーザ検索
    texts_searchName = driver.find_element_by_id('searchName')
    button_searchSubmit = driver.find_element_by_id('searchSubmit')
    texts_searchName.send_keys(member)
    button_searchSubmit.click()

    #ユーザマイページへ
    driver.find_element_by_link_text(member).click()

    #ブログタイトル取得
    i = 0
    h = 0
    
    while i < 5 :
        entryTitle = driver.find_element_by_xpath(f'//a[@id="{i}-blogTitle"]')
        #print(entryTitle.text + "👇")
        #print(entryTitle.get_attribute('href'))
            
        
        with open(f'{today}.txt', 'a', encoding='utf-8') as f:
            if h == 0:
                f.write(f'\n★{member}\n')

            Titlelist = [f'{entryTitle.text}👇 \n', f'{entryTitle.get_attribute("href")}\n']
            f.writelines(Titlelist)
            i += 1
            h = 1
            
#実行ファイルのパスに戻る
#連続して実行した際になぜか実行中のファイルパスにポインタがなかった
os.chdir('../')
#ドライバー閉じる
driver.close()
driver.quit()
