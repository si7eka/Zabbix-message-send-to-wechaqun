# 将Zabbix报警推送到企业微信群
[toc]



## 1. 概述
实现由企业微信客户端，群管理员管理报警信息接收人员名单，并支持及时讨论。

限制说明：
只允许企业自建应用调用，且应用的可见范围必须是根部门；
chatid所代表的群必须是该应用所创建；
每企业消息发送量不可超过2万人次/分，不可超过20万人次/小时（若群有100人，每发一次消息算100人次）；
每个成员在群中收到的应用消息不可超过200条/分，1万条/天，超过会被丢弃（接口不会报错）；


## 2. 申请企业
https://work.weixin.qq.com/

## 3. 企业微信API官方文档
API开发必读：https://work.weixin.qq.com/api/doc#90000/90135/90664  
消息推送概述：https://work.weixin.qq.com/api/doc#90000/90135/90235  
创建群聊会话：https://work.weixin.qq.com/api/doc#90000/90135/90245  
应用推送消息：https://work.weixin.qq.com/api/doc#90000/90135/90248  

## 4.部署脚本
将脚本上传到zabbix服务器上,并zabbix有执行权限   
```
/usr/lib/zabbix/alertscripts/    
```

#### 使用企业微信API创建群会话 
wechatqun-createqun.py
```python
#!/usr/bin/python
#_*_coding:utf-8 _*_



import urllib,urllib2
import json

def get_access_token():
    '''
    获取认证access_token值
    '''
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    # corpid: 每个企业都拥有唯一的corpid       corpsecret: 自建应用secret
    para = {'corpid':'xxxxxxxx','corpsecret':'0BkIw0wxxxxxxxxxxxxxxxxxxxxxxxxxxxt8'}
    req = urllib2.Request(url + urllib.urlencode(para))
    ret = urllib2.urlopen(req)
    ret = json.loads(ret.read())
    return ret

token_id = get_access_token().get('access_token')
data = {
    "name" : "测试群",        # 群聊名 (选填）
    "owner" : "zhengli",      # 指定群主的id （选填）
    "userlist" : ["zhengli", "caogang"],    # 群成员id列表，至少2人（必填）
}

print token_id
def create_group(token_id,data):
    '''
    创建群会话
    :param token_id:  用于认证的access_token
    :param data:     提交创建群会话的数据
    '''
    headers = {'Content-Type': 'application/json'}
    url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=%s"%(token_id)
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()        # 返回结果：{"errcode":0,"errmsg":"ok","chatid":"xxxxxxxxxxxx"}，chatid需要保留

create_group(token_id,data)
```
创建群
```
./wechatqun-createqun.py
```
  

#### 推送消息到群会话
wechatqun-sendalert.py
```python
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
    para = {'corpid':'wxxxxxxxxxxxx3','corpsecret':'0Bxxxxxxxxxxxxxxxxxxt8'}
    req = urllib2.Request(url + urllib.urlencode(para))
    ret = urllib2.urlopen(req)
    ret = json.loads(ret.read())
    return ret

token_id = get_access_token().get('access_token')
data = {
    "chatid": "xxxxxxxxxxxxx",      # 群聊id（必填），创建群返回信息中有记录
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

```  
测试发送消息
```
./wechatqun-sendalert.py 负责人 主题 内容   
```

## 5. zabbix 前端操作
#### 1). 报警媒体类型
![image](https://res.cloudinary.com/liz/image/upload/v1543481726/Zabbix-message-send-to-wechaqun/10.jpg)
更多请参考官方文档

#### 2). 用户
![image](https://res.cloudinary.com/liz/image/upload/v1543481726/Zabbix-message-send-to-wechaqun/20.jpg)
![image](https://res.cloudinary.com/liz/image/upload/v1543481726/Zabbix-message-send-to-wechaqun/30.jpg)


更多请参考官方文档
#### 3). 动作
![image](https://res.cloudinary.com/liz/image/upload/v1543481726/Zabbix-message-send-to-wechaqun/40.png)

如果接收信息的人比较复杂建议使用组来管理

故障报警消息参考
```
【故障报警！】服务器:{HOST.NAME}发生: {TRIGGER.NAME}故障!
告警主机:{HOST.NAME} {HOSTNAME1}
告警时间:{EVENT.DATE} {EVENT.TIME}
告警等级:{TRIGGER.SEVERITY}
告警信息:{HOST.NAME} {TRIGGER.NAME}
告警项目:{TRIGGER.KEY1}
问题详情:{ITEM.NAME}:{ITEM.VALUE}
当前状态:{TRIGGER.STATUS}:{ITEM.VALUE1}
事件ID:{EVENT.ID}
```
故障恢复消息参考
```
【故障恢复】服务器:{HOST.NAME}: {TRIGGER.NAME}已恢复!
告警主机:{HOST.NAME} {HOSTNAME1}
告警时间:{EVENT.DATE} {EVENT.TIME}
告警等级:{TRIGGER.SEVERITY}
告警信息:{HOST.NAME} {TRIGGER.NAME}
告警项目:{TRIGGER.KEY1}
问题详情:{ITEM.NAME}:{ITEM.VALUE}
当前状态:{TRIGGER.STATUS}:{ITEM.VALUE1}
事件ID:{EVENT.ID}
```

更多请参考官方文档

## 6. “报警信息”展示
手机端  
![image](https://res.cloudinary.com/liz/image/upload/v1543481727/Zabbix-message-send-to-wechaqun/50.jpg)

PC端   
![image](https://res.cloudinary.com/liz/image/upload/v1543482654/Zabbix-message-send-to-wechaqun/51.jpg)


## 7. 参考资料
资源下载
https://github.com/si7eka/Zabbix-message-send-to-wechaqun

配置动作
https://www.zabbix.com/documentation/3.4/zh/manual/config/notifications/action

配置用户
https://www.zabbix.com/documentation/3.4/zh/manual/config/users_and_usergroups/user

配置媒体类型
https://www.zabbix.com/documentation/3.4/zh/manual/config/notifications/media/script
