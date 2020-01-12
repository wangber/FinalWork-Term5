from rest_framework.views import APIView
import pandas as pd
import json
from index2.views import *
from pandas import DataFrame
from pyecharts import options as opts
from pyecharts.charts import Radar
import re
import jieba
fth = open('D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\pyecharts_citys_supported.txt', 'r', encoding='utf-8').read() # pyecharts支持城市列表
#过滤字符
def translate(str):
    line = str.strip()#去除换行符或者空格
    p2 = re.compile('[^\u4e00-\u9fa5]')   # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(p2.split(line)).strip()
    zh = ",".join(zh.split())
    str = re.sub("[A-Za-z0-9!！，%\[\],。]", "", zh)
    return str
def count_city(csv_file):
    #path = os.path.abspath(os.curdir)
    #csv_file = path+ "\\" + csv_file +".csv"
    #csv_file = csv_file.replace('\\', '\\\\')
    csv_file = csv_file
    d = pd.read_csv(csv_file, engine='python', encoding='utf-8')
    city = [translate(n) for n in d['city'].dropna()] # 清洗城市，将中文城市提取出来并删除标点符号等 
    # 这是从网上找的省份的名称，将其转换成列表的形式
    province = '湖南,湖北,广东,广西、河南、河北、山东、山西,江苏、浙江、江西、黑龙江、新疆,云南、贵州、福建、吉林、安徽,四川、西藏、宁夏、辽宁、青海、甘肃、陕西,内蒙古、台湾,海南'
    province = province.replace('、',',').split(',')
    rep_province = "|".join(province) # re.sub中城市替换的条件
    
    All_city = jieba.cut("".join(city)) # 分词，将省份和市级地名分开，当然有一些如吉林长春之类没有很好的分开，因此我们需要用re.sub（）来将之中的省份去除掉
    final_city= []
    for a_city in All_city:
        a_city_sub = re.sub(rep_province,"",a_city) # 对每一个单元使用sub方法，如果有省份的名称，就将他替换为“”（空）
        if a_city_sub == "": # 判断，如果为空，跳过
            continue
        elif a_city_sub in fth: # 因为所有的省份都被排除掉了，便可以直接判断城市在不在列表之中，如果在，final_city便增加
            final_city.append(a_city_sub)
        else: # 不在fth中的城市，跳过
            continue
            
    result = {}
    print("城市总数量为：",len(final_city))
    for i in set(final_city):#去除重复的城市
        result[i] = final_city.count(i)
    return result

#对城市数量绘制柱状图
def cityinfo(moviename):
    city = count_city("D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\"+moviename+".csv")
    cityname = []
    citynum = []
    for key in city:
        cityname.append(str(key))
        citynum.append(int(city[key]))
    return cityname,citynum
def getnumBar(cityname,citynum):
    c = (
    Bar()
    .add_xaxis(cityname)
    .add_yaxis("评论来源城市排行",citynum)
    .dump_options_with_quotes())
    return c

class ChartView_citynumbar(APIView):
    def get(self, request, *args, **kwargs):
        moviename = json.loads(request.COOKIES.get("moviename"))
        print("城市数量函数已经被访问")
        return JsonResponse(json.loads(getnumBar(cityinfo(moviename)[0],cityinfo(moviename)[1])))

