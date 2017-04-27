#!/usr/bin/evn python 
# -*- coding:utf-8 -*-
__author__ = 'mjrao'
__time__ = '2017/4/27'


import web
#import utils
import json

urls = (
    '/phonebooks','Phonebooks',
)

class Phonebooks:
    def POST(self):
        data = web.data();
        req_json= json.loads(data)
        opid = req_json.get('opid',0)
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
    app.run()
    pass