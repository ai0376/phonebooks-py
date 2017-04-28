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
        req_json= json.loads(data)
        opid = req_json.get('opid',0)
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
        if opid == 1001:
            response={'ret':0,'msg':'success'}
            return json.dumps(response)
            pass
        elif opid == 1002:
            response={'ret':0,'msg':'success'}
            return json.dumps(response)
            pass
        else:
            return json.dumps({'ret':-1,'msg':'no method'})
            pass


app = web.application(urls, globals())
application = app.wsgifunc()

if __name__=='__main__':

    #app.run()
    pass