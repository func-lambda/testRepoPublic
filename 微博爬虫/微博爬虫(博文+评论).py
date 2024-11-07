import requests
from lxml import etree
import csv
import time, random
from datetime import datetime
import pytz


def toUNIXSec(t1, regex):
    if regex == 1:
        return int(datetime.strptime(t1, "%a %b %d %H:%M:%S %z %Y").astimezone(pytz.utc).timestamp())
    elif regex == 2:
        if not '年' in t1:
            t1 = str(datetime.now().year) + '年' + t1
        return int(datetime.strptime(t1, "%Y年%m月%d日 %H:%M").timestamp())


def findInterest(jsoni):
    reslist = []
    for i in jsoni:
        tmp = {
            '评论内容': etree.HTML(i['text']).xpath('string(/)'),
            '评论人': i['id'],
            '评论时间': toUNIXSec(i['created_at'], 1),
            'IP': i['source'].strip("来自"),
        }
        reslist.append(tmp)
        if 'comments' in i and i['comments']:
            reslist = reslist + findInterest(i['comments'])
    return reslist


def getComments(mid, max_id, max_id_type):
    proxies = {"http": random.choice(proxy_list)}
    commenti = requests.get(f"https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid}&max_id={max_id}\
                                              &max_id_type={max_id_type}&display=0&retcode=6102&#39;",
                            headers=myheaders, cookies=mycookies, proxies=proxies)
    commenti.encoding = 'utf-8'
    commenti = commenti.json()['data']
    reslist = findInterest(commenti['data'])
    return commenti['max_id'], commenti['max_id_type'], reslist


def downloadOneBowen(bowen):
    name = bowen.xpath("./div/div[1]/div[2]/div[1]/div[2]/a/text()")[0].strip()
    date = toUNIXSec(bowen.xpath("./div/div[1]/div[2]/div[2]/a[1]/text()")[0].strip(), 2)
    if bowen.xpath('./div/div[1]/div[2]/p[@node-type=\'feed_list_content_full\']'):
        word = bowen.xpath('string(./div/div[1]/div[2]/p[@node-type=\'feed_list_content_full\'])') \
            .replace("收起d", '').strip()
    else:
        word = bowen.xpath('string(./div/div[1]/div[2]/p[@node-type=\'feed_list_content\'])').strip()
    zhuanfa = bowen.xpath("./div/div[2]/ul/li[1]/a/span/following::text()[1]")[0]
    zhuanfa = ('0' if zhuanfa == ' 转发' else zhuanfa.strip())
    pinglun = bowen.xpath("./div/div[2]/ul/li[2]/a/span/following::text()[1]")[0]
    pinglun = ('0' if pinglun == ' 评论' else pinglun.strip())
    dianzan = bowen.xpath("./div/div[2]/ul/li[3]/a/button/span[2]/text()")[0]
    dianzan = ('0' if dianzan == '赞' else dianzan.strip())
    # print(name, f"data={date}", f"len={len(word)}", zhuanfa, pinglun, dianzan)
    bowen_n = {
        "发布者": name,
        "发布时间": date,
        "微博内容": word,
        "转发数": zhuanfa,
        "评论数": pinglun,
        "点赞数": dianzan,
    }
    # 以下获取评论
    mid = bowen.xpath("./@mid")[0]
    # print(f"mid={mid}")
    if pinglun == '0':
        return bowen_n, []
    reslist = []
    max_id, max_id_type, temp = getComments(mid, 0, 0)  # type=0按热门，type=1按时间
    reslist = reslist + temp
    while max_id:
        max_id, max_id_type, temp = getComments(mid, max_id, max_id_type)
        reslist = reslist + temp
    return bowen_n, reslist


myheaders = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 \
                   Safari/537.36",
}
proxy_list = [
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
]
cookies_text = '''
SINAGLOBAL=6181368979455.227.1730380216070; SCF=AshHZztEPpz3vs9Xvy7aBUZGU5PJdQZH36qmZIwpw3JphRaBaCrF192r9NTL5LLG47JwvtT
YUcunBZdoUpEez0g.; _s_tentry=passport.weibo.com; Apache=1043242127831.01.1730460856072; ULV=1730460856074:2:1:2:1043242
127831.01.1730460856072:1730380216079; cross_origin_proto=SSL; ALF=1733052927; SUB=_2A25KIMyvDeRhGeFH7lsY9y3Kyj6IHXVpXE
BnrDV8PUJbkNANLUz_kW1NesjlvBt56Oz8CthWGJXr6maUIalqoWL0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9I0fsNHpP6bMMog6qKkLy5J
pX5KzhUgL.FoM4SK.4S0eceKz2dJLoI7_JUg4oPcpydgi.qBtt; UOR=,,www.baidu.com
'''
mycookies = {}
for i in cookies_text.split(';'):
    a, b = i.strip().replace("\n", '').split('=')
    mycookies[a] = b

f1 = open("微博博文.csv", mode="w", newline='', encoding='utf-8')
csvwriter1 = csv.DictWriter(f1, ["发布者", "发布时间", "微博内容", "转发数", "评论数", "点赞数"])# "形式（文字、图片、视频）"
csvwriter1.writeheader()
f2 = open("微博评论.csv", mode="w", newline='', encoding='utf-8')
csvwriter2 = csv.DictWriter(f2, ["评论人", "评论内容", "评论时间", "IP"])
csvwriter2.writeheader()

url = "https://s.weibo.com/weibo?q=%23杨利伟的太空一日%23&nodup=1"
for page in range(1, 3):
    proxies = {"http": random.choice(proxy_list)}
    resp = requests.get(url + f"&page={page}", headers=myheaders, cookies=mycookies, proxies=proxies)
    resp.encoding = 'utf-8'
    html = etree.HTML(resp.text)
    for bowen in html.xpath("//*[@action-type=\'feed_list_item\']"):
        bowen_n, commentlist = downloadOneBowen(bowen)
        print(bowen_n)
        print(commentlist)
        print('')
        csvwriter1.writerow(bowen_n)
        for comment in commentlist:
            csvwriter2.writerow(comment)
    print(f"page={page}\n")

f1.close()
f2.close()