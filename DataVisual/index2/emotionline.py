import pandas as pd
from index2.views import *
from rest_framework.views import APIView
from pyecharts.charts import Line
import json
def takeThird(elem):
    return elem[2]
def takeOne(elem):
    return elem[0]
def emotiontime(csv_file):#通过该函数直接返回可供河流图使用的数据格式
    score, date, val, score_list = [], [], [], []
    result = {}
    #path = os.path.abspath(os.curdir)
    #csv_file = path + "\\" + csv_file + ".csv"
    #csv_file = csv_file.replace('\\', '\\\\')
    d = pd.read_csv(csv_file, engine='python', encoding='utf-8')[['score', 'date']].dropna()  # 读取CSV转为dataframe格式，并丢弃评论为空的记录
    for indexs in d.index:  # 一种遍历df行的方法（下面还有第二种，iterrows）
        score_list.append(tuple(d.loc[indexs].values[:])) # 目前只找到转换为tuple然后统计相同元素个数的方法
    print("有效评分总数量为：",len(score_list), " 条")
    #统计日期与评论出现的次数
    #转换为主键式列表
    mainkey = []
    for i in score_list:
        mainkey.append(i[0]+"#"+i[1])
    #统计主键数
    keynum = {}
    for i in mainkey:
        if i in keynum:
            keynum[i] +=1
        else:
            keynum[i] = 1
    #转换为河流图可用的数据格式-[[time,num,emotion]......]
    graphData = []
    for i in keynum :
        temp = []
        temp.append(i.split("#")[1].replace("-","/"))
        temp.append(keynum[i])
        temp.append(i.split("#")[0])
        graphData.append(temp)
        graphData.sort(key=takeThird)
    #进行时间排序
    emotion = ['力荐','很差','推荐','较差',"还行"]
    timesort = {
        '力荐':[],
        '很差':[],
        '推荐':[],
        '较差':[],
        "还行":[],
    }
    for i in graphData:
        timesort[i[2]].append(i)
    for i in timesort:
        timesort[i].sort(key=takeOne)
    graphData = []
    for i in timesort:
        graphData+=timesort[i]
    return graphData

## 寻找时间轴
def findalltime(emotiontime):
    alltime = []
    for i in emotiontime:
        if i[0] in alltime:
            continue
        else:
            alltime.append(i[0])
    alltime.sort()
    return alltime
def emotiontimekey(csv_file):#通过该函数返回统计之后每种情感的时间与数目
    score, date, val, score_list = [], [], [], []
    result = {}
    #path = os.path.abspath(os.curdir)
    #csv_file = path + "\\" + csv_file + ".csv"
    #csv_file = csv_file.replace('\\', '\\\\')
    d = pd.read_csv(csv_file, engine='python', encoding='utf-8')[['score', 'date']].dropna()  # 读取CSV转为dataframe格式，并丢弃评论为空的记录
    for indexs in d.index:  # 一种遍历df行的方法（下面还有第二种，iterrows）
        score_list.append(tuple(d.loc[indexs].values[:])) # 目前只找到转换为tuple然后统计相同元素个数的方法
    print("有效评分总数量为：",len(score_list), " 条")
    #统计日期与评论出现的次数
    #转换为主键式列表
    mainkey = []
    for i in score_list:
        mainkey.append(i[0]+"#"+i[1])
    #统计主键数
    keynum = {}
    for i in mainkey:
        if i in keynum:
            keynum[i] +=1
        else:
            keynum[i] = 1
    #转换为河流图可用的数据格式-[[time,num,emotion]......]
    graphData = []
    for i in keynum :
        temp = []
        temp.append(i.split("#")[1].replace("-","/"))
        temp.append(keynum[i])
        temp.append(i.split("#")[0])
        graphData.append(temp)
        graphData.sort(key=takeThird)
    #进行时间排序
    emotion = ['力荐','很差','推荐','较差',"还行"]
    timesort = {
        '力荐':[],
        '很差':[],
        '推荐':[],
        '较差':[],
        "还行":[],
    }
    for i in graphData:
        timesort[i[2]].append(i)
    return timesort
## 统计各类评价各个时间点的数量
def time_emotionnum(emotiontimekey,alltime):
    emotion = {
        '力荐':[],
        '很差':[],
        '推荐':[],
        '较差':[],
        "还行":[],
    }
    for i in emotiontimekey:#i对应某种情感
        temp = []
        for k in emotiontimekey[i]:#情感里每个日期
            temp.append(k[0])   
        for j in alltime: #j为日期轴内的日期
            if j in temp:
                emotion[i].append(emotiontimekey[i][temp.index(j)][1])
            else:
                emotion[i].append(0)
    return emotion

def givevalue(moviename):
    dataforriver=emotiontime("D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\"+moviename+".csv")
    alltime = findalltime(dataforriver)
    key = emotiontimekey("D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\"+moviename+".csv")
    Value = time_emotionnum(key,alltime)
    return alltime,Value
def line_smooth(x,y) -> Line:
    c = (
        Line()
        .add_xaxis(x)
        
        .add_yaxis('力荐', y['力荐'], is_smooth=True)
        .add_yaxis('推荐', y['推荐'], is_smooth=True)
        .add_yaxis("还行", y["还行"], is_smooth=True)
         .add_yaxis('较差',y['较差'], is_smooth=True)
        .add_yaxis('很差', y['很差'], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-smooth"))
        .dump_options_with_quotes()
    )
    
    return c
class ChartView_emotionline(APIView):
   def get(self, request, *args, **kwargs):
        moviename = json.loads(request.COOKIES.get("moviename"))
        print("情感时间线图被访问")
        return JsonResponse(json.loads(line_smooth(givevalue(moviename)[0],givevalue(moviename)[1])))
