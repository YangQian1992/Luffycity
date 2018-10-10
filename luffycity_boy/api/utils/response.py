# 创建一个响应数据的基类
class BaseResponse(object):
    def __init__(self):
        self.code = 1000
        self.data = ''
        self.error = ''

    @property
    def dict(self):
        return self.__dict__

if __name__ == '__main__':
    response = BaseResponse()
    response.data = '杨倩'
    print(response.dict)