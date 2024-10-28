from lxml import etree
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 \
    Safari/537.36"
}
# proxies = {"http": '58.246.58.150:9002'}
url = 'https://www.zdaye.com/free/?&sleep=1&px=4'
resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
html = etree.HTML(resp.text)

a = html.xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/text()')
b = html.xpath('/html/body/div[3]/div/table/tbody/tr/td[2]/text()')
c = []
for i in range(len(a)):
    c.append(f"'{a[i]}:{b[i]}',")
with open('proxies.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(c))
