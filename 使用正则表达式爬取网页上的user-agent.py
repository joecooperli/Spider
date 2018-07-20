# -*- coding: utf-8 -*-
"""
Created on Mon May 14 09:32:09 2018

@author: JoeCooper
"""

#使用正则表达式爬取网页上的user-agent，添加了browser字段

import re
#from selenium import webdriver
import urllib.request
import pymysql

if __name__ == '__main__':
    #连接数据库，建表
    print('数据库连接中......')
    conn = pymysql.connect(host='localhost',user='root',passwd='123456',db='company',charset='utf8')
    print('已成功连接！')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS UAGENTS')
    #变量名不能出现短横线
    sql = """CREATE TABLE UAGENTS(
            ID INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            BROWSER CHAR(200),
            UAGENT VARCHAR(200))"""
    #BROWSER CHAR(30),
    cur.execute(sql)
    print('表格已成功建成！')
        
    url = 'https://blog.csdn.net/aeolus1019/article/details/41725273'
    
    #使用selenium的webdriver模拟浏览器登录
    """
    driver = webdriver.Chrome()
    driver.get(url)
    #html1 = driver.page_source
    html2 = driver.page_source  
    """
    
    #使用urllib.request发送访问网页请求
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')

    #print(html)
    
    #使用正则表达式定位查找p标签
    p1 = re.compile(r'<p class="cye-lm-tag" .*?>(.*?)</p>',re.S)
    strings1 = p1.findall(html)
    print(strings1[3])
    
    #使用正则表达式定位查找 > < 符号里面的的字符串（里面含有空列表）
    p3 = re.compile(r'>(.*?)<',re.S)
    uagents = p3.findall(str(strings1[3]))
    print(uagents)
    
    uagent_list = []
    #去掉空列表，重新将目标字符串添加到新的列表
    for uagent in uagents:
        if len(uagent) != 0:
            uagent_list.append(uagent)
    
    print(uagent_list)
    print(len(uagent_list))
     
    i = 0   
        
    """
    #出错，无法使用while True循环将数据插入数据库
    while True:

        #存入数据库操作
        insert_uagent = ('INSERT INTO UAGENTS(BROWSER,UAGENT)' 'VALUES(%s,%s)')
        
        a = uagent_list[j]
        b = uagent_list[j+1]
        
        insert_data = (a,b)
        cur.execute(insert_uagent,insert_data)
        
        #计算爬取的user-agent的数量
        i += 1
        
        j += 2
        
        if j == len(uagent_list) - 1:
            break     
    """ 
    
    #使用正则表达式定位查找带双引号的字符串
    for k in range(0,len(uagent_list),2):
         insert_uagent = ('INSERT INTO UAGENTS(BROWSER,UAGENT)' 'VALUES(%s,%s)')         
         #a = uagent_list[k]
         #b = uagent_list[k+1]
         insert_data = (uagent_list[k],uagent_list[k+1])
         cur.execute(insert_uagent,insert_data)
         
         #计算爬取的user-agent的数量
         i += 1
     
    print('共有%s条数据被爬取!'%i)
    
    #关闭游标和提交，不然无法保存新建或者修改的数据
    cur.close()
    conn.commit()
    
    print('数据已成功存入数据库！')