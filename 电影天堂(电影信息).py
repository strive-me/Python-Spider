import requests
from lxml import etree

BASE_DOMAIN = 'https://www.dy2018.com/'
# 设置请求头部信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36',
}

# 1、将目标网站的页面全部爬取下来
# 获取每一个详情页面信息的url
def get_detail(url):
    # 请求网页数据
    response = requests.get(url=url, headers=HEADERS)
    # requests库中默认的编码方式和网页的编码方式不一样，所以就会产生乱码
    text = response.content.decode('gbk')

    html = etree.HTML(text)

    # 使用xpath解析网页
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    print(detail_urls)
    # 将得到的详情页面的url进行拼接
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    # 返回详情页面的url地址
    return detail_urls

# 获取网页数据函数
def parse_detail(url):
    movie = {}
    # 访问每一个电影详情的页面
    respose = requests.get(url,headers=HEADERS)
    text = respose.content.decode('gbk')
    # 解析网页
    html = etree.HTML(text)
    # 开始获取信息  头部信息
    title = html.xpath("//div[@class='title_all']/h1//text()")[0]
    movie['标题'] = title
    # 电影的所有信息存放的div
    Zoom = html.xpath("//div[@id='Zoom']")[0]
    # 海报
    cover = Zoom.xpath(".//img/@src")[0]
    movie['海报'] = cover
    # 电影截图
    screenshot = Zoom.xpath(".//img/@src")[1]
    movie['电影截图'] = screenshot
    # 信息
    infos = Zoom.xpath(".//text()")
    for index,info in enumerate(infos):
        if info.startswith("◎片　　名"):
            info = info.replace("◎片　　名","").strip()
            movie["译名"] = info
        elif info.startswith("◎年　　代"):
            info = info.replace("◎年　　代", "").strip()
            movie["年代"] = info
        elif info.startswith("◎产　　地"):
            info = info.replace("◎产　　地", "").strip()
            movie["产地"] = info
        elif info.startswith("◎上映日期"):
            info = info.replace("◎上映日期", "").strip()
            movie["上映日期"] = info
        elif info.startswith("◎片　　长"):
            info = info.replace("◎片　　长", "").strip()
            movie["片长"] = info
        elif info.startswith("◎导　　演"):
            info = info.replace("◎导　　演", "").strip()
            movie["导演"] = info
        elif info.startswith("◎主　　演"):
            info = info.replace("◎主　　演", "").strip()
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie['主演'] = actors

        elif info.startswith("◎简　　介"):
            info = info.replace("◎简　　介", "").strip()
            for x  in range(index+1,len(infos)):
                profile = infos[x].strip()
                movie["简介"] = profile

    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie["下载地址"] = download_url
    return movie


# 使用循环完成多个页面的访问
def spider():
    movies = []
    # 定义url地址
    base_url = 'https://www.dy2018.com/html/gndy/dyzz/index_{}.html'
    # 使用循环访问2---5页的所有电影
    for i in range(2,3):
        # 每一页的电影的url
        url = base_url.format(i)
        # 调用上边的函数获取每一页的电影的详情的url地址
        detail_urls = get_detail(url)
        # 将得到的所有的详情页面的地址传入获取详情信息的函数
        for detail_url in detail_urls:
            movie = parse_detail(detail_url)
            movies.append(movie)
    for i in movies:
        print(i)


if __name__ == '__main__':
    spider()
