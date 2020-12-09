# Date:2020/12/2 22:55
# Author:Simon-syf

from weibopy import WeiboOauth2,WeiboClient
from collections import defaultdict
import pandas as pd
import time
import webbrowser                                                #.net控件
import re                                                        #正则表达式



#获取微博访问权限
client_key = '1682831498'
client_secret = '1d59150536c692bed24d59d46ae2b32d'
redirect_url = 'https://api.weibo.com/oauth2/default.html'       #授权回调页
auth = WeiboOauth2(client_key,client_secret,redirect_url)        #第三方应用请求用户授权
webbrowser.open_new(auth.authorize_url)                          #通过net控件自动启动web浏览器访问url
code = input('输入code:')                                         #获得服务器授权的授权码（用户授权）
token = auth.auth_access(code)                                   #第三方应用向服务器请求授权
print(token)                                                     #凭借token向资源服务器请求资源
#调用API接口获得数据
client = WeiboClient(token['access_token'])
print(client)


#表头定义
name = ['user_name','created_at','attitudes_count','comments']

#评论内容预处理
comment_text_list = []                                                                #评论内容
user_name = []                                                                        #用户ID
created_at = []                                                                       #评论时间
attitudes_count = []                                                                  #点赞数量

for i in range(1,50):
    result = client.get(suffix='comments/show.json',params={'id':4573338503217812,'count':100,'page':i})
    comments = result['comments']
    if not len(comments):
        break
    for comment in comments:
        # print(comment)
        text = re.sub('回复.*?:', '', str(comment['text']))
        comment_text_list.append(text)
        print(text)
        username = comment['user']['screen_name']
        user_name.append(username)
        print(username)
        createdat = comment['created_at']
        created_at.append(createdat)
        print(created_at)
        attitudescount = comment['status']['attitudes_count']
        attitudes_count.append(attitudescount)
        print(attitudescount)
    print('已抓取评论{}条'.format(len(comments)))
    time.sleep(5)

test = pd.DataFrame({'user_name':user_name,'created_at':created_at,'attitudes_count':attitudes_count,'comments':comment_text_list})
test.to_csv('f:/comment.csv',encoding='gb18030')




