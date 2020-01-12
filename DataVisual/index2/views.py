# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
# Create your views here.
import json
from random import randrange
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework.views import APIView
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Page, ThemeRiver
# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def bar_base() -> Bar:
    data = [
        ["2015/11/08", 10, "DQ"],
        ["2015/11/09", 15, "DQ"],
        ["2015/11/10", 35, "DQ"],
        ["2015/11/14", 7, "DQ"],
        ["2015/11/15", 2, "DQ"],
       
        
    ]
    c = (
        ThemeRiver()
        .add(
            ["DQ", "TY", "SS", "QG", "SY", "DD"],
            data,
            singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="10%"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="ThemeRiver-基本示例"))
        .dump_options_with_quotes()
    )
    
    return c


# class ChartView(APIView):
#     def get(self, request, *args, **kwargs):
#         print("基本测试视图")
#         return JsonResponse(json.loads(bar_base()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index2.html").read())

def index(request):
    request.encoding='utf-8'
    if request.method == "GET":
        return render(request,"index.html")
    if request.method =="POST":
        moviename = request.POST.get("movie")
        print("接收到表单数据：",moviename)
        
        #检查文件是否存在
        exist = 0
        try:
            f = open('D:\\Desktop\\DataVisual\\Presentation\\DataVisual\\index2\\OtherFile\\'+moviename+".csv")
            exist =1
        except Exception as e:
            print("请求的数据后台没有存档")
            exist = 0
        if exist == 1:
            response = redirect("../../index2/index2/")
            moviename = json.dumps(moviename)
            response.set_cookie('moviename',moviename)
            return response
        else :
            return render(request,"nodata.html")
# 从Cookie中获取电影名
# 根据电影名寻找数据文件
# 显示

######*************************
'''
依据名字获取id
传入进行爬取
保存文件后进行提示

'''
