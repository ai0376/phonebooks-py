#!/usr/bin/evn python 
# -*- coding:utf-8 -*-
__author__ = 'mjrao'
__time__ = '2017/4/27'


import web
import utils
import json


urls = (
    '/phonebooks','Phonebooks',
)

dbinfo= utils.get_cfg('db.ini','mysql')

db = web.database(dbn='mysql', user=dbinfo.get('user',''),pw=dbinfo.get('password',''),db=dbinfo.get('database',''),host=dbinfo.get('host',''), port=int(dbinfo.get('port','')))

print('db',db)

class Phonebooks:
    def POST(self):
        data = web.data()
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
            ret = self.user_register(req_json)

            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'rid':ret[2]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
            pass
        elif op == 1002:
            response = {'ret':0,'msg':'success'}
            return json.dumps(response)
            pass

        elif op == 1003: #user login
            ret = self.user_login(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'num':ret[2],'rid':ret[3]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return  json.dumps(response)

        elif op == 1004: #logout

            pass
        elif op == 1005: # user add
            ret = self.user_phone_manage_add(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
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

    def user_register(self,user_info):
        rphone = user_info.get('phone','')
        if not rphone.strip():
            return (-1, 'phone empty')
        var = dict(phone=rphone)
        results = db.select(utils.DB_TABLE_REG, vars = var, where="phone=$phone")
        rowcount = len(list(results))

        if not rowcount: #no person
            rid = utils.get_uuid()
            rintime = utils.get_cur_time()
            rname = user_info.get('name','')
            remail = user_info.get('email', rphone)
            rpassword = user_info.get('password','')
            rpassword = utils.get_md5(rpassword)

            ret = db.insert(utils.DB_TABLE_REG,rid=rid, phone=rphone,password=rpassword, name=rname, email=remail,intime=rintime)
            print('ret:',ret)
            if not ret:
                return (0, 'success', rid)
            else:
                return (-1, 'register error')
        else:
            return (-1, 'user had registed')

    def user_login(self, user_info):
        uphone = user_info.get('phone','')
        upassword = user_info.get('password','')
        upassword = utils.get_md5(upassword)

        if not uphone.strip():
            return (-1, 'login phone empty')
        var = dict(phone=uphone, password=upassword)
        results = db.select(utils.DB_TABLE_REG, what="rid",vars=var, where="phone=$phone and password=$password")
        rids = list(results)
        rowcount = len(rids)
        if not rowcount:
            return (-1,"phone or password error")
        rid = rids[0]['rid']
        results = db.select(utils.DB_TABLE_USER, what="uid",where="rid='%s'" % (rid))
        uids = list(results)
        num = len(uids)
        return (0,'success', num, rid)

    def user_phone_manage_add(self, user_info):
        rid = user_info.get('rid','')
        users = user_info.get('users','')
        for user in users:
            uname = user.get('name','')
            if uname.strip == '':
                return (-1, 'failed')
            phones = user.get('phones','')
            uid = utils.get_uuid()
            curtime = utils.get_cur_time()
            ret = db.insert(utils.DB_TABLE_USER,uid=uid,rid=rid,name=uname,intime=curtime)
            print('ret:',ret)

            for phone in phones:   #insert into t_phone
                p = phone.get('phone','')
                if p.strip() != '':
                    pid = utils.get_uuid()
                    db.insert(utils.DB_TABLE_PHONE,pid=pid,uid=uid,phone=p,intime=curtime)
                    pass
            tags = user.get('tags','')
            for tag in tags:
                tname = tag.get('name','')
                if tname.strip() != '':
                    tid = utils.get_uuid()
                    db.insert(utils.DB_TABLE_TAG,tid=tid,uid=uid,name=tname,intime=curtime)
            mails = user.get('mails','')
            for mail in mails:
                mail_str = mail.get('mail','')
                if mail_str.strip() != '':
                    mid = utils.get_uuid();
                    db.insert(utils.DB_TABLE_MAIL,mid=mid,uid=uid,mail=mail_str,intime=curtime)

        return (0,'success')
        pass

    def user_phone_maneage_modify(self, user_info):
        pass

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__=='__main__':

    app.run()
    #print utils.get_md5('123456')
    pass