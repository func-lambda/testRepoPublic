import requests
from bs4 import BeautifulSoup
import time, random
import pymysql

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 \
    Safari/537.36",
    "referer": "https://movie.douban.com/"
}
proxy_list = [
    # '58.246.58.150:9002',
    # '47.115.173.217:8989',
    # '117.50.108.90:7890',
    # '120.25.1.15:7890',
    # ---
    '58.246.58.150:9002',
    '111.26.177.28:9091',
    '139.9.119.20:80',
    '117.50.108.90:7890',
    '58.220.95.32:10174',
    '58.220.95.30:10174',
    '117.74.65.207:443',
    '47.116.181.146:8800',
    '47.99.112.148:8060',
    '47.92.194.235:8800',
    '47.122.56.158:8081',
    '114.215.127.92:9100',
    '47.109.83.196:8800',
    '47.121.133.212:4006',
    '47.122.5.165:4006',
    '47.116.126.57:3128',
    '47.104.27.249:80',
    '39.102.211.162:3128',
    '39.102.209.163:3128',
    '47.122.31.238:80',
    # ---
]
conn = pymysql.connect(host='localhost', user='root', password='rootpwd', database='douban',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

url = "https://movie.douban.com/top250"
urls = []
for i in range(10):
    proxies = {"http": random.choice(proxy_list)}
    resp = requests.get(url + "?start=" + str(i * 25), headers=headers, proxies=proxies)
    while resp.status_code == 443:
        print("443 retry")
        time.sleep(1)
        resp = requests.get(url + "?start=" + str(i * 25), headers=headers, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    while not soup.select("ol li"):
        print('retry')
        time.sleep(1)
        proxies = {"http": random.choice(proxy_list)}
        resp = requests.get(url + "?start=" + str(i * 25), headers=headers, proxies=proxies)
        soup = BeautifulSoup(resp.text, 'html.parser')
    for lis in soup.select("ol li"):
        urls.append(lis.select("div div div div a")[0].get('href'))
        print(urls[-1], i)
    time.sleep(1)
print("影片数：", len(urls))
if not len(urls) == 250: exit(250)
# urls = ["https://movie.douban.com/subject/1291546/","https://movie.douban.com/subject/1292052/"]

for a in urls:
    proxies = {"http": random.choice(proxy_list)}
    print(urls.index(a), " : ", a)
    req = requests.get(a, headers=headers, proxies=proxies)
    while req.status_code == 443:
        print("443 retry")
        time.sleep(1)
        req = requests.get(a, headers=headers, proxies=proxies)
    soup = BeautifulSoup(req.text, 'html.parser')

    info = soup.find("div", {"id": "info"})
    while not info:
        print("反爬" if '有异常请求从你的 IP 发出' in req.text else "未知")
        time.sleep(1)
        proxies = {"http": random.choice(proxy_list)}
        req = requests.get(a, headers=headers, proxies=proxies)
        soup = BeautifulSoup(req.text, 'html.parser')
        info = soup.find("div", {"id": "info"})

    attrss = info.find_all("span", {"class": "attrs"})
    dic = {
        "电影名": soup.find("span", {"property": "v:itemreviewed"}).text,
        "导演": attrss[0].find("a").text,
        "编剧": '无',
        "主演": "无",
        "类型": ' / '.join([i.text for i in info.find_all("span", {"property": "v:genre"})]),
        "制片国家/地区": info.find("span", string="制片国家/地区:").next_sibling.text.strip(' '),
        "语言": info.find("span", string="语言:").next_sibling.text.strip(' '),
        "上映日期": ' / '.join([i.text for i in info.find_all("span", {"property": "v:initialReleaseDate"})]),
        "片长": info.find("span", {"property": "v:runtime"}).text,
        "又名": "无",
        "IMDb": info.find("span", string="IMDb:").next_sibling.text.strip(' '),
    }
    if len(attrss) == 3:
        dic.update({"主演": ' / '.join([i.text for i in attrss[2].find_all("a")])})
    if info.find("span", string="编剧:"):
        dic.update({"编剧": ' / '.join([i.text for i in attrss[1].find_all("a")])})
    if info.find("span", string="又名:"):
        dic.update({"又名": info.find("span", string="又名:").next_sibling.text.strip(' ')})
    print(dic)
    vvv = tuple(dic.values())
    sqll = 'insert into top250(电影名,导演, 编剧, 主演, 类型, 制片国家地区, 语言, 上映日期, 片长, 又名, IMDb) \
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sqll, vvv)
        conn.commit()
    except Exception as e:
        print('插入数据失败', e)
        conn.rollback()

    time.sleep(1)

cursor.close()
conn.close()
print("over!")
