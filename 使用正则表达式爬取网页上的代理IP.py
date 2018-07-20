# -*- coding: utf-8 -*-
"""
Created on Sun May 13 21:40:51 2018

@author: JoeCooper
"""

#使用正则表达式爬取网页上的代理IP,加上了“是否匿名”字段

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
    cur.execute('DROP TABLE IF EXISTS IP')
    sql = """CREATE TABLE IP(
            ID INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            IP_ADDRESS CHAR(20),
            PORT CHAR(10),
            SERVER_ADDRESS VARCHAR(10),
            ISANONYMOUS VARCHAR(2),
            TYPE CHAR(10),
            SURVIVAL_TIME VARCHAR(10),
            VERIFICATION_TIME VARCHAR(10)                       
            )"""
    #ISANONYMOUS VARCHAR(2),
    cur.execute(sql)
    print('表格已成功建成！')
        
    url = 'http://www.xicidaili.com/'
    
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
    
    #使用正则表达式定位查找tr标签，因tr标签里面内容不一致，需分两步来操作
    p1 = re.compile(r'<tr class="odd">(.*?)</tr>',re.S)
    strings1 = p1.findall(html)
    print(strings1)
    
    p2 = re.compile(r'<tr class="">(.*?)</tr>',re.S)
    strings2 = p2.findall(html)
    print(strings2)
    
    """
    #查找失败
    p = re.compile(r'<tr class="[a-z]*?">(.*?)</tr>',re.S)
    strings = p.findall(html)
    print(strings)
    """
    i = 0
    
    #使用正则表达式定位查找td标签
    #for string in strings:
    for string1,string2 in zip(strings1,strings2):
        
        p3 = re.compile(r'<td>(.*?)</td>',re.S)
        ips1 = p3.findall(string1)
        print(ips1[0]+':'+ips1[1])
        
        p4 = re.compile(r'<td>(.*?)</td>',re.S)        
        ips2 = p4.findall(string2)        
        print(ips2[0]+':'+ips2[1])
        
        p6 = re.compile(r'<td class="country">(.*?)</td>',re.S)
        ips4 = p6.findall(string1)
        values1 = ips4[1]
        print(ips4)
        print(values1)
        ips1.insert(3,values1)
        
        p6 = re.compile(r'<td class="country">(.*?)</td>',re.S)
        ips5 = p6.findall(string2)
        values2 = ips5[1]
        print(ips5)
        print(values2)
        ips2.insert(3,values2)
        #print(ips4[0]+':'+ips4[1])
        """
        p5 = re.compile(r'<td>(.*?)</td>',re.S)
        ips3 = p5.findall(string)
        print(ips3[0]+':'+ips3[1])
        """
        #计算爬取的IP地址的数量
        i += 2
        #i += 1
        print(ips1)
        print(ips2)
        #存入数据库操作
        insert_ip = ('INSERT INTO IP(IP_ADDRESS,PORT,SERVER_ADDRESS,ISANONYMOUS,TYPE,SURVIVAL_TIME,VERIFICATION_TIME)' 'VALUES(%s,%s,%s,%s,%s,%s,%s)')
        
        insert_data1 = (ips1[0],ips1[1],ips1[2],ips1[3],ips1[4],ips1[5],ips1[6])
        cur.execute(insert_ip,insert_data1)
        
        insert_data2 = (ips2[0],ips2[1],ips2[2],ips2[3],ips2[4],ips2[5],ips2[6])
        cur.execute(insert_ip,insert_data2)
        """
        insert_data3 = (ips3[0],ips3[1],ips3[2],ips3[3],ips3[4],ips3[5])
        cur.execute(insert_ip,insert_data3)
        """
        
    print('共有%s条数据被爬取!'%i)
    
    #关闭游标和提交，不然无法保存新建或者修改的数据
    cur.close()
    conn.commit()
    
    print('数据已成功存入数据库！')
        
        