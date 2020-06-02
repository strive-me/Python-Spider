import requests
from lxml import etree

BASE_DOMAIN = 'https://m.qiuwu.net'
# 设置请求头部信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36',
    'Referer': 'https://movie.douban.com/'
}

urls = "https://m.qiuwu.net/toplist/allvisit-{}.html"

def ranking_information():
    N = int(input("每页20本小说，输入多少页"))
    count = 0
    for page in range(1,N+1):
        url = urls.format(page)
        # 请求网页数据
        response = requests.get(url=url, headers=HEADERS)
        # print(response)
        # requests库中默认的编码方式和网页的编码方式不一样，所以就会产生乱码
        text = response.content.decode('gbk')

        html = etree.HTML(text)
        # 每一个里标签就是一本书的内容
        uls = html.xpath('//section[@class="list fk"]//ul[@class="xbk"]/li[@class="tjxs"]')
        # print(uls)
        detail_data = []
        for ul in uls:
            count += 1
            # 建立、字典存储信息
            detail = {}
            title = ul.xpath('./span[@class="xsm"]/a//text()')[0]
            author = ul.xpath('./span[@class=""]/a//text()')[0]
            presentation = ul.xpath('./span[@class=""]/text()')[1]
            addr = ul.xpath('./span[@class="xsm"]/a/@href')[0]
            # 对地址进行操作最终返回的是每一本书的主页地址
            addr1 = addr.split('/')[2]
            addr2 = addr.split('/')[2][:-3]
            url_model = 'https://m.qiuwu.net/html/{}/{}/'
            addr_url = url_model.format(addr2,addr1)
            detail["书名"] = title
            detail["作者"] = author
            detail["简介"] = presentation
            detail["链接"] = addr_url

            detail_data.append(detail)
            print("排名第 {} 的小说文章".format(count),end=": ")
            print(detail)

# if __name__ == '__main__':
#     ranking_information()