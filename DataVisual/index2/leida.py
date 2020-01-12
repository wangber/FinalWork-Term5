from index2.views import *
import pandas as pd
from pandas import DataFrame
from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts import options as opts
from pyecharts.charts import Radar
def score_draw(csv_file):
    score, date, val, score_list = [], [], [], []
    result = {}
    #path = os.path.abspath(os.curdir)
    #csv_file = path + "\\" + csv_file + ".csv"
    #csv_file = csv_file.replace('\\', '\\\\')
    csv_file = csv_file
    d = pd.read_csv(csv_file, engine='python', encoding='utf-8')[['score', 'date']].dropna()  # 读取CSV转为dataframe格式，并丢弃评论为空的记录
    for indexs in d.index:  # 一种遍历df行的方法（下面还有第二种，iterrows）
        score_list.append(tuple(d.loc[indexs].values[:])) # 目前只找到转换为tuple然后统计相同元素个数的方法
    print("有效评分总数量为：",len(score_list), " 条")
    #print(score_list)
    #统计情感1
    emotion = {"力荐":0,
               "推荐":0,
               "还行":0,
               "较差":0,
               "很差":0
               }
    for i in score_list:
        #print(i)
        emotion[i[0]]+=1
    print("情绪统计1：",emotion)   
    for i in set(list(score_list)):
        result[i] = score_list.count(i)  # dict类型
    info = []
    for key in result:
        score= key[0]
        date = key[1]
        val = result[key]
        info.append([score, date, val])
    info_new = DataFrame(info)  # 将字典转换成为数据框
    info_new.columns = ['score', 'date', 'votes']
    info_new.sort_values('date', inplace=True)    # 按日期升序排列df，便于找最早date和最晚data，方便后面插值
    #print("first df", info_new)
    # 以下代码用于插入空缺的数据，每个日期的评分类型应该有5种，依次遍历判断是否存在，若不存在则往新的df中插入新数值
    mark = 0
    creat_df = pd.DataFrame(columns = ['score', 'date', 'votes']) # 创建空的dataframe
    for i in list(info_new['date']):
        location = info_new[(info_new.date==i)&(info_new.score=="力荐")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["力荐", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="推荐")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["推荐", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="还行")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["还行", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="较差")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["较差", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="很差")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["很差", i, 0]
            mark += 1
    info_new = info_new.append(creat_df.drop_duplicates(), ignore_index=True)
    score_list = []
    info_new.sort_values('date', inplace=True)    # 按日期升序排列df，便于找最早date和最晚data，方便后面插值
    #print(info_new)
    #print(type(info_new))
    print(len(info_new))
    for index, row in info_new.iterrows():   # 第二种遍历df的方法
        score_list.append([row['date'], row['votes'], row['score']])
        #print(row['date'], row['votes'], row['score'])
    #将情感统计的数目进行返回
    return emotion


def radar_base(v1):
    c = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="力荐", max_=100),
                opts.RadarIndicatorItem(name="推荐", max_=100),
                opts.RadarIndicatorItem(name="还行", max_=1000),
                opts.RadarIndicatorItem(name="较差", max_=100),
                opts.RadarIndicatorItem(name="很差", max_=100),
            ]
        )
        .add("评价情感", [v1])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="评论情感雷达图"))
        .dump_options_with_quotes()
    )
    return c

def filetoleidaimg(filename):
    all_mention = score_draw("D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\"+filename+".csv")
#绘制情感分析雷达图
    v1 =[]
    for key in all_mention:
        v1.append(all_mention[key])
    return v1

class ChartView_leida(APIView):
    def get(self, request, *args, **kwargs):
        moviename = json.loads(request.COOKIES.get("moviename"))
        print(type(moviename))
        print("雷达图视图被访问")
        return JsonResponse(json.loads(radar_base(filetoleidaimg(moviename))))

