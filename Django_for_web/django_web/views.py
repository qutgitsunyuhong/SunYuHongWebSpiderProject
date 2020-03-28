from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from . import models
from django.core.urlresolvers import reverse
from django import forms
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
# from .models import jobList, java_job, learning
from datetime import datetime
from django.shortcuts import redirect
from .forms import   BookForm
from .models import bookList,VisitNumber,Userip,DayNumber
import re
import MySQLdb
import pandas as pd
import jieba
import csv
from collections import Counter

# 自定义的函数，不是视图
def change_info(request):  # 修改网站访问量和访问ip等信息
    # 每一次访问，网站总访问次数加一
    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()
    # print("执行到change_info内部")
    # 记录访问ip和每个ip的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']

        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
    # print(client_ip)

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:  # 判断是否存在该ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1
    uobj.save()

    # 增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()


def index(request):
    change_info(request)
    return render(request, 'mainpage/index.html')


def homepage(request):
    user = request.user if request.user.is_authenticated() else None
    change_info(request)
    books = bookList.objects.filter()
    books_novel = bookList.objects.filter(kind='小说')
    books_foreign = bookList.objects.filter(kind='外国文学')
    Count = VisitNumber.objects.filter(id=1)
    Count_num=Count[0].count
    print(Count_num)
    form = BookForm()
    return render(request, 'mainpage/index.html', locals())



def homepage_search(request):
    user = request.user if request.user.is_authenticated() else None
    form = BookForm()

    BookName = request.GET['BookName']
    BookType = request.GET['BookDec']
    if BookType == '所有':
        jobs = bookList.objects.filter(job_name__contains=BookName, isGetDetail=1)
    else:
        jobs = bookList.objects.filter(job_name__contains=BookName, job_dec=BookType)
    return render(request, 'mainpage/index.html', locals())

def signup(request):
    # if request.user.is_authenticated():  # 已经登陆过的账号
    #     return HttpResponseRedirect(reverse('homepage'))
    # state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':  # 输入密码为空
            state = 'empty'
        elif password != repeat_password:  # 输入的密码前后不一致
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')  # 获取用户名
            if User.objects.filter(username=username):
                state = 'user_exist'  # 用户名应存在
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                state = 'success'
        content = {
            'active_menu': 'homepage',
            'state': state,
            'user': None,
        }
        return render(request, 'mainpage/signup.html', content)
    else:
        return render(request, 'mainpage/signup.html')

def my_login(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse('homepage'))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
        content = {
            'active_menu': 'homepage',
            'state': state,###
            'user': None
        }
        return render(request, 'mainpage/login.html', content)
    else:
        return render(request, 'mainpage/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))

@login_required  # django内置用法，只有登录过的才可以浏览，如果还没有登录就进行访问，就先登录括号中的网址。
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'mainpage/set_password.html', content)
@login_required  # django内置用法，只有登录过的才可以浏览，如果还没有登录就进行访问，就先登录括号中的网址。
def myInfo(request):
    user = request.user
    return render(request, 'mainpage/info.html', locals())
def get_wordcloud():
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='xu332230', db='test2', charset='utf8')
    curs = conn.cursor()
    sql1 = '''select book_comm1,book_comm2,book_comm3,book_comm4,book_comm5 from  django_web_booklist'''  # sql语句
    curs.execute(sql1)
    row = curs.fetchall()  # 读取数据表内容，返回元祖类型,元祖的每个元素还是为元祖

    data = []
    for i in row:
        i = list(i)  # 将元祖的每个元素转换为列表
        new = str(i[0])  # 将列表转换为字符串
        xx = ' '.join(jieba.cut(new))  # 每一段字符串进行分词
        yy = xx.split(' ')
        for j in yy:
            data.append(j)  # 追加写入data列表，得到的数据格式为：a=['我 爱 学习 我 喜欢 北京']

    result = dict(Counter(data))
    my_result = dict(sorted(result.items(), key=lambda result: result[1], reverse=True))

    cnt = 0
    truly_result = {}
    for key, value in my_result.items():
        cnt = cnt + 1
        if cnt < 80:
            pass
        if cnt >= 80 and cnt < 180:
            truly_result[key] = value
        if cnt >= 180:
            break
    return truly_result

def homepage_search(request):
    user = request.user if request.user.is_authenticated() else None
    form = BookForm()

    BookName = request.GET['BookName']
    BookType = request.GET['BookType']
    if BookType == '所有':
        books = bookList.objects.filter(book_name=BookName)
    # books = bookList.objects.filter(id=26836970)
    else:
        books = bookList.objects.filter(book_name=BookName, kind=BookType)

    return render(request, 'mainpage/index.html', locals())
def book_detail(request, bookid):
    user = request.user if request.user.is_authenticated() else None
    form = BookForm()

    books_detail = bookList.objects.filter(id=bookid)
    book_detail_name= books_detail[0]
    # print("----------------------")
    # print(books_detail)
    # print("----------------------")
    total_book = bookList.objects.filter()

    # 0-6
    book_socre_0_6 = bookList.objects.filter(book_score__range =[0, 6])
    book_socre_0_6_num = book_socre_0_6.count()
    #6-7
    book_socre_6_7 = bookList.objects.filter(book_score__range =[6,7])
    book_socre_6_7_num=book_socre_6_7.count()
    #7-8
    book_socre_7_8 = bookList.objects.filter(book_score__range =[7, 8])
    book_socre_7_8_num = book_socre_7_8.count()
    #8-9
    book_socre_8_9 = bookList.objects.filter(book_score__range =[8, 9])
    book_socre_8_9_num = book_socre_8_9.count()
    #9-10
    book_socre_9_10 = bookList.objects.filter(book_score__range =[9, 10])
    book_socre_9_10_num = book_socre_9_10.count()
    print("----------------------")
    print(book_socre_0_6_num,book_socre_6_7_num,book_socre_7_8_num,book_socre_8_9_num,book_socre_9_10_num)
    print("----------------------")
    print(book_detail_name.book_stars5, book_detail_name.book_stars4, book_detail_name.book_stars3, book_detail_name.book_stars2, book_detail_name.book_stars1)
    content = {
            'user': 'user',
            'job_detail': 'job_detail',
            'job_name': 'job_name',
            'job_first_label': 'job_first_label',
            'job_second_label': 'job_second_label',
            'data': 'data',
            'learn': 'learn',
            'keyWord': 'keyWord',
            'workYear': 'workYear',
            'keyWordCloud': 'keyWordCloud',
            'education': 'education',
        }
    my_dict = get_wordcloud()
    print(my_dict)
    return render(request,'mainpage/job_detail.html',locals())

