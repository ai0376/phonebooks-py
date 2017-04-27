#!/usr/bin/evn python 
# -*- coding:utf-8 -*-
__author__ = 'mjrao'
__time__ = '2017/4/27'


__all__=[
    "DB_TABLE_USER", "DB_TABLE_REG",
    "DB_TABLE_TAG", "DB_TABLE_MAIL",
    "DB_TABLE_PHONE", "get_cfg"
         ]

DB_TABLE_USER='t_mail'
DB_TABLE_REG='t_phone'
DB_TABLE_TAG='t_register'
DB_TABLE_MAIL='t_tag'
DB_TABLE_PHONE='t_user'

import os
import ConfigParser


def get_cfg(file):
    cfg_abspath = (os.path.join((os.path.split(os.path.realpath(__file__)))[0], file))
    config = ConfigParser.ConfigParser()
    config.read(cfg_abspath)
    host = config.get('mysql','host')
    port = config.get('mysql','port')
    database= config.get('mysql','database')
    user = config.get('mysql','user')
    password = config.get('mysql','password')

    ret_dic = dict(host=host,port=port, database=database, user=user,password=password)
    return ret_dic

