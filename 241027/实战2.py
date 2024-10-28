import time
import requests, csv

myHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.\
                   97 Safari/537.36 Core/1.116.438.400 QQBrowser/13.0.6071.400"
}
url = 'https://search.cnki.com.cn/api/search/listresult'
myParams = {
    "searchType": "MulityTermsSearch",
    "ArticleType": "0",
    "ParamIsNullOrEmpty": "false",
    "Islegal": "false",
    "Theme": "机器学习"
}
f = open("data2.csv", mode="w", encoding='utf-8')
csvwriter = csv.DictWriter(f, ["title", "summary", "author", "originate", "publishTime", "arcitleType",
                               "tutor", "kewWord", "downloadCount", "quoteCount"])
csvwriter.writeheader()
for page in range(1, 11):
    myParams.update({'page': page})
    response = requests.post(url, params=myParams, headers=myHeaders)
    articles = response.json()['articleList']
    for i in articles:
        dic = {
            "title": i['title'].replace('~#@', '').replace('@#~', ''),
            "summary": i['summary'].replace('~#@', '').replace('@#~', ''),
            "author": i['author'],
            "originate": i['originate'],
            "publishTime": i['publishTime'],
            "arcitleType": i['arcitleType'],
            "tutor": "无",
            "kewWord": i['keyWord'],
            "downloadCount": i['downloadCount'],
            "quoteCount": i['quoteCount'],
        }
        if 'tutor' in i.keys():
            dic.update({'tutor': i['tutor']})
        csvwriter.writerow(dic)
    response.close()
    time.sleep(2)
