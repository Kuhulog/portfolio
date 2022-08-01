#!/usr/bin/env python
# coding:uft-8
#FWログDB格納

import sqlite3
import glob
import os
import re
import time

class createDB:
    def __init__(self, HOST, DB_PATH, LOG_FOLDER_PATH, REGEXP):
        self.HOST = HOST
        self.TABLE = HOST
        self.TABLE_BK = self.TABLE + '_BK'
        self.DB_PATH = DB_PATH
        self.LOG_FOLDER_PATH = LOG_FOLDER_PATH
        self.REGEXP = REGEXP

    def __format_log(self, log_line):
        res = re.search(self.REGEXP, log_line)
        log_line_tuple = res.groups()
        return log_line_tuple

    def insert(self):
        #DBがなければ新規作成、あれば接続のみ
        conn = sqlite3.connect(self.DB_PATH)
        cur  = conn.cursor()
        #テーブルがなければ新規作成
        cur.execute('CREATE TABLE IF NOT EXISTS {0} (' \
        'Date TEXT,' \
        'Time TEXT, ' \
        'Src_IP TEXT' \
        'Dst_IP TEXT)'.format(self.TABLE))

        #フォルダを検索してファイルの中身を整形＆DB書き込み
        for path in glob.glob(self.LOG_FOLDER_PATH + '/*'):
            if os.path.isdir(path, 'r') or re.compile('.*\.db').search(path): #ディレクトリとDBは無視する
                continue
            else:
                with open(path, 'r') as f:
                    for line in f.read().split('\n'): #改行区切りで1行ずつ抜き取る
                        if line == '' : #空白行は無視する
                            pass
                        else:
                            formatted_line = self.__format_log(line)
                            #テーブルにカラムの値を入れる(VALUES)数を計算してcur.executeの第2引数に指定する配列の各データを格納する下地を作る
                            formatted_line_count = '?,' * len(formatted_line)
                            formatted_line_count = formatted_line_count.rstrip(',') #末尾「,」が不要なので削除
                            #?へ配列の各値を代入してくれる
                            cur.execute('INSERT INTO {0} VALUES' \
                            '({1})'.format(self.TABLE, formatted_line_count), formatted_line)

            conn.commit()
            conn.close()
