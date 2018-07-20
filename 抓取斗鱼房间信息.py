# -*- coding: utf-8 -*-
"""
Created on Tue May  1 11:31:51 2018

@author: JoeCooper
"""

#抓取斗鱼直播平台的直播房间号及其观众人数，最后统计出某一时刻的总直播人数和总观众人数。

#coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import sys
import importlib
importlib.reload(sys)

class Douyu():
    
    def __init__(self):
        #使用selenium和PhantomJS模拟点击
        self.driver = webdriver.Firefox() #Firefox浏览器
        #self.driver = webdriver.PhantomJS(executable_path=r"D:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        self.num = 0
        self.count = 0

    def douyuSpider(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            soup = bs(self.driver.page_source, "xml")
            # 房间名, 返回列表
            names = soup.find_all("h3", {"class" : "ellipsis"})
            # 观众人数, 返回列表
            numbers = soup.find_all("span", {"class" :"dy-num fr"})

            for name, number in zip(names, numbers):
                print ( u"观众人数: " + number.get_text().strip()+u"\t房间名: " + name.get_text().strip()) #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格）
                self.num += 1
                count = number.get_text().strip()
                if count[-1]=="万":
                    countNum = float(count[:-1])*10000 #将几万的人数全部转换为全数字形式
                else:
                    countNum = float(count)
                self.count += countNum
            
            # 一直点击下一页
            self.driver.find_element_by_class_name("shark-pager-next").click()
            # 如果在页面源码里找到"下一页"为隐藏的标签，就退出循环
            if self.driver.page_source.find("shark-pager-disable-next") != -1:
                break    

        print ("\n当前网站直播人数:%s" % self.num)
        print ("当前网站观众人数:%s" % self.count)
            

if __name__ == "__main__":
    d = Douyu()
    d.douyuSpider()