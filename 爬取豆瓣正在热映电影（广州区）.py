#豆瓣4.21正在热映的全部影片

import requests
from lxml import html
url = 'https://movie.douban.com/'

page = requests.Session().get(url)
tree = html.fromstring(page.text)
result = tree.xpath('//li[@class = "title"]//a/text()')

for each in result:
    print(each)

