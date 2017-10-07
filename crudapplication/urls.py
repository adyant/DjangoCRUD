"""crudapplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from crudapplication.views import Getview, Updateview, Createview, Deleteview, UserListview, GetUsersCount,\
    LogListview, GetLogsCount
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', views.home, name='home'),
    url(r'^$', TemplateView.as_view(template_name = "home.html")),
    url(r'^api/getUser/(?P<pk>[0-9]+)$', Getview.as_view()),
    url(r'^api/updateUser$', Updateview.as_view()),
    url(r'^api/createUser$', Createview.as_view()),
    url(r'^api/deleteUser/(?P<pk>[0-9]+)$', Deleteview.as_view()),
    url(r'^api/listUsers/(?P<page>[0-9]+)$', UserListview.as_view()),
    url(r'^api/getUsersCount', GetUsersCount.as_view()),
    url(r'^listLogs/(?P<page>[0-9]+)$', LogListview.as_view()),
    url(r'^getLogsCount', GetLogsCount.as_view()),
    url(r'^viewLogs', TemplateView.as_view(template_name = "logs.html")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
