from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from .models import Myusers,Sen
import hashlib
from emotion.usemodelapi import * 

#定义一个将密码加密的函数
def md5(pwd,username):
    import random
    import hashlib
    salt = username
    m = hashlib.md5(bytes(pwd,encoding='utf-8'))
    m.update(bytes(salt,encoding='utf-8'))
    return m.hexdigest()
def index(request):
    username = str(request.COOKIES.get('username',''))
    namekey = request.COOKIES.get('_NAMEIDKEY','')
    print(namekey)
    print(type(namekey))
    if username:
        #依据用户名计算_NAMEIDKEY用于验证身份是否合法
        pwd = str(Myusers.objects.get(username=username).pwd)
        cacu_namekey = md5(pwd,username)
        authpass = (namekey==cacu_namekey) #验证通过标识符（计算字段等于获取到的字段则验证通过）
        if authpass:
            content = {
                "login":True
            }
        else:
            content = {
            "login":False
        }
    else:
        content = {
            "login":False
        }
    return render(request,"index.html",context=content)

def register(request):
    user = request.POST.get("username")
    password = str(request.POST.get("pwd"))
    #find the user exist?
    try:
        a=Myusers.object.get(username=user)
        if a:
            return HttpResponse("该用户名已经被使用")
    except Exception as e:
        print(e) 
    try:
        Myusers.objects.update_or_create(username = user,defaults={"pwd":password})
        return HttpResponse("注册成功,前往"+'<a href="../login/">登录</a>')
    except Exception as e:
        print(e)
        return HttpResponse("好气哦,注册失败")

def to_register(request):
    return render(request,"register.html")
def to_login(request):
    return render(request,"login.html")
def login(request):
    user = request.POST["username"]
    pwd = request.POST["pwd"]   
    print(user)
    try:
                    will_login = Myusers.objects.get(username=user)
                    print(will_login.pwd)
                    if will_login.pwd == pwd:
                        #succes to login then set cookie
                        response = HttpResponseRedirect("../../index")
                        response.set_cookie('username',user,3600)
                        response.set_cookie('_NAMEIDKEY',md5(pwd,user))
                        return response
                    else:
                        return HttpResponse("Wrong username or password,failed_to_login")
    except Exception as e:
                    print(e)
                    return HttpResponse("no_this_user")
        
def givesen(request):
    if request.method =="GET":
        #判断是否登录
        if request.COOKIES.get('username',''):

            return render(request,"givesen.html")
        else:
            return redirect("../../index/login/")
    if request.method =="POST":
        if request.COOKIES.get('username',''):
            username = request.COOKIES.get('username','')
            print(username)
            try:
                sharer = Myusers.objects.get(username=username)
            except Exception as e:
                print(e)
        #依据cookie获得用户名
        title = request.POST.get("title","标题未设置")
        content = request.POST.get("sencontent","no things")
        print(sharer)
        try:
            sentype = sentypepre(content)
        except:
            sentype = "其他"
        onesen = Sen(title=title,content=content,sharer=sharer,sentype=sentype)
        onesen.save()
        return HttpResponse("句子发表成功！")

def allsen(request):
    allsen = Sen.objects.all().order_by("sharetime")
    cont = {
        "allsen":allsen
    }
    return render(request,"seeallsen.html",context=cont)
# Create your views here.
