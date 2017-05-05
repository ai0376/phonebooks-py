#!/usr/bin/evn python 
# -*- coding:utf-8 -*-
__author__ = 'mjrao'
__time__ = '2017/4/27'


import web
#import utils
import json
import uuid

urls = (
    '/phonebooks','Phonebooks',
)

class Phonebooks:
    def POST(self):
        data = web.data();
        req_json = json.loads(data)
        op = req_json.get('op',0)
        '''
        1001: register
        1002: forgot password
        1003: login
        1004: logout
        1005: user add
        1006: user modify
        1007: user delete
        1008: search
        1009: get_all_user
        1010: get_all_tags
        '''
        if op == 1001:
            response={'ret':0,'msg':'success'}
            return json.dumps(response)
            pass
        elif op == 1002:
            response={'ret':0,'msg':'success'}
            return json.dumps(response)
            pass
        elif op == 1003:
            pass
        elif op == 1004:
            pass
        elif op == 1005:
            pass
        elif op == 1006:
            pass
        elif op == 1007:
            pass
        elif op == 1008:
            pass
        elif op == 1009:
            pass
        else:
            return json.dumps({'ret':-1,'msg':'no method'})
            pass


app = web.application(urls, globals())
application = app.wsgifunc()

if __name__=='__main__':

    #app.run()
    pass