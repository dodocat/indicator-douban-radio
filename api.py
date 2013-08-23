#coding=utf-8

import json
import uuid
import os
import getpass
import md5
import urllib
import urllib2


class Api:
    """
    Apid for douban FM
    """

    HOST_API = "api.douban.com"
    HOST_DOUBAN = "www.douban.com"

    APIKEY = "02f7751a55066bcb08e65f4eff134361"
    CLIENT = "s:mobile|y:android 4.2.2|f:618|m:Douban|d:294257752|e:samsung_gt-i9100g"

    CLIENT_ID = "02f7751a55066bcb08e65f4eff134361"
    CLIENT_SECRET = "63cf04ebd7b0ff3b"

    PKG_NAME = "com.douban.radio"
    PKG_VERSION_NAME = "3.0.2"
    PKG_VERSION_CODE = "101"
    SDK_INT = "14"
    DEV_MOD = " GT-I9100G samsung GT-I9100G"

    def __init__(self):
        self.uuid = self.gen_uuid()
        self.user_agent = self.gen_agent()
        self.token = None
    
    def do_login(self, username, password):
        data = self.token_by_password(username, password)
        print data
        self.token = json.loads(data, encoding = 'utf-8')
        

    def do_logout(self):
        self.token = None

    def gen_header(self):
        headers = {}
        headers['User-Agent'] = self.gen_agent()
        headers['Cookie2'] = '$Version=1'
        if self.token is not None:
            headers["Authorization"] = "Bearer " + self.token["access_token"]
        return headers

    def gen_agent(self):
        agent_builder = []
        agent_builder.append("api-client/")
        agent_builder.append('2.0')
        agent_builder.append(' ')
        agent_builder.append(self.PKG_NAME)

        agent_builder.append('/')
        agent_builder.append(self.PKG_VERSION_NAME)
        agent_builder.append("(")
        agent_builder.append(self.PKG_VERSION_CODE)
        agent_builder.append(")")

        agent_builder.append(" Android/")
        agent_builder.append(self.SDK_INT)
        agent_builder.append(" ")
        agent_builder.append(self.DEV_MOD)

        return ''.join(agent_builder)

    def gen_uuid(self):
        """ generate uuid for current user """
        mac = self._get_mac()
        os_user = getpass.getuser()
        str1 = "python_douban"
        str2 = "dodocat.github.com"
        str3 = 'papa'
        ustr = mac + os_user + str1 + str2 + str3

        m = md5.new()
        m.update(ustr)
        uuid = m.hexdigest() 
        uuid += "351ac62d" # 0:8 in md5 hex "blog.quanqi.org"
        return uuid

    def _get_mac(self):
        """ get mac address with uuid module """
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        return mac

    def get_channels(self):
        """ get channels """
        paras = self.create_paras()
        return self.open('get', self.HOST_API, '/v2/fm/app_channels', paras)

    def get_new_playlist(self, channel):
        paras = self.create_paras()
        paras['channel'] = str(channel)
        paras['type'] = 'n'
        paras['app_name'] = 'radio_android'
        paras['kbps'] = '64'
        paras['version'] = '618'
        paras['sid'] = ''
        paras['pb'] = '0'
        paras['pt'] = '0.0'
        paras['from'] = ''
        paras['formats'] = 'null'
        return self.open('get', self.HOST_API, '/v2/fm/playlist', paras)

    def get_lyric(self, ssid, sid):
        paras = self.create_paras()
        paras['ssid'] = ssid
        paras['sid'] = sid


    def token_by_password(self, username, password):
        paras = self.create_paras()
        paras['redirect_uri'] = "http://douban.fm"
        paras['grant_type'] = "password"
        paras['client_id'] = self.CLIENT_ID
        paras['client_secret'] = self.CLIENT_SECRET
        paras['username'] = username
        paras['password'] = password
        return self.open('post', self.HOST_DOUBAN, '/service/auth2/token', paras)

    def create_paras(self):
        paras = {'uuid' : self.gen_uuid(),
               'client' : self.CLIENT,
               "apikey" : self.APIKEY
        }
        return paras

    def open(self, method, host, api, paras):
        data = urllib.urlencode(paras)
        headers = self.gen_header()
        if method == 'get':
            url = "https://" + host + api + '?' + data
            req = urllib2.Request(url, None, headers)
        elif method == 'post':
            url = "https://" + host + api
            req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        return response.read()


