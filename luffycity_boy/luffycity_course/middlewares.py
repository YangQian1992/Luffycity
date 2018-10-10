from django.utils.deprecation import MiddlewareMixin


class CrossDomainMiddleware(MiddlewareMixin):

    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            # 复杂请求（预检）
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Allow-Methods'] = 'POST,DELETE,PUT'
        return response
