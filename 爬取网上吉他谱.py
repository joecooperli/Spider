
#coding: utf-8

#In[1]:

import requests as rq
import urllib
from lxml import html



def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print (path+u' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+u' 目录已存在')
        return False

# In[3]:
    
names = [u'好妹妹乐队',u'陈奕迅',u'毛不易',u'陈粒',u'李宗盛',u'房东的猫',u'郭顶']
for name in names:
    mkpath = r"C:\Users\JoeCooper\Desktop\练习\\"+name
    mkdir(mkpath)
    url = 'https://www.jitashe.org/search.php?mod=tab&srchtxt='+name+'&type=2&page='
    
    titles = []
    hrefs = []
    for page in range(30):
        search_page = rq.get(url+str(page))
        tree=html.fromstring(search_page.text)
        page_title = [title.text for title in tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')]
        if(len(page_title)== 0):break
        titles= titles+page_title
        hrefs=hrefs+[u'https://www.jitashe.org'+href for href in tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]//@href')]

    i = 0
    for title,jitar_url in zip(titles,hrefs):
        i = i+1 #用于区分同名
        jitar_page = rq.get(jitar_url)
        sub_tree = html.fromstring(jitar_page.text)
        sub_tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "imgtab", " " ))]//img//@src')
        try:
            sub_path = mkpath+'\\'+str(i)+title
            mkdir(sub_path)
        except Exception as a:
            sub_path = mkpath+'\\'+str(i)
            mkdir(mkpath+'\\'+str(i))

        jitar_page = rq.get(jitar_url)
        sub_tree = html.fromstring(jitar_page.text)
        imgs = sub_tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "imgtab", " " ))]//img//@src')
        x = 0
        for img in imgs:
            x = x+1
            try:
                urllib.request.urlretrieve(img, sub_path+'\\%s.jpg' % x)
            except Exception as b:
                print(b)


