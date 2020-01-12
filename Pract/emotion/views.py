from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .usemodelapi import sentypepre,typetext,splittext2
import json
def sentype(request):
    if request.method =="POST":
        sen = request.POST["sen"]
        type = sentypepre(sen)
        return HttpResponse(type)
    elif request.method =="GET":
        return render(request,"sentype.html")


def textemotion(request):
    if request.method =="GET":
        con = {
            "getresult":False,
        }
        return render(request,"texttype.html",context=con)
    if request.method =="POST":
        text = request.POST["text"]
        text_li = splittext2(text)
        type = typetext(text_li) #各个情感所占的比例，以及每一类的句子
        typepart = []       
        con = {
            "getresult":True,
            "typepart":type[0],
            "typesens":type[1]
        }
        htmlcon = creathtml(con)
        return HttpResponse(htmlcon)
def seetext(request):
    return render(request,"texttype.html")
def index(request):
    return render(request,"index-emotion.html")

def creathtml(con):
    htmlpart1 = '''<table width="1000px" border="1" style="position: fixed;left:60px;top: 180px;margin-top:50px">
        <tr>
          <th scope="row" width="80px"><p style="text-align: left">成分比例分析</p></th>
            <td width="200px" style="position: left"><strong>百分比</strong></td>
        </tr>'''
    htmlpart2 = '''
        <tr>
          <th scope="row" width="80px"><p style="text-align: left">{}</p></th>
          <td width="200px">
            <div class="progress">
                <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {};">
                    {}
                </div>
            </div>
          </td>
        </tr>'''
    #添加类别和占比
    htmlpart2_2 = ""
    emotion = con["typepart"]
    for i in emotion:
        htmlpart2_2 = htmlpart2_2+htmlpart2.format(i,emotion[i],emotion[i])
    htmlpart2_2 = htmlpart2_2+"</table>"
    return htmlpart1+htmlpart2_2

# 编写一个返回各种句子的视图

    
    

# Create your views here.
