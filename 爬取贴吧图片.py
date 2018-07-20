#使用打开网页函数、获取网页照片函数、正则表达式来爬取图片
#此网页有多张图片

#导入模块
import urllib.request #获取网页
import re #正则表达式
import os #新建文件夹

#创建打开网页函数
def url_open(url):
    #生成request对象
    req = urllib.request.Request(url)
    #添加header参数（隐藏代码，不被网页发现是代码访问）
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')

    response = urllib.request.urlopen(req) #括号里面的参数应该是req,而不是url，不然会被反爬
    html = response.read().decode('utf-8') #read()读取网页源代码，是二进制形式，需转换成utf-8形式

    return html

#创建获取网页照片函数
def get_img(html):
    p = r'<img class="BDE_Image" src="([^"]+\.jpg)"' #正则表达式（重要），获取照片字符串地址（爬取的是贴吧上的图片，除了吧主的图片外，还会把评论区相同字符串格式地址的图片也给下载下来）
    #创建一个imglist列表来存放图片的字符串地址
    imglist = re.findall(p,html) #正则表达式 findall方法，查找所有目标图片地址

    #folder 创建文件夹并命名
    folder = '爬图片1'
    os.makedirs(folder,exist_ok = True) #此语句表示运行前可不删除之前存在的同名文件
    os.chdir(folder) #保存到当前工作目录下的文件夹

    #写入照片
    for each in imglist:
        filename = each.split("/")[-1] #图片名字，取每个字符串地址最后斜杠后面的一段字符串
        urllib.request.urlretrieve(each,filename,None)#（不熟）

        #with open('photograth.jpg','wb') as f: #获取此照片
            #f.write(each) #写入此照片

if __name__ == '__main__': #（不熟）
    #获取网页
    url = "https://tieba.baidu.com/p/5658376209"
    #调用函数
    get_img(url_open(url))

