from django.http import HttpResponse
import os
import json
import pandas as pd
from pandas import DataFrame
import re
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import base64
import matplotlib.pyplot as plt
#过滤字符
def translate(str):
    line = str.strip()#去除换行符或者空格
    p2 = re.compile('[^\u4e00-\u9fa5]')   # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(p2.split(line)).strip()
    zh = ",".join(zh.split())
    str = re.sub("[A-Za-z0-9!！，%\[\],。]", "", zh)
    return str
def word_cloud(csv_file, stopwords_path, pic_path):
    pic_name = "D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\魔童降世词云2.jpg"
    #path = os.path.abspath(os.curdir)
    csv_file = csv_file
    #csv_file = csv_file.replace('\\', '\\\\')
    d = pd.read_csv(csv_file, engine='python', encoding='utf-8')
    content = []
    print("数据读取完毕")
    for i in d['content']:
        try:
            i = translate(i)
        except AttributeError as e:
            continue
        else:
            content.append(i)
    comment_after_split = jieba.cut(str(content), cut_all=False)
    wl_space_split = " ".join(comment_after_split)
    backgroud_Image = plt.imread(pic_path)
    stopwords = STOPWORDS.copy()
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            stopwords.add(i.strip('\n'))
        f.close()
    print("分词结束")

    wc = WordCloud(width=1024, height=768, background_color='white',
                   font_path = 'D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\font.ttf',
                   stopwords=stopwords, max_font_size=400,
                   random_state=50)
    
 
    print(wc.generate_from_text(wl_space_split))
    #img_colors = ImageColorGenerator(backgroud_Image)
    #wc.recolor(color_func=img_colors)
    
    wc.to_file(pic_name)
    with open(pic_name,'rb') as f:
        clouddata = f.read()
        base64data = base64.b64encode(clouddata)
        return str(base64data)[2:]
    
def CloudAPI(request):
        moviename = json.loads(request.COOKIES.get("moviename"))
        base64data = word_cloud('D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\'+moviename+".csv",'D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\stopwords.txt',"D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\两只小狗.jpg")
        html_cloud = "<img src='data:image/png;base64,"+str(base64data)+"height='400' width='600'/>"
        return HttpResponse(html_cloud) 
