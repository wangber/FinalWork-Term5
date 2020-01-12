from django.shortcuts import render
from django.http import HttpResponse
def getcompage(request):
    return render(request,"getcomment.html")
