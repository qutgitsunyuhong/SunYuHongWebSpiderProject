"""untitled2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
# from django_web.views import index
from django_web import views
urlpatterns = [
    url('admin/', admin.site.urls),
    #path('index/',index),
    # path(r'register/',RegisterView.as_view(),name = 'register'),
    # path('registerView/', views.registerView),
    # path('register/', views.register),
    #path('login/', views.login),
    #path(r'^article/$', views.article),

    #path('regist/', views.regist),

    # path('accounts/login/', views.logout),

    url(r'^accounts/login/$', views.my_login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^accounts/set_password/$', views.set_password, name='set_password'),
    url(r'^accounts/info/$', views.myInfo, name='info'),
    url(r'^$', views.homepage, name='homepage'),  # 此行一定放在job_list行之上，否则出错
    url(r'^job/search/$', views.homepage_search, name='homepage_search'),
    url(r'^job_detail/(.+?)/$', views.book_detail, name='book_detail'),#http://127.0.0.1:8080/job_detail/1000856/
    # url(r'^job/(.+?)$', views.showjobs, name='job_list'),
    # url(r'^job_detail/(.+?)$', views.show_job_detail, name='job_detail'),

]
