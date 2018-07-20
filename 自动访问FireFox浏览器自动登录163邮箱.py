# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 10:11:33 2018

@author: JoeCooper
"""

#自动访问FireFox浏览器自动登录163邮箱
#运行失败：Unable to locate element: [name="username"]

from selenium import webdriver    
from selenium.webdriver.common.keys import Keys
#import selenium.webdriver.support.ui as ui    
import time  
  
# Login 163 email  
driver = webdriver.Firefox()    
driver.get("http://mail.163.com/")

#wait = ui.WebDriverWait(driver,10)
#elem_user = wait.until(lambda driver:driver.find_element_by_name("username"))  
 
# 首先通过name定位用户名和密码，再调用方法clear()清除输入框默认内容 
elem_user = driver.find_element_by_name("username")  
elem_user.clear

#通过send_keys("**")输入正确的用户名和密码
#如果需要输入中文，防止编码错误使用send_keys(u"中文用户名")  
elem_user.send_keys("Joe_Cooper")    
elem_pwd = driver.find_element_by_name("password")  
elem_pwd.clear  
elem_pwd.send_keys("lixufa520")

#最后通过click()点击登录按钮或send_keys(Keys.RETURN)相当于回车登录，submit()提交表单    
elem_pwd.send_keys(Keys.RETURN)  
#driver.find_element_by_id("loginBtn").click()  
#driver.find_element_by_id("loginBtn").submit()  
time.sleep(5)    
assert "baidu" in driver.title    
driver.close()    
driver.quit()   