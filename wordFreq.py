# -*- coding: utf-8 -*-
"""
@file wordFreq.py
@version 0.0.1
@author Masayoshi Horita
@date 2022/12/03
@brief 形態素解析によって単語の頻出度を算出します。
@note 
"""

import MeCab
import collections
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
import glob
import csv
import pandas as pd
pydir = os.path.dirname(os.path.abspath(__file__))


## 頻出度を抽出したい列を指定します。
extract_row = "レビュー本文"

## 出力したい頻出単語の最大数を指定します。
output_count = 50


## csvを読み込んで、頻出後をプロットします。
def wordFrec():
    # select dataset path
    DATA_PATH = pydir + "/dataset/"
    all_Files = glob.glob('{}*.csv'.format(DATA_PATH))
    
    # load dataset from each file
    list = []
    for file in all_Files:
        infile = open(file, encoding="utf_8", errors='ignore')
        list.append(pd.read_csv(infile))
    df = pd.concat(list, sort=False)
    
    ## load data from marged csv
    # df.to_csv('merged_comment.csv', encoding='utf_8')
    
    # files = open('merged_comment.csv', encoding="utf-8", errors='ignore')
    # data = pd.read_csv(files)
    
    # extract message
    message = df[extract_row]
    
    messagelst = message.astype(str).tolist() # 文字列のリストに変換
    messagestr = ' '.join(messagelst)         # 空白文字で結合
    # print(messagestr) 
    
    tagger = MeCab.Tagger() 
    words=[]
    node = tagger.parseToNode(messagestr)
    # print(node)
    
    while node:
        tkn = node.feature.split(',')
        # print(tkn)
        # if tkn[0] in ["名詞", "動詞"]:
        if tkn[0] in ["名詞"]:
            words.append(node.surface)
        node = node.next
    
    
    # 単語のカウント
    c = collections.Counter(words)
    print(c.most_common(output_count))
    
    # 結果のグラフ化 
    sns.set(context="talk")
    # 結果の日本語化
    japanize_matplotlib.japanize()
    fig = plt.subplots(figsize=(8, 18))
     
    sns.countplot(y=words,order=[i[0] for i in c.most_common(output_count)])
    
    return c
    

## 単語のカウントを引数にとり、wordFreq.pyと同じディレクトリにcsv出力します。
def writeResulttoCSV(c):
    #CSV出力
    with open(pydir + "/wordFreq_result.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(c.most_common(output_count))


if __name__ == '__main__':
    collection = wordFrec()
    writeResulttoCSV(collection)
    
    


