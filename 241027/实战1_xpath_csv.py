import requests
from lxml import etree
import csv, time, random

# 这个没加代理，所以爬不了太多
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 \
    Safari/537.36",
    "referer": "https://movie.douban.com/"
}
f = open("data.csv", mode="w", encoding='utf-8')
csvwriter = csv.DictWriter(f, ["电影名", "导演", "编剧", "主演", "类型", "制片国家/地区", "语言", "上映日期", "片长",
                               "又名", "IMDb"])
csvwriter.writeheader()

url = "https://movie.douban.com/top250"
urls = []
for i in range(10):
    resp = requests.get(url + "?start=" + str(i * 25), headers=headers)
    while resp.status_code == 443:
        print("443 retry")
        time.sleep(random.random() * 5 + 5)
        resp = requests.get(url + "?start=" + str(i * 25), headers=headers)
    html = etree.HTML(resp.text)
    urls = urls + html.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href")
    time.sleep(random.random() * 5 + 5)

print("影片数：", len(urls))
# urls = ["https://movie.douban.com/subject/1652587/"]
for a in urls:
    print(urls.index(a), " : ", a)
    req = requests.get(a, headers=headers)
    while req.status_code == 443:
        print("443 retry")
        time.sleep(random.random() * 5 + 5)
        req = requests.get(a, headers=headers)
    i = etree.HTML(req.text)
    try:
        info = i.xpath("/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]")[0]
    except Exception as e:
        print(req.text)
        print("反爬")
        exit(1)
    info = i.xpath("/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]")[0]
    dic = {
        "电影名": info.xpath("../../../../../../h1/span[1]/text()")[0],
        "导演": info.xpath("string(./span[1]/span[2])"),
        "编剧": info.xpath("string(./span[2]/span[2])"),
        "主演": "无",
        "类型": ' / '.join(info.xpath("./span[@property=\"v:genre\"]/text()")),
        "制片国家/地区": info.xpath("./span[text()=\"制片国家/地区:\"]/following::text()[1]")[0].strip(' '),
        "语言": info.xpath("./span[text()=\"语言:\"]/following::text()[1]")[0].strip(' '),
        "上映日期": ' / '.join(info.xpath("./span[@property=\"v:initialReleaseDate\"]/text()")),
        "片长": info.xpath("./span[@property=\"v:runtime\"]/text()")[0],
        "又名": "无",
        "IMDb": info.xpath("./span[text()=\"IMDb:\"]/following::text()[1]")[0].strip(' '),
    }
    if info.xpath("string(./span[3]/span[2])"):
        dic.update({"主演": info.xpath("string(./span[3]/span[2])")})
    if info.xpath("./span[text()=\"又名:\"]"):
        dic.update({"又名": info.xpath("./span[text()=\"又名:\"]/following::text()[1]")[0].strip(' ')})
    print(dic)
    csvwriter.writerow(dic)

    time.sleep(random.random() * 5 + 5)
f.close()
print("over!")
