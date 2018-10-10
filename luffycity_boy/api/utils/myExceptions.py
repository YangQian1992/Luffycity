from api.utils.response import BaseResponse


class PriceDoesNotExist(Exception):
    def __init__(self):
        self.error = "您所选的价格策略不存在！"


class CourseDoesNotExist(Exception):
    def __init__(self):
        self.error = "购物车中不存在该商品！"


class CommonException(Exception):
    def __init__(self,error,code=1100):
        self.error = error
        self.code = code