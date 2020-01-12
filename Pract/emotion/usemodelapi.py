import warnings

warnings.filterwarnings('ignore')
#加载词向量模型
from gensim.models import Word2Vec
# import os
# path1=os.path.abspath('.')
# print(path1)
word2vec_model = Word2Vec.load("./emotion/word2vec_model.w2v")
#加载逻辑回归模型
from sklearn.externals import joblib

logistic_model = joblib.load('./emotion/logistic.model')

#使用pandas的mean方法进行向量化
import time 
import numpy as np
import jieba
import pandas as pd
#加载分词字典
stopword_list = [k.strip() for k in open('./emotion/chineseStopWords.txt', encoding='utf8').readlines() if k.strip() != '']
def getVector_v2(cutWords, word2vec_model):
    vector_list = [word2vec_model[k] for k in cutWords if k in word2vec_model]
    vector_df = pd.DataFrame(vector_list)
    cutWord_vector = vector_df.mean(axis=0).values
    return cutWord_vector
#进行句子接收并使用模型
def useModelPredict(onesen):
    #分词
    cutWords = [k for k in jieba.cut(onesen) if k not in stopword_list]
    #print(cutWords)
    #向量化
    testsenvec = getVector_v2(cutWords,word2vec_model)
    #用于预测
    return logistic_model.predict([testsenvec])[0]

def sentypepre(sen):
    alltype = ['【优美语句】', '【伤感语句】', '【励志的话】', '【想念的句子】', '【爱情语句】']
    sen = sen
    type_pre = useModelPredict(sen)
    return alltype[type_pre]

##首先对文段进行分句处理
def splittext(textfilename):
    allsens= []
    text = ""
    with open (textfilename) as file:
        for f in file:
            text += f
        allsens = text.split("。")
        return allsens #返回由该文章中句子组成的列表
def splittext2(text):
    allsens= []
    allsens = text.split("。")
    return allsens #返回由该文章中句子组成的列表

def typetext(text):#接收分句之后的文句列表
    emotion = {
        "【优美语句】":0,
        "【伤感语句】":0,
        "【励志的话】":0,
        "【想念的句子】":0,
        "【爱情语句】":0,
        "【其他句子】":0
    }
    everytypesens = {
        "【优美语句】":[],
        "【伤感语句】":[],
        "【励志的话】":[],
        "【想念的句子】":[],
        "【爱情语句】":[],
        "【其他句子】":[]
    }
    for i in text:
        try:
            emotion[sentypepre(i)] = emotion[sentypepre(i)]+1
            everytypesens[sentypepre(i)].append(i)
        except Exception as e:
            print(e)
            emotion["【其他句子】"] = emotion["【其他句子】"]+1
    # 计算每个类别的占比
    sumpart = 0
    for i in emotion:
        sumpart = sumpart + emotion[i]
    #复制字典并赋值
    emotionpart = emotion
    for i in emotionpart:
        emotionpart[i] = str(int((int((emotionpart[i]/sumpart)*10000)/10000)*100)) + "%"
        
    return emotionpart,everytypesens #返回一个各种类别的占比字典

