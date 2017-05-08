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
        elif op == 1005: # user phone add
            ret = self.user_phone_manage_add(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}
            return json.dumps(response)
            pass
        elif op == 1006: #user phone modify
            pass
        elif op == 1007: #user phone delte
            ret =  self.user_phone_manage_delete(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1]}
            else:
                response = {'ret':ret[0],'msg':ret[1]}

            return json.dumps(response)
        elif op == 1008:
            pass
        elif op == 1009:
            ret = self.user_phone_get_all(req_json)
            if ret[0] is 0:
                response = {'ret':ret[0],'msg':ret[1],'rid':ret[2],'users':ret[3]}
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
            mails = user.get('mails','')
            for mail in mails:
                mail_str = mail.get('mail','')
                if mail_str.strip() != '':
                    mid = utils.get_uuid()
                    db.insert(utils.DB_TABLE_MAIL,mid=mid,uid=uid,mail=mail_str,intime=curtime)

        return (0,'success')
        pass

    def user_phone_manage_modify(self, user_info):
        pass
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
        results = db.select(utils.DB_TABLE_USER, what='uid,name', where="rid=$rid",vars=vars)
        for result in results:
            uid = result['uid']
            uname = result['name']
            phone_list = []
            mail_list = []
            phone_results = db.select(utils.DB_TABLE_PHONE, what='phone',where="uid=$uid",vars=dict(uid=uid))
            for phone_result in phone_results:
                phone = phone_result['phone']
                phone_dic = dict(phone=phone)
                phone_list.append(phone_dic)
            mail_results = db.select(utils.DB_TABLE_MAIL, what='mail',where="uid=$uid",vars=dict(uid=uid))
            for mail_result in mail_results:
                mail = mail_result['mail']
                mail_dic = dict(mail=mail)
                mail_list.append(mail_dic)
            user_dic = dict(uid=uid,name=uname,phones=phone_list,mails=mail_list)
            user_list.append(user_dic)
        return (0, 'success',rid,user_list)
        pass

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__=='__main__':

    app.run()
    #print utils.get_md5('123456')
    pass