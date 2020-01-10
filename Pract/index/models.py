from django.db import models

class Myusers(models.Model):
    username = models.CharField(max_length=20,verbose_name="用户名")
    pwd = models.CharField(max_length=20,verbose_name="密码")
    nickname = models.CharField(max_length=30,verbose_name="用户昵称",default="暂未设置昵称")
    presentence = models.TextField(max_length=140,verbose_name="个人宣言",default="暂未设置宣言")
    location = models.TextField(max_length=50,verbose_name="居住地址",default="暂未设置住址")
    university = models.CharField(max_length=50,verbose_name="就读学校",default="暂未设置学校")
    def __str__(self):
        return self.nickname
class Sen(models.Model):
    title = models.CharField(max_length=50,verbose_name="分享标题")
    content = models.TextField(max_length=500,verbose_name="分享内容")
    sharer = models.ForeignKey('Myusers',on_delete=models.CASCADE,verbose_name="分享人")
    sharetime = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
# Create your models here.
