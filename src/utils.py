#!/usr/bin/evn python 
# -*- coding:utf-8 -*-
__author__ = 'mjrao'
__time__ = '2017/4/27'


__all__=[
    "DB_TABLE_USER", "DB_TABLE_REG",
    "DB_TABLE_TAG", "DB_TABLE_MAIL",
    "DB_TABLE_PHONE", "get_cfg",
    "get_cur_time", "get_uuid",
    "get_md5"
         ]

DB_TABLE_USER='t_user'
DB_TABLE_REG='t_register'
DB_TABLE_MAIL='t_mail'
DB_TABLE_PHONE='t_phone'

import os
import ConfigParser
from time import strftime, localtime
from uuid import uuid1
from hashlib import md5

def get_cfg(file,section):
    cfg_abspath = (os.path.join((os.path.split(os.path.realpath(__file__)))[0], file))
    config = ConfigParser.ConfigParser()
    config.read(cfg_abspath)
    if section == 'mysql':
        host = config.get(section,'host')
        port = config.get(section,'port')
        database= config.get(section,'database')
        user = config.get(section,'user')
        password = config.get(section,'password')

        ret_dic = dict(host=host,port=port, database=database, user=user,password=password)
        return ret_dic
    elif section == 'memcached':
        host = config.get(section,'host')
        port = config.get(section,'port')
        user = config.get(section,'user')
        password = config.get(section,'password')
        expired = config.get(section,'expired')
        ret_dic = dict(host=host,port=port, user=user,password=password,expired=expired)
        return ret_dic
    elif section == 'jwt':
        key = config.get(section,'key')
        ret_dic = dict(key=key)
        return ret_dic

def get_cur_time():
    return strftime("%Y%m%d%H%M%S",localtime())

def get_uuid():
    return str(uuid1())

def get_md5(src):
    m_md5 = md5()
    m_md5.update(src)
    return m_md5.hexdigest()
