from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.response import BaseResponse
from api.models import User,UserToken

import time
import hashlib

import rest_framework
def get_token(user):
    # 获取一个字符串类型的时间戳时间
    str_ctime = str(time.time())
    # 生成一个加盐的hashlib对象
    md5 = hashlib.md5(bytes(user,encoding='utf-8'))
    # 给随机生成的字符串加密
    md5.update(bytes(str_ctime,encoding='utf-8'))
    # 返回加密后的字节型数据
    return md5.hexdigest()


class LoginView(APIView):
    '''登录视图是校验逻辑接口，不需要用视图类组件'''
    def post(self,request):
        response = BaseResponse()
        try:
            # 获取前端通过POST请求发送过来的数据
            user = request.data.get('username')
            pwd = request.data.get('password')
            # 查找数据库中是否有此用户
            user_obj = User.objects.filter(username=user,password=pwd).first()
            if user_obj:
                # 如果数据库中有此用户，就做以下内容：
                    # 1.将此用户名返回给前端
                response.user = user_obj.username
                    # 2.将随机生成一个字符串作为Token值返回给前端
                token = get_token(user)
                response.user_token = token
                    # 将随机生成的token保存在数据库中
                UserToken.objects.update_or_create(user=user_obj,defaults={'userToken':token})
            else:
                response.code = 1001
                response.error = '用户名或者密码错误'
        except Exception as e:
            response.code = 1002
            response.error = str(e)
        return Response(response.dict)