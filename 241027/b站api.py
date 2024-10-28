from requests import get
from json import loads
from numpy import average
from os.path import dirname, abspath

cwd = dirname(abspath(__file__)) + '\\'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/94.0.4606.71 Safari/537.36 Core/1.94.169.400 QQBrowser/11.0.5130.400"}
ans = open(cwd + '[title]BVids.txt', 'w', encoding='utf-8')
with open(cwd + 'BVids.txt', 'r', encoding='utf-8') as file:
    for i in file:
        BVid = i.split("\n")[0]
        res = get("https://api.bilibili.com/x/web-interface/view?bvid=" + BVid, headers=headers)
        resdict = loads(res.text)
        try:
            title = resdict["data"]["title"]
        except Exception as e:
            print("failure")
            ans.write("err:" + BVid + ":" + str(e) + "\n")
            continue
        allP = []
        for i in resdict["data"]["pages"]:
            temp = dict()
            temp["cid"] = i["cid"]
            temp["page"] = i["page"]
            temp["part"] = i["part"]
            allP.append(temp)
        print("success")
        if len(allP) > 1: ans.write("【分P】")
        ans.write(BVid + "【" + title.replace("【", "[").replace("】", "]") + "】\n")

input("完成。")
