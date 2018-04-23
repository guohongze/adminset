#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:lvhaidong
# datetime:2018/4/19 13:15
# software: PyCharm


class ResponseCode(object):
    """返回代码"""

    SUCCEED = 1  # 成功
    FAIL = 0
    ERROR = -1  # 失败


class ResponseMessage(object):
    """响应信息"""
    NOT_LOGIN = "Not Login!"
