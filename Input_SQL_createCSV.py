#!/usr/bin/env python
# coding:uft-8
#DBからCSVへ出力

import sqlite3
import os
import csv
import datetime
import time
import sys

print(sys.version)

start_time = time.time() #開始時刻

#お客様に提供しているサービス名を選択する
print('0 = Proxyサーバ \n' \
'1 = DNSサーバ \n'
'20 = FW'\
)

SERVICE = int(input("DBへ取り込むサービスを数字で指定してください \n")) 

if SERVICE == 0:
    SERVICE = 'Proxyサーバ'
elif SERVICE == 1:
    SERVICE = 'DNSサーバ'
elif SERVICE == 20:
    SERVICE = 'FW'

#上記選択したサービス内の各NW毎におけるサーバを選択する
if SERVICE == 'Proxyサーバ':
    print('0 = NW1のProxyサーバ \n' \
    '1 = NW2のProxyサーバ \n')
    HOST = int(input('DBへ取り込むサーバを数字で指定してください'))
    if HOST == 0:
        HOST = 'NW1のProxyサーバ'
    elif HOST == 1:
        HOST = 'NW2のProxyサーバ'
elif SERVICE == 'DNSサーバ':
    print('0 = NW1のDNSサーバ \n' \
    '1 = NW2のDNSサーバ \n')
    HOST = int(input('DBへ取り込むサーバを数字で指定してください'))
    if HOST == 0:
        HOST = 'NW1のDNSサーバ'
    elif HOST == 1:
        HOST = 'NW2のDNSサーバ'
elif SERVICE == 'FW':
    print('0 = NW1のFW \n' \
    '1 = NW2のFW \n')
    HOST = int(input('DBへ取り込むサーバを数字で指定してください'))
    if HOST == 0:
        HOST = 'NW1のFW'
    elif HOST == 1:
        HOST = 'NW2のFW'

#DBのパス
DB_PATH = '/mnt/data/work/log_data/{0}/{1}/【{0}】{1}.db'.format(SERVICE, HOST)
TABLE = HOST

#CSVの保存先と名前定義
dt_now = datetime.datetime.now()
dt_now = dt_now.strftime('%Y%m%d_%H%M') #ツール実行しCSV出力した時刻
SQL_Sentence = input('SQL文を入力してください \n')
CSV_Name = input('CSVの名前を入力してください \n') 
CSV_PATH = '/mnt/data/work/log_data/{0}/{1}/csv/【{0}_{2}】{1}_{3}.csv'.format(SERVICE, HOST, dt_now, CSV_Name)

def write_csv():
    #DBファイルがあれば接続、なければ終了
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
    else:
        print('DB nor found：' + DB_PATH)
        sys.exit()

    cur.execute(SQL_Sentence)

    #CSVファイル作成＆書き込みモードで開き、DBから取得してきた情報を格納
    with open(CSV_PATH, 'w') as f:
        writer = csv.writer(f)
        header = [i[0] for i in cur.description] #カラム名取得
        writer.writerow(header) #CSVのヘッダにカラム名を記載
        writer.writerows(cur.fetchall()) #各レコードが格納された二次元配列(タプル)(cur.fetchall())をCSVへ出力

    conn.close()

    #経過時間
    end_time = time.time() #終了時刻
    elapsed_time = end_time - start_time #処理時間

    elapsed_hour = elapsed_time // 3600 #時
    elapsed_minute = (elapsed_time % 3600) // 60 #分
    elapsed_second = (elapsed_time % 3600 % 60) #秒

    print('処理が完了しました' + '\n' + \
    '経過時間：' + str(elapsed_hour).zfill(2) + '時間' + str(elapsed_minute).zfill(2) + '分' + str(elapsed_second).zfill(2) + '秒')
    
if __name__ == '__main__':
    write_csv()