#!/usr/bin/env python
# coding:utf-8
#各サーバログのスクリプトファイルを呼び出す
import sys
sys.path.append("各SVログを格納するスクリプトファイルが格納されているフォルダ") #パスを通す
import FW_DB #FWログをDBに格納するスクリプトファイル
import glob
import os
import re
import sqlite3
import time

print(sys.version)

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

#DBのパスやテーブル名、対象ログが格納されているパスを指定
DB_PATH = '/mnt/data/work/log_data/{0}/{1}/【{0}】{1}.db'.format(SERVICE, HOST)
TABLE = HOST
TABLE_BK = TABLE + 'BK'
LOG_FOLDER_PATH = '/mnt/data/work/log_data/{0}/{1}'.format(SERVICE, HOST)

#正規表現でログ内の対象の要素だけをDBへ格納する
if SERVICE == 'Proxyサーバ' and HOST == 'NW1のProxyサーバ':
    REGEXP = 'NW1のProxyサーバ用の正規表現'
elif SERVICE == 'Proxyサーバ' and HOST == 'NW2のProxyサーバ':
    REGEXP = 'NW2のProxyサーバ用の正規表現'
elif SERVICE == 'DNSサーバ' and HOST == 'NW1のDNSサーバ':
    REGEXP = 'NW1のDNSサーバ用の正規表現'
elif SERVICE == 'DNSサーバ' and HOST == 'NW2のDNSサーバ':
    REGEXP = 'NW2のDNSサーバ用の正規表現'
elif SERVICE == 'FW':
    REGEXP = '(?P<Date>^[a-zA-Z]{3}\s*(?:[0-9]{1,2}))/s(?P<Time>\d{1,2}:\d{1,2}:\d{1,2}\s' \
    'proto=(?P<Protocol>[0-9]*)\s' \
    'src\szone=(?P<Src_Zone>[a-zA-Z0-9]*)\s' \
    'dst\szone=(?P<Dst_Zone>[a-zA-Z0-9]*)\s' \
    'src=(?P<Src_IP>(?:(?:\d{1,3}\.){3}\d{1,3})?)\s' \
    'dst=(?P<Dst_IP>(?:(?:\d{1,3}\.){3}\d{1,3})?)\s' \
    '(?:\s\S*=)?(?P<Src_Port>\d{1,5})?' \
    '(?:\s\S*=)?(?P<Dst_Port>\d{1,5})?\s'\
    '(?:.*ip=(?P<Src_Xlated_IP>(?:(?:\d{1,3}\.){3}\d{1,3})?)' \
    '(?:\s\S*=)?(?P<Src_Xlated_Port>\d{1,5})?\s\S\s' \
    '(?:.*ip=(?P<Dst_Xlated_IP>(?:(?:\d{1,3}\.){3}\d{1,3})?)' \
    '(?:\s\S*=)?(?P<Dst_Xlated_Port>\d{1,5})?\s\S\s' 

#コマンドラインから実行されたら下記の処理を行う
if __name__ == '__main__':
    if SERVICE == 'Proxyサーバ' and HOST == 'NW1のProxyサーバ':
        createDB = 'ProxyサーバをDBへ格納する用のclass' #インスタンス作成
        createDB.insert_db() #DBへ格納するためのメソッド
    elif SERVICE == 'Proxyサーバ' and HOST == 'NW2のProxyサーバ':
        createDB = 'ProxyサーバをDBへ格納する用のclass' #インスタンス作成
        createDB.insert_db() #DBへ格納するためのメソッド
    elif SERVICE == 'DNSサーバ' and HOST == 'NW1のDNSサーバ':
        createDB = 'DNSサーバをDBへ格納する用のclass' #インスタンス作成
        createDB.insert_db() #DBへ格納するためのメソッド
    elif SERVICE == 'DNSサーバ' and HOST == 'NW2のDNSサーバ':
        createDB = 'DNSサーバをDBへ格納する用のclass' #インスタンス作成
        createDB.insert_db() #DBへ格納するためのメソッド
    elif SERVICE == 'FW':
        createDB = 'FW_DB.FW_DB(HOST, DB_PATH, LOG_FOLDER_PATH, REGEXP)'
        createDB.insert_db()
