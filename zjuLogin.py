#! -*- encoding:utf-8 -*-
"""
author: wwtdsg
version: 1.5
type: script
2015.3.13
"""
import urllib2
import cookielib
import re
import urllib
import sys


class ZJULogin():
    def __init__(self):
        self.cj = ''
        self.opener = ''
        self.content = ''
        self.inputState = 0
        # set cookie
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def inputUserData(self):
        self.username = '********'  # raw_input('Input your username: ')
        self.password = '******'  # raw_input('Input your password: ')
        self.inputState = 1

    def login(self):
        self.inputUserData()

        # set form
        form_data = {'action': 'login',
                'username': self.username,
                'password': self.password,
                'ac_id': 3,
                'wbaredirect': '',
                'mac': 'undefined',
                'is_ldap': '1',
                'local_auth': '1'}
        url = 'https://net.zju.edu.cn/cgi-bin/srun_portal'

        login_operate = self.opener.open(url, data=urllib.urlencode(form_data))
        self.content = login_operate.read()
        self.state_check()

    def state_check(self):
        # 登录状态检查：登录或注销是否成功
        # 登录成功，返回欢迎语；登陆失败，返回失败信息
        string = 'login_ok'
        obj = re.compile(string)
        if re.findall(obj, self.content):
            print '登录成功：Welcome to ZJU WLAN!'
        else:
            print self.content
            sys.exit()

    def logout(self):
        # 注销用户需要访问同一个url并post两次，故构造两次报表
        # 并需要用第一次访问得到的sid值构造第二份报表
        if not self.inputState:
            self.inputUserData()
        url = 'http://net.zju.edu.cn/rad_online.php'
        form_data1 = {'action': 'logout',
                'username': self.username,
                'password': self.password}
        logout_operate1 = self.opener.open(url, data=urllib.urlencode(form_data1))
        # 获取sid的值以构造第二份报表
        string = '[0-9]{8,8}'
        obj = re.compile(string)
        self.content = logout_operate1.read()
        sid = re.findall(obj, self.content)
        if not sid:
            print "您尚未登录"
        else:
            form_data2 = {'action': 'dm',
                    'sid': sid[0]}
            self.opener.open(url, data=urllib.urlencode(form_data2))
            print "Logout successfully, goodbye!!"


def main():
    try:
        command = sys.argv[1]
    except IndexError, e:
        print e
        print "Input your command after *.py: 'login' or 'logout'."
        sys.exit(1)
    zju = ZJULogin()
    try:
        if command == 'login':
            zju.login()
        elif command == 'logout':
            zju.logout()
    except urllib2.URLError, e:
        print str(e.reason) + ': ' + "请检查网络连接"
        sys.exit(1)
    else:
        print 'Command input error, please check and try again!'
    print '----------------'

if __name__ == '__main__':
    main()
