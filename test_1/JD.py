# -*- coding: UTF-8 -*-
import json
import csv
import sys

import requests
from bs4 import BeautifulSoup
import pymysql

class JD():
    """输入账号密码，登录京东，存储相应个人信息"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'https://www.jd.com/2017?t='
        }

    def get_login_data(self):
        # 模拟登录所需数据
        url = 'https://passport.jd.com/new/login.aspx'
        html = session.get(url, headers=self.headers).content
        bsObj = BeautifulSoup(html, 'lxml')
        display = bsObj.select('#o-authcode')[0].get('style')
        auth_code = ''
        if not display:
            print('需要的验证图片在源文件所在文件夹。')
            auth_code_url = bsObj.select('#JD_Verification1')[0].get('src2')
            auth_code = self.get_auth_img(auth_code_url)
        uuid = bsObj.select('#uuid')[0].get('value')
        eid = bsObj.select('#eid')[0].get('value')
        fp = bsObj.select('input[name="fp"]')[0].get('value')  # session id
        _t = bsObj.select('input[name="_t"]')[0].get('value')  # token
        login_type = bsObj.select('input[name="loginType"]')[0].get('value')
        pub_key = bsObj.select('input[name="pubKey"]')[0].get('value')
        sa_token = bsObj.select('input[name="sa_token"]')[0].get('value')

        data = {
            'uuid': uuid,
            'eid': eid,
            'fp': fp,
            '_t': _t,
            'loginType': login_type,
            'loginname': self.username,
            'nloginpwd': self.password,
            'chkRememberMe': True,
            'authcode': '',
            'pubKey': pub_key,
            'sa_token': sa_token,
            'authCode': auth_code
        }
        return data

    def get_auth_img(self, url):
        # 获得验证图片
        auth_code_url = 'http:' + url
        auth_img = session.get(auth_code_url, headers=self.headers)
        with open(sys.path[0] + '/auth.jpg', 'wb') as f:
            f.write(auth_img.content)
        code = input('请输入验证码：')
        return code

    def login(self):
        # 登录
        url = 'https://passport.jd.com/uc/loginService'
        data = self.get_login_data()
        headers = {
            'Referer': 'https://passport.jd.com/uc/login?ltype=logout',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        content = session.post(url, data=data, headers=headers).text
        result = json.loads(content[1:-1])
        return result

    def get_per_info(self):
        # 获取个人基本信息
        url = 'https://i.jd.com/user/info'
        html = session.get(url, headers=self.headers).content
        bsObj = BeautifulSoup(html, 'lxml')
        user_name = bsObj.find('strong').string
        loginname = bsObj.find('div',{'id':'aliasBefore'}).strong.string
        nickname = bsObj.select('#nickName')[0].get("value")
        #sex = bsObj.select.
        #birthday = bsObj.select
        hobbies = ['']
        hobuls = bsObj.findAll('ul',class_='hobul')
        for hobul in hobuls:
            if hobul.get('class') == "selected i-li":
                hobby = hobul.get_text()
                hobbies.append(hobby)
        email = bsObj.select('a[href=//safe.jd.com/validate/updateMail]')[0].find_previous_sibling().get_text().strip()

        per_info = {
            'username' : user_name,
            'loginname' : loginname,
            'nickname' : nickname,
            #'性别' : sex,
            #'生日' : birthday,
            'hobbies' : hobbies,
            'email' : email
        }
        return per_info

    def save_per_info(self):
        # 存储个人信息到MySQL数据库
        info = self.get_per_info()
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='hzzdaxia', charset='utf8')
        cursor = conn.cursor()
        sql = 'CREATE DATABASE IF NOT EXISTS perinfo charset="utf8"'
        cursor.execute(sql)
        sql = 'USE perinfo'
        print('个人信息准备存入数据库。')
        cursor.execute(sql)
        sql = """CREATE TABLE IF NOT EXISTS user(
            username VARCHAR(30) NOT NULL,
            loginname VARCHAR(30) NOT NULL,
            nickname VARCHAR(100) NOT NULL,
            hobbies VARCHAR(300), 
            email VARCHAR(50) 
        )"""
        cursor.execute(sql)
        sql = 'INSERT INTO user(username, loginname, nickname, hobbies, email) VALUES(%s, %s, %s, %s, %s)'
        args = [(info['username'], info['loginname'], info['nickname'], info['hobbies'], info['email'])]
        cursor.executemany(sql, args)
        conn.commit()
        print('信息存入成功，正在关闭数据库。')
        cursor.close()
        conn.close()
        print('数据库已关闭。')

session = requests.Session()
username = input('请输入您的京东账号：')
password = input('请输入您的京东密码：')
jd = JD(username, password)
result = jd.login()
if result.get('success'):
    print('登录成功')
else:
    print('登录失败')
save_info = jd.save_per_info()



