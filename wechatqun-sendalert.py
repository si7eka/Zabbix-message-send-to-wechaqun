#!/usr/bin/python
#_*_coding:utf-8 _*_

 
import urllib,urllib2
import json
import sys
import simplejson

reload(sys)
sys.setdefaultencoding('utf-8')


user = str(sys.argv[1])     #zabbix传过来的第一个参数{ALERT.SENDTO}，负责人
subject = str(sys.argv[2])  #zabbix传过来的第二个参数{ALERT.SUBJECT}，主题
content = str(sys.argv[3])  #zabbix传过来的第三个参数{ALERT.MESSAGE}，内容


def get_access_token():
    '''获取认证access_token值'''
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    # corpid: 每个企业都拥有唯一的corpid       corpsecret: 自建应用secret
    para = {'corpid':'xxxxxxxxxx','corpsecret':'xxxxxxxxxxxxxxxxxxxx'}
    req = urllib2.Request(url + urllib.urlencode(para))
    ret = urllib2.urlopen(req)
    ret = json.loads(ret.read())
    return ret

token_id = get_access_token().get('access_token')
data = {
    "chatid": "9787729367721683473",      # 群聊id（必填）
    "msgtype":"text",                       # 消息类型（必填）
    "text":{                                # 消息内容（必填）
        "content" :subject + '\n' + content  + '\n' + user
    },
    "safe":0                                # 表示是否是保密消息，0表示否，1表示是，默认0（选填）
}


print token_id
def send_msg_group(token_id,data):
    '''应用推送消息
    :param token_id:  用于认证的access_token
    :param data:     发送到群会话的数据
    '''
    headers = {'Content-Type': 'application/json'}
    url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=%s"%(token_id)
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()        # 返回结果：{"errcode":0,"errmsg":"ok"}


send_msg_group(token_id,data)


