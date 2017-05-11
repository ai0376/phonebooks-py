#!/usr/bin/evn python 
# -*- coding:utf-8 -*-
__author__ = 'mjrao'
__time__ = '2017/4/27'


import web
import utils
import json
import jwt
import re


urls = (
    '/phonebooks','Phonebooks',
)

dbinfo= utils.get_cfg('db.ini','mysql')
jwtinfo = utils.get_cfg('db.ini','jwt')

db = web.database(dbn='mysql', user=dbinfo.get('user',''),pw=dbinfo.get('password',''),db=dbinfo.get('database',''),host=dbinfo.get('host',''), port=int(dbinfo.get('port','')))

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
        1010: user query
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
                response = {'ret':ret[0],'msg':ret[1],'num':ret[2],'rid':ret[3],'token':ret[4]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return  json.dumps(response)

        elif op == 1004: #logout
            pass

        elif op == 1005: # user phone add
            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            if auth is None:
                web.ctx.status='401 Unauthorized'
                return
            else:
                auth = re.sub('^JWT ','' ,auth)
                print('auth:',auth)
                ret = self.__verify_token(auth)
                if ret[0] != 0:
                    response = {'ret':ret[0],'msg':ret[1]}
                    return json.dumps(response)
                else:
                    pass

            ret = self.user_phone_manage_add(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'rid':ret[2],'users':ret[3]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
            pass
        elif op == 1006: #user phone modify
            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            if auth is None:
                web.ctx.status='401 Unauthorized'
                return
            else:
                auth = re.sub('^JWT ','' ,auth)
                print('auth:',auth)
                ret = self.__verify_token(auth)
                if ret[0] != 0:
                    response = {'ret':ret[0],'msg':ret[1]}
                    return json.dumps(response)
                else:
                    pass
            ret = self.user_phone_manage_modify(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'uid':ret[2],'user':ret[3]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
            pass
        elif op == 1007: #user phone delete
            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            if auth is None:
                web.ctx.status='401 Unauthorized'
                return
            else:
                auth = re.sub('^JWT ','' ,auth)
                print('auth:',auth)
                ret = self.__verify_token(auth)
                if ret[0] != 0:
                    response = {'ret':ret[0],'msg':ret[1]}
                    return json.dumps(response)
                else:
                    pass
            ret =  self.user_phone_manage_delete(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}

            return json.dumps(response)
        elif op == 1008:
            pass
        elif op == 1009:
            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            if auth is None:
                web.ctx.status='401 Unauthorized'
                return
            else:
                auth = re.sub('^JWT ','' ,auth)
                print('auth:',auth)
                ret = self.__verify_token(auth)
                if ret[0] != 0:
                    response = {'ret':ret[0],'msg':ret[1]}
                    return json.dumps(response)
                else:
                    pass
            ret = self.user_phone_get_all(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'rid':ret[2],'users':ret[3]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
        elif op == 1010:
            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            if auth is None:
                web.ctx.status='401 Unauthorized'
                return
            else:
                auth = re.sub('^JWT ','' ,auth)
                print('auth:',auth)
                ret = self.__verify_token(auth)
                if ret[0] != 0:
                    response = {'ret':ret[0],'msg':ret[1]}
                    return json.dumps(response)
                else:
                    pass
            ret = self.user_query(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'users':ret[2]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
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
        access_token = self.__token_get(rid)
        return (0,'success', num, rid,access_token)

    def user_phone_manage_add(self, user_info):
        rid = user_info.get('rid','')
        users = user_info.get('users','')
        user_list = []
        for user in users:
            uname = user.get('name','')
            phone_list = []
            mail_list = []
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
                    phone_dic = dict(pid=pid,uid=uid,phone=p,intime=curtime)
                    phone_list.append(phone_dic)
                    pass
            mails = user.get('mails','')
            for mail in mails:
                mail_str = mail.get('mail','')
                if mail_str.strip() != '':
                    mid = utils.get_uuid()
                    db.insert(utils.DB_TABLE_MAIL,mid=mid,uid=uid,mail=mail_str,intime=curtime)
                    mail_dic = dict(mid=mid,uid=uid, mail=mail_str,intime=curtime)
                    mail_list.append(mail_dic)
            user_dic = dict(uid=uid,name=uname,phones=phone_list,mails=mail_list,intime=curtime)
            user_list.append(user_dic)
        return (0,'success',rid,user_list)
        pass

    def user_phone_manage_modify(self, user_info):
        uid = user_info.get('uid','')
        user = user_info.get('user','')
        uname = user.get('name','')
        phones = user.get('phones','')
        phones_list = []
        mails_list = []
        for phone in phones:
            pid = phone.get('pid','')
            phone = phone.get('phone','')
            if pid: #update
                vars = dict(pid=pid)
                intime_new = utils.get_cur_time()
                db.update(utils.DB_TABLE_PHONE, where="pid=$pid",phone=phone,intime=intime_new,vars=vars)
                phone_dic= dict(pid=pid,phone=phone,intime=intime_new)
                phones_list.append(phone_dic)
                pass
            else: #insert
                pid_new = utils.get_uuid()
                intime_new = utils.get_cur_time()
                db.insert(utils.DB_TABLE_PHONE,uid=uid,phone=phone,pid=pid_new,intime=intime_new)
                phone_dic= dict(pid=pid_new,phone=phone,intime=intime_new)
                phones_list.append(phone_dic)
                pass
        mails = user.get('mails','')
        for mail in mails:
            mid = mail.get('mid','')
            mail_str = mail.get('mail','')
            if mid:
                vars = dict(mid=mid)
                intime_new = utils.get_cur_time()
                db.update(utils.DB_TABLE_MAIL, where="mid=$mid",mail=mail_str ,intime=intime_new,vars=vars)
                mail_dic = dict(mid=mid,mail=mail_str,intime=intime_new)
                mails_list.append(mail_dic)
                pass
            else:
                mid_new = utils.get_uuid()
                intime_new = utils.get_cur_time()
                db.insert(utils.DB_TABLE_MAIL,uid=uid,mail=mail_str,mid=mid_new,intime=intime_new)
                mail_dic = dict(mid=mid_new,mail=mail_str,intime=intime_new)
                mails_list.append(mail_dic)
                pass
        user_dic = dict(uid=uid,name=uname,phones=phones_list,mails=mails_list)
        return (0,'success',uid,user_dic)
    def user_phone_manage_delete(self, user_info):
        users = user_info.get('users','')
        id_list = ''
        for user in users:
            uid = user.get('uid','')
            if uid.strip() != '':
                if id_list is '':
                    id_list = "'%s'" % uid
                else:
                    id_list = "%s,'%s'" %(id_list, uid)
        vars = dict(uids=id_list)
        db.delete(utils.DB_TABLE_MAIL ,where="uid in ($uids)",vars=vars)
        db.delete(utils.DB_TABLE_PHONE ,where="uid in ($uids)",vars=vars)
        db.delete(utils.DB_TABLE_USER ,where="uid in ($uids)",vars=vars)
        return (0,'success')

    def user_phone_get_all(self, user_info):
        rid = user_info.get('rid','')
        vars = dict(rid=rid)
        user_list = []
        '''
        tables = utils.DB_TABLE_USER +' u,'+utils.DB_TABLE_PHONE+' p,'+utils.DB_TABLE_MAIL+' m'
        results = db.select(tables , what='u.uid,u.name,p.phone,m.mail',where="u.rid=$rid AND u.uid=m.uid AND m.uid=p.uid",vars=vars)
        for user in results:
            user_dic =dict(uid=user['uid'],name=user['name'],phone=user['phone'],mail=)
        '''
        results = db.select(utils.DB_TABLE_USER, what='uid,name,intime', where="rid=$rid",vars=vars)
        for result in results:
            uid = result['uid']
            uname = result['name']
            uintime = result['intime']
            phone_list = []
            mail_list = []
            phone_results = db.select(utils.DB_TABLE_PHONE, what='phone,pid,intime',where="uid=$uid",vars=dict(uid=uid))
            for phone_result in phone_results:
                phone = phone_result['phone']
                pid = phone_result['pid']
                intime = phone_result['intime']
                phone_dic = dict(phone=phone,pid=pid,intime=intime)
                phone_list.append(phone_dic)
            mail_results = db.select(utils.DB_TABLE_MAIL, what='mail,mid,intime',where="uid=$uid",vars=dict(uid=uid))
            for mail_result in mail_results:
                mail = mail_result['mail']
                mid = mail_result['mid']
                intime = mail_result['intime']
                mail_dic = dict(mail=mail,mid=mid,intime=intime)
                mail_list.append(mail_dic)
            user_dic = dict(uid=uid,name=uname,phones=phone_list,mails=mail_list,intime=uintime)
            user_list.append(user_dic)
        return (0, 'success',rid,user_list)

    def user_query(self,user_info):
        users = user_info.get('users','')
        user_list=[]
        for user in users:
            uid = user.get('uid','')
            vars = dict(uid=uid)
            phone_list = []
            mail_list = []
            results = db.select(utils.DB_TABLE_USER, what='uid,name,intime', where="uid=$uid",vars=vars)
            for result in results:
                #id = result['uid']
                name = result['name']
                intime = result['intime']
            phone_results = db.select(utils.DB_TABLE_PHONE, what='phone,pid,intime',where="uid=$uid",vars=vars)
            for phone_result in phone_results:
                phone = phone_result['phone']
                pid = phone_result['pid']
                pintime = phone_result['intime']
                phone_dic = dict(phone=phone,pid=pid,intime=pintime)
                phone_list.append(phone_dic)

            mail_results = db.select(utils.DB_TABLE_MAIL, what='mail,mid,intime',where="uid=$uid",vars=vars)
            for mail_result in mail_results:
                mail = mail_result['mail']
                mid = mail_result['mid']
                mintime = mail_result['intime']
                mail_dic = dict(mid=mid,mail=mail,intime=mintime)
                mail_list.append(mail_dic)
            user_dic = dict(uid=uid,name=name,intime=intime,phones=phone_list,mails=mail_list)
            user_list.append(user_dic)
        return (0,'success',user_list)

    def __token_get(self,uid):
        iat = utils.get_iat()
        exp = iat + int(jwtinfo.get('expired','7200'))
        payload=dict(uid=uid,iat=iat,exp=exp)
        token = jwt.encode(payload,jwtinfo['key'], algorithm='HS256')
        return dict(type='JWT',access_token=token)
    def __verify_token(self,token):
        try:
            token_decode = jwt.decode(token,jwtinfo['key'],algorithm='HS256')
        except jwt.ExpiredSignatureError as e:
            return (-1,e.message)
        return (0,'success')

app = web.application(urls, globals())
application = app.wsgifunc()

'''
Deployment with gunicorn:

gunicorn -b ip:port main:application --access-logfile access.log --error-logfile error.log  -w 4 -D


'''
if __name__=='__main__':

    app.run()
    #print utils.get_md5('123456')
    pass