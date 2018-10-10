from rest_framework.authentication import BaseAuthentication
from api.models import UserToken
from rest_framework.exceptions import AuthenticationFailed
from api.utils.response import BaseResponse


class Authentication(BaseAuthentication):

    def authenticate(self,request):
        # 获取前端发送过来的token值
        user_token = request.query_params.get('token')
        # 从数据库中查找token所对应的对象userToken_obj
        userToken_obj = UserToken.objects.filter(userToken=user_token).first()

        # 判断从前端获取到的token值是否在数据库中存在：
            # 若存在，则说明认证成功,放行并且返回user和userToken；
            # 否则，认证失败，不放行并且抛出认证失败异常。
        if userToken_obj:
            return userToken_obj.user , userToken_obj.userToken
        else:
            response = BaseResponse()
            response.code = 1001
            response.error = "认证失败"
            raise AuthenticationFailed(response.dict)   # 抛出异常
