#!/usr/bin/python
#_*_coding:utf-8 _*_



import urllib,urllib2
import json

def get_access_token():
    '''获取认证access_token值'''
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    # corpid: 每个企业都拥有唯一的corpid       corpsecret: 自建应用secret
    para = {'corpid':'xxxxxxxxxxxx','corpsecret':'xxxxxxxxxxxxxxxxxxx'}
    req = urllib2.Request(url + urllib.urlencode(para))
    ret = urllib2.urlopen(req)
    ret = json.loads(ret.read())
    return ret

token_id = get_access_token().get('access_token')
data = {
    "name" : "测试群",        # 群聊名 (选填）
    "owner" : "zhengli",      # 指定群主的id （选填）
    "userlist" : ["zhenglif", "cao"],    # 群成员id列表，至少2人（必填）
}

print token_id
def create_group(token_id,data):
    '''创建群会话
    :param token_id:  用于认证的access_token
    :param data:     提交创建群会话的数据
    '''
    headers = {'Content-Type': 'application/json'}
    url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=%s"%(token_id)
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()        # 返回结果：{"errcode":0,"errmsg":"ok","chatid":"16894972527282740677"}

create_group(token_id,data)
