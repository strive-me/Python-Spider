import requests
from lxml import etree
import os
from PythonSpider.网页小说爬取.凤舞小说排行榜信息 import ranking_information

BASE_DOMAIN = 'https://m.qiuwu.net'
# 设置请求头部信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36',
    'Referer': 'https://movie.douban.com/'
}

# 获取每一章节的url
def get_url(url_section):
    # 请求网页数据
    response = requests.get(url=url_section,headers=HEADERS)
    # print(response)
    # requests库中默认的编码方式和网页的编码方式不一样，所以就会产生乱码
    text = response.content.decode('gbk')

    html = etree.HTML(text)
    detail_urls = html.xpath("//section[@class='zjlb']/ul/li/a/@href")
    # print(detail_urls)
    # 将得到的详情页面的url进行拼接
    detail_urls = map(lambda url: BASE_DOMAIN + url, detail_urls)
    return detail_urls

# 获取书的名称
def create_file(book_index_path):
    respose = requests.get(url=book_index_path,headers=HEADERS)
    text = respose.content.decode('gbk')
    # 解析网页
    html = etree.HTML(text)
    # 解析出标题
    title_file_name = html.xpath('//div[@class="zhong"]/a//text()')
    # 拼接文佳名称,将书的标题从列表中拿出来
    t_file = title_file_name[0]

    # 返回是否存在该书名
    return t_file

# 爬取正文和章节名称
def get_detail(url_detail):
    # 访问每一个小说详情的页面
    respose = requests.get(url_detail, headers=HEADERS)
    text = respose.content.decode('gbk')
    # 解析网页
    html = etree.HTML(text)
    # 获取章节标题
    title = html.xpath('//div[@class="zhong"]/a//text()')[0]
    # 获取正文内容
    text_part = html.xpath('//section[@class="zj"]//article//p/text()')
    # print(title)
    # print(text_part)
    return title,text_part

# 将得到的内容写入本地文件
def index_url(book_index_path):
    # 电子书的地址
    base_url = book_index_path+'&id={}'
    N = int(input("输入页数"))
    for i in range(1,N+1):
        # 拼接地址完成每一页
        url = base_url.format(i)
        # print(url)
        detail_url = get_url(url)
        # 得到详情页面的url开始进行爬取
        # print("detail_urls",list(detail_url))
        for x in detail_url:
            title,text_part= get_detail(x)
            # 拼接得到每一章节的文件名称
            title_name = title + '.text'
            # 判断书的文件夹是否存在,得到书本的名称和路径是否存在
            book_name = create_file(book_index_path)
            # 放入异常，文件存在，抛出异常，进入except直接写入，没有异常则直接创建文件并写入
            try:
                # 创建一个文佳夹，名字为书的名字
                os.mkdir(book_name)
                # 进入文件夹
                os.chdir(book_name)
                with open(title_name, 'a') as fp:
                    for txt in text_part:
                        fp.write(txt + '\n')
                    print(title + "  写入完成")
                os.chdir('../')
            except:
                # 进入文件夹
                os.chdir(book_name)
                with open(title_name, 'a') as fp:
                    for txt in text_part:
                        fp.write(txt + '\n')
                    print(title + "  写入完成")
                os.chdir('../')

if __name__ == '__main__':
    flag = input("是否需要排行榜推荐y/n  :")
    if flag == 'y':
        ranking_information()
        print("*" * 50)
        book_index_path = input("输入书本的主页地址")
        while book_index_path is '':
            print('小说首页地址不能为空')
            book_index_path = input("输入书本的主页地址")
        index_url(book_index_path)
    else:
        book_index_path = input("输入书本的主页地址")
        while book_index_path is '':
            print('小说首页地址不能为空')
            book_index_path = input("输入书本的主页地址")
        index_url(book_index_path)


