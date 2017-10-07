'''
Created on Oct 5, 2017

@author: adyant
'''
from django.views import generic
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import generics
from crudapplication.serializers import UserSerializer
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from django.conf import settings
import math, logging, os


rlogger = logging.getLogger(__name__)


class ListLogs(generic.ListView):
    template_name = 'logs.html'
    context_object_name = 'users'
    paginate_by = 3
    paginate_by_param = 2
    max_paginate_by = 10
    def get_queryset(self):
        users = User.objects.all()
        return users


class ListUserApi(generics.ListAPIView):
    serializer_class = UserSerializer
    template_name = 'home.html'
    context_object_name = 'users'
    paginate_by = 2
    paginate_by_param = 2
    max_paginate_by = 10
    def get_queryset(self, *args, **kwargs):
        users = User.objects.all()
        return users


class Getview(generics.RetrieveAPIView):
    seralizer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.values("id","username","first_name","last_name","email").get(pk=pk)
        except User.DoesNotExist:
            raise Http404 
  
    def get(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
            return Response(user,status=HTTP_200_OK)
        except:
            return Response({'status':'GET Failure'},status=HTTP_500_INTERNAL_SERVER_ERROR)
            

class Createview(generics.CreateAPIView):
    seralizer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            username = self.request.data.get('uname',None)
            fname = self.request.data.get('fname',None)
            lname = self.request.data.get('lname',None)
            email = self.request.data.get('email',None)
            thisuser = User()
            thisuser.username = username
            thisuser.first_name = fname
            thisuser.last_name = lname
            thisuser.email = email
            thisuser.save()
            return Response({'status':'POST Success'},status=HTTP_200_OK)
        except:
            return Response({'status':'POST Failure'},status=HTTP_500_INTERNAL_SERVER_ERROR)


class Updateview(generics.UpdateAPIView):
    seralizer_class = UserSerializer
    
    def update(self, request, *args, **kwargs):
        try:
            id = self.request.data.get('id',None)
            username = self.request.data.get('uname',None)
            fname = self.request.data.get('fname',None)
            lname = self.request.data.get('lname',None)
            email = self.request.data.get('email',None)
            thisuser = User.objects.get(pk=id)
            if username is not None and username != '':
                thisuser.username = username
            if fname is not None and fname != '':
                thisuser.first_name = fname
            if lname is not None and lname != '':
                thisuser.last_name = lname
            if email is not None and email != '':
                thisuser.email = email
            thisuser.save()
            return Response({'status':'PUT Success'},status=HTTP_200_OK)
        except:
            return Response({'status':'PUT Failed'},status=HTTP_500_INTERNAL_SERVER_ERROR)


class Deleteview(generics.DestroyAPIView):
    seralizer_class = UserSerializer

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'status':'DELETE Success'},status=HTTP_200_OK)
        except:
            return Response({'status':'DELETE Failure'},status=HTTP_500_INTERNAL_SERVER_ERROR)

class UserListview(generics.ListAPIView):
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    def get_queryset(self, *args, **kwargs):
        recs_in_page = settings.REST_FRAMEWORK.get('PAGINATE_BY',1)
        current_page = int(self.kwargs.get('page' ,'1'))
        end_rec = current_page * recs_in_page
        start_rec = end_rec - recs_in_page
        users = User.objects.all()[start_rec:end_rec]
        return users        

class LogListview(APIView):
    def get(self, request, page = '1', format=None):
        recs_in_page = settings.LOG_PAGE_SIZE
        current_page = int(page)
        end_rec = current_page * recs_in_page
        start_rec = end_rec - recs_in_page
        logpath = os.path.join(settings.BASE_DIR, 'logfile')
        fl = open(logpath,"r")
        i = 0
        log_list = []
        for line in fl:
            if i >= start_rec and i < end_rec:
                log_list.append([i,line])
            elif i >= end_rec:
                break
            i+=1
        fl.close()
        return Response({'log_list': log_list})

class LogCapture():
    _initial_http_body = None
       
    def process_request(self,request):
        if request.path.startswith('/api/'):
            if request.method=="GET" or request.method=="DELETE":#:
                rlogger.info(request.method + " " + request.path)
            elif request.META.get('CONTENT_TYPE') == 'application/x-www-form-urlencoded; charset=UTF-8' and (request.method in ("POST","PUT")):
                rlogger.info(request.method + " " + request.path)
                          
    def process_response(self, request, response):
        pass
        print(response.status_code)
# IF YOU WANT TO LOG IN RESPONSE
#         if request.path.startswith('/api/'):
#             if request.method=="GET" or request.method=="DELETE":#:
#                 rlogger.info(request.method + " " + request.path + request.status_code)
#             elif request.META.get('CONTENT_TYPE') == 'application/x-www-form-urlencoded; charset=UTF-8' and (request.method in ("POST","PUT")):
#                 rlogger.info(request.method + " " + request.path + " " + request.status_code)
        return response


class GetUsersCount(APIView):
    def get(self,request):
        page_size = settings.REST_FRAMEWORK.get('PAGINATE_BY',1)
        try:
            max_recs = float(User.objects.count())
            max_pages = int(math.ceil(max_recs / page_size));
            return Response({'max_pages':max_pages},status=HTTP_200_OK)
        except:
            return Response({'status':'GetUsersCount Failure'},status=HTTP_500_INTERNAL_SERVER_ERROR)

class GetLogsCount(APIView):
    def get(self,request):
        page_size = settings.LOG_PAGE_SIZE
        try:
            logpath = os.path.join(settings.BASE_DIR, 'logfile')
            fl = open(logpath,"r")
            max_lines = float(len(fl.readlines()))
            fl.close()
            max_pages = int(math.ceil(max_lines / page_size));
            return Response({'max_pages':max_pages},status=HTTP_200_OK)
        except:
            return Response({'status':'GetLogsCount Failure'},status=HTTP_500_INTERNAL_SERVER_ERROR)
