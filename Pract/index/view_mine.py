from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from .models import Myusers,Sen
import random
def aboutme(request):
    if request.method == "GET":
        if request.COOKIES.get('username',''):
            user = request.COOKIES.get('username','')
        else:
            return redirect("../../index/")
        me = Myusers.objects.get(username=user)
        mysen = Sen.objects.filter(sharer = me)
        random_value = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','+','-','*','/',], random.randint(10,20)))
        con = {
            "me":me,
            "allmysen":mysen,
            "random_value":random_value
        }
        return render(request,"aboutme.html",context=con)
    if request.method == "POST":
        if request.COOKIES.get('username',''):
            user = request.COOKIES.get('username','')
        else:
            return redirect("../../index/")
        newme = Myusers.objects.get(username=user)
        newme.nickname = request.POST["nickname"]
        newme.presentence = request.POST["presentence"]
        newme.location = request.POST["location"]
        newme.university = request.POST["university"]
        newme.save()
        return HttpResponse("资料修改成功")
