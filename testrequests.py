import re,requests,json

x = 1111111111111150721

for i in range(100):
    x = x + i
    # print(x)

url = "https://yomi1.yy.com/zhuiya_recommend/v2/get_recommend_info?id=32100&next=0"
headers = {
    "x-fts-platform": "4"
}
gameType = []
res = requests.get(url=url, headers=headers)
data = json.loads(res.content)["list"]
for i, cleanData in enumerate(data):
    data[i].pop('liveInfo')
    gameType.append(data[i]["gameType"])
print(gameType)
