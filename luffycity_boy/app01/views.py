from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.views import View
from app01 import models
import json

class Luffycity(View):
    def get(self,request):
        data_list = [{'name':'yangqian'},{"hobby":"wan"}]
        return JsonResponse(data_list,safe=False)

# 不用DRF也可做前后端分离接口
# class Luffycity(View):
#     def get(self,request):
#         book_obj_list = models.Book.objects.all()
#         res = []
#         for book_obj in book_obj_list:
#             res.append({
#                 "title":book_obj.title,
#                 "desc":book_obj.desc
#             })
#         return HttpResponse(json.dumps(res,ensure_ascii=False))


# 用DRF做前后端分离接口
# from rest_framework.views import APIView
# class Luffycity(APIView):
#     def get(self,request):
#         book_obj_list = models.Book.objects.all()
#         res = []
#         for book_obj in book_obj_list:
#             res.append({
#                 "title":book_obj.title,
#                 "desc":book_obj.desc
#             })
#         return HttpResponse(json.dumps(res,ensure_ascii=False))

# class Login(View):
#     def get(self,request):
#         return render(request,'login.html')
#
#     def post(self,request):
#         print(request.body)
#         print(request.body.decode('utf-8'),type(request.body.decode('utf-8')))
#         print(json.loads(request.body.decode('utf-8')),type(json.loads(request.body.decode('utf-8'))))
#         print(json.loads(request.body.decode('utf-8'))['name'])
#         print(type(request))
#         return HttpResponse('POST')

from rest_framework.views import APIView

from rest_framework.parsers import JSONParser,FormParser,MultiPartParser


class Login(APIView):
    parser_classes = [JSONParser]

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        print('执行post了！')
        print("request.body-->",request.body)
        '''
        执行post了！
        request.body--> b'name=yangqian&age=18'
       '''
        print("request.data-->",request.data) # 说明问题出在request.data上
        print("type(request)-->",type(request))
        return HttpResponse('OK')