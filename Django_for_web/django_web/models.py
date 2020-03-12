from django.db import models
from  django.utils import timezone
# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.CharField(max_length=60)
#     password = models.CharField(max_length=20)
#
#     def __str__(self):
#         print(self.username)
class bookList(models.Model):
    id = models.IntegerField(null=True,default=0)
    book_name = models.CharField(max_length=30)
    book_author = models.CharField(max_length=200)
    book_publisher = models.CharField(max_length=30, null=True)
    book_translator = models.CharField(max_length=30)
    book_page_num = models.CharField(max_length=30, null=True)
    book_score = models.FloatField(null=True)
    book_rating_num = models.IntegerField(null=True)
    book_comm1 = models.CharField(max_length=500)
    book_comm2 = models.CharField(max_length=500)
    book_comm3 = models.CharField(max_length=500)
    book_comm4 = models.CharField(max_length=500)
    book_comm5 = models.CharField(max_length=500)
    book_stars5 = models.FloatField(null=True)
    book_stars4 = models.FloatField(null=True)
    book_stars3 = models.FloatField(null=True)
    book_stars2 = models.FloatField(null=True)
    book_stars1 = models.FloatField(null=True)
    kind= models.CharField(max_length=16,default=0)
    No = models.IntegerField(default=0,primary_key=True)


    class META:
        ordering = ['book_name']
    def __str__(self):
        return self.book_name
class Userip(models.Model):
    ip = models.CharField(verbose_name='IP地址', max_length=30)  # ip地址
    count = models.IntegerField(verbose_name='访问次数', default=0)  # 该ip访问次数

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip
#网站总访问次数
class VisitNumber(models.Model):
    count=models.IntegerField(verbose_name='网站访问总次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.count)

#单日访问量统计
class DayNumber(models.Model):
    day=models.DateField(verbose_name='日期',default=timezone.now)
    count=models.IntegerField(verbose_name='网站访问次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.day)
