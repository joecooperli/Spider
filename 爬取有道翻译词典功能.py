#模拟浏览器，词典翻译

import urllib.request 
import urllib.parse 
import json
import time

while True: #多次翻译
    content = input('请输入需要翻译的内容(输入"end"退出程序)：') #设置键入元素的操作
    if content == 'end':
        break
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule' #有道词典具有反爬虫机制，去掉_o即可


    #第一种方法：添加head，通过修改header来隐藏代码
    #head = {} #隐藏，躲过网页的反爬虫机制，浏览器通过检查链接里面的User-Agent来判断数据读取操作是代码（人为）还是浏览器
    #head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'     

    data = {}
    data['type'] = 'AUTO' 
    data['i'] = content #要翻译的内容
    data['doctype'] = 'json' #轻量级数据交换模式，把数据结构给封装起来
    data['xmlversion'] = '2.1' 
    data['keyfrom'] = 'fanyi.web' 
    data['ue'] = 'UTF-8' 
    data['typoResult'] = 'true' 
    data = urllib.parse.urlencode(data).encode('utf-8') #将unicode形式的文件编码（转化）成utf-8的形式


    #req = urllib.request.Request(url,data,head) #响应 （链接，数据）
    #第二种方法：先响应，再添加head参数
    req = urllib.request.Request(url,data)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')

    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8') #解码成unicode的形式

    target = json.loads(html) #loads 载入字符串（字典）
    print("翻译结果：%s" % (target['translateResult'][0][0]['tgt'])) #利用列表知识，提取翻译结果的元素
    #print(html)

    time.sleep(3) #延迟时间，再进入下一次循环
