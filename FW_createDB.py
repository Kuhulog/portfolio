#!/usr/bin/env python
# coding:uft-8
#FWログDB格納

import sqlite3
import glob
import os
import re
import time
import gzip

class FW_createDB:
    def __init__(self, HOST, DB_PATH, LOG_FOLDER_PATH, REGEXP):
        self.HOST = HOST
        self.TABLE = HOST
        self.TABLE_BK = self.TABLE + '_BK'
        self.DB_PATH = DB_PATH
        self.LOG_FOLDER_PATH = LOG_FOLDER_PATH
        self.REGEXP = REGEXP

    def __format_log(self, log_line):
        res = re.search(self.REGEXP, log_line)
        log_line_Molding = res.groups()
        return log_line_Molding

    def insert_db(self):
        start_time = time.time() #開始時刻
        #DBがなければ新規作成、あれば接続のみ
        conn = sqlite3.connect(self.DB_PATH)
        cur  = conn.cursor()
        #テーブルがなければ新規作成
        cur.execute('CREATE TABLE IF NOT EXISTS {0} (' \
        'Date TEXT,' \
        'Time TEXT, ' \
        'Protocol INTEGER, ' \
        'Src_Zone TEXT' \
        'Dst_Zone TEXT' \
        'Src_IP TEXT' \
        'Dst_IP TEXT' \
        'Src_Port INTEGER' \
        'Dst_Port INTEGER' \
        'Src_Xlated_IP TEXT' \
        'Src_Xlated_Port INTEGER' \
        'Dst_Xlated_IP TEXT' \
        'Dst_Xlated_Port INTEGER)'.format(self.TABLE))

        #フォルダを検索してファイルの中身を整形＆DB書き込み
        for path in glob.glob(self.LOG_FOLDER_PATH + '/*'):
            if os.path.isdir(path, 'r') or re.compile('.*\.db').search(path): #ディレクトリとDBは無視する
                continue
            elif re.compile('.*(?:\.gz)$').search(path): #gzipの場合の処理
                with gzip.open(path, 'rb') as f: #gzipファイルなのでバイナリモードで開く
                    for line in f.read().split('\n'):
                        line = line.decode() #バイナリコードなのでデコードして文字列に変換
                        if line == '' : #空白行は無視する
                            pass
                        else:
                            #正規表現に当てはまらず抜き取れなかったら画面へ出力する
                            try:
                                formatted_line = self.__format_log(line)
                            except AttributeError:
                                print('抜き取れなかったログ \n')
                                print(line)
                                continue
                            formatted_line = list(formatted_line)
                            #月によって日付変換を行う
                            if re.compile('^Jan').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '1/', formatted_line[0])
                            elif re.compile('^Feb').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '2/', formatted_line[0])
                            elif re.compile('^Mar').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '3/', formatted_line[0])
                            elif re.compile('^Apr').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '4/', formatted_line[0])
                            elif re.compile('^May').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '5/', formatted_line[0])
                            elif re.compile('^Jun').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '6/', formatted_line[0])
                            elif re.compile('^Jul').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '7/', formatted_line[0])
                            elif re.compile('^Aug').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '8/', formatted_line[0])
                            elif re.compile('^Sep').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '9/', formatted_line[0])
                            elif re.compile('^Oct').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '10/', formatted_line[0])
                            elif re.compile('^Nov').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '11/', formatted_line[0])
                            elif re.compile('^Dec').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '12/', formatted_line[0])
                            #テーブルにカラムの値を入れる(VALUES)数を計算してcur.executeの第2引数に指定する配列の各データを格納する下地を作る
                            formatted_line_count = '?,' * len(formatted_line)
                            formatted_line_count = formatted_line_count.rstrip(',') #末尾「,」が不要なので削除
                            #?へ配列の各値を代入してくれる
                            cur.execute('INSERT INTO {0} VALUES' \
                            '({1})'.format(self.TABLE, formatted_line_count), formatted_line)

            else: #gzipではない場合の処理
                with open(path, 'r') as f:
                    for line in f.read().split('\n'):
                        if line == '' : #空白行は無視する
                            pass
                        else:
                            #正規表現に当てはまらず抜き取れなかったら画面へ出力する
                            try:
                                formatted_line = self.__format_log(line)
                            except AttributeError:
                                print('抜き取れなかったログ \n')
                                print(line)
                                continue
                            formatted_line = list(formatted_line)
                            #月によって日付変換を行う
                            if re.compile('^Jan').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '1/', formatted_line[0])
                            elif re.compile('^Feb').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '2/', formatted_line[0])
                            elif re.compile('^Mar').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '3/', formatted_line[0])
                            elif re.compile('^Apr').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '4/', formatted_line[0])
                            elif re.compile('^May').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '5/', formatted_line[0])
                            elif re.compile('^Jun').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '6/', formatted_line[0])
                            elif re.compile('^Jul').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '7/', formatted_line[0])
                            elif re.compile('^Aug').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '8/', formatted_line[0])
                            elif re.compile('^Sep').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '9/', formatted_line[0])
                            elif re.compile('^Oct').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '10/', formatted_line[0])
                            elif re.compile('^Nov').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '11/', formatted_line[0])
                            elif re.compile('^Dec').search(formatted_line[0]):
                                formatted_line[0] = re.sub('\S{3}\s{1,2}', '12/', formatted_line[0])
                            #テーブルにカラムの値を入れる(VALUES)数を計算してcur.executeの第2引数に指定する配列の各データを格納する下地を作る
                            formatted_line_count = '?,' * len(formatted_line)
                            formatted_line_count = formatted_line_count.rstrip(',') #末尾「,」が不要なので削除
                            #?へ配列の各値を代入してくれる
                            cur.execute('INSERT INTO {0} VALUES' \
                            '({1})'.format(self.TABLE, formatted_line_count), formatted_line)

            #重複削除の準備
            cur.execute('SELECT * FROM {0}'.format(self.TABLE))
            LIST = []
            for desc in cur.description:
                LIST.append(desc[0]) #カラム名をリストに格納
            
            LIST_Iter = iter(LIST)

            LIST_count = None
            LIST_count = ''
            LIST_Index = 0
            #LIST_countに{0[0]}, {0[1]},{0[2]}, {0[3]}・・・の文字列を格納し、format(LIST)からカラム名を取り出せるようにする
            try:
                while next(LIST_Iter): #{0[0]}, {0[1]}・・・とStopIterationエラーが出るまで繰り返す
                    LIST_count += '{{0[{0}]}},'.format(LIST_Index) #波括弧{}は{{}}でエスケープ出来る
                    LIST_Index += 1
            except StopIteration:
                pass
            LIST_count = LIST_count.rstrip(',') #末尾「,」が不要のため削除

            #重複削除(各レコードをグループ化し重複削除した新規テーブルを作成)
            #CREATE TABLE テーブル名+BK AS SELECT * FROM テーブル名 GROUP BY {0[0]}, {0[1]},{0[2]}, {0[3]}・・・となる
            NewTableSql = 'CREATE TABLE {1} AS SELECT * FROM {0} GROUP BY {2}'.format(self.TABLE, self.TABLE_BK, LIST_count)
            #CREATE TABLE テーブル名+BK AS SELECT * FROM テーブル名 GROUP BY {0[0]}, {0[1]},{0[2]}, {0[3]}・・・.format(LIST)
            #LIST(各カラム名が格納されているリスト)を使用し、テーブルの全カラムを対象にグループ化事によって重複削除を行う
            cur.execute(NewTableSql.format(LIST))
            #旧テーブル削除
            cur.execute('DROP TABLE {0}'.format(self.TABLE))
            #新テーブル名(テーブル名+BK)を旧テーブル名(テーブル名)に変更する
            cur.execute('ALTER TABLE {0} RENAME TO {1}'.format(self.TABLE_BK, self.TABLE))

            conn.commit()
            conn.close()
            
            #経過時間
            end_time = time.time() #終了時刻
            elapsed_time = end_time - start_time #処理時間

            elapsed_hour = elapsed_time // 3600 #時
            elapsed_minute = (elapsed_time % 3600) // 60 #分
            elapsed_second = (elapsed_time % 3600 % 60) #秒

            print('処理が完了しました' + '\n' + \
            '経過時間：' + str(elapsed_hour).zfill(2) + '時間' + str(elapsed_minute).zfill(2) + '分' + str(elapsed_second).zfill(2) + '秒')
            #コマンドライン上で当ファイルを実行しないようにする
            if __name__ == '__main__':
                print('createDB.pyから実行してください')
