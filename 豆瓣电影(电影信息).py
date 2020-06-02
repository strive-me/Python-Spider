import requests
from lxml import etree

# 1、将目标网站的页面全部爬取下来

# 设置请求头部信息
headers = {
'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36',
'Referer': 'https://movie.douban.com/'
}
# 定义url地址
douban_url = 'https://movie.douban.com/cinema/nowplaying/xian/'
# 使用requests发送请求
response = requests.get(url=douban_url,headers=headers)
# text属性是经过解码的str（Unicode）类型文本
# connect是直接从网页上抓取的内容，没有经过转换的字符串，是最开始的bytes格式内容
text = response.text

# 2、将抓取下来的网页内容根据需求提取
html = etree.HTML(text)
ul = html.xpath("//ul[@class='lists']")[0]
# print(etree.tostring(ul,encoding='utf-8').decode('utf-8'))
# 获取ul标签下的li标签
ul_li = ul.xpath("./li")

movies = []
for li in ul_li:
    # print(etree.tostring(li,encoding='utf-8').decode('utf-8'))
    title = li.xpath("@data-title")[0]
    region = li.xpath("@data-region")[0]
    director = li.xpath("@data-director")[0]
    actors = li.xpath("@data-actors")[0]
    poster = li.xpath(".//img/@src")[0]
    date = li.xpath(".//ul/li[@class='release-date']/text()")[0].strip()
    movie = {
        '电影名称':title,
        '地区':region,
        '导演':director,
        '演员':actors,
        '上映时间': date,
        '海报':poster,
    }
    movies.append(movie)


for i in movies:
    for k, v in i.items():
        with open('douban.txt','a+',encoding='utf-8') as fp:
            fp.write(str(k) + ' ' + str(v) + '\n')

