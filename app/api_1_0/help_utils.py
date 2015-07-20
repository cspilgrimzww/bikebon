#coding=utf-8
__author__ = 'cspilgrim'
from random import randint
import requests,json

def generate_confirm_number():
    return str(randint(100000,1000000))

def request_confirm_number(phone_num,confirm_num=0):
    url="https://api.leancloud.cn/1.1/requestSmsCode"
    postdict ={
        "mobilePhoneNumber": phone_num,
        # "confirm_num": confirm_num
    }
    print('phone_num:'+phone_num)
    headers = {
        'Content-Type': "application/json",
        'X-AVOSCloud-Application-Id': "9o4sx4g9mxe07ub36jeh6vmyqf11fbfuc5jtdlu3z3r5x2k1",
        'X-AVOSCloud-Application-Key': "gltiwv78prih0tq90lpz1yjb04db2hhz9r58c4jqsb92ym96"
    }
    r = requests.post(url, data=json.dumps(postdict), headers=headers)
    return r.json()