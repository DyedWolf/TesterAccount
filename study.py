import requests,json, random

# 热门：32600 交友:32100  宝贝：32900 女团：32200
headers = {"x-fts-platform": "4"}

url = "https://yomi1-test.yy.com/zhuiya_recommend/v2/get_recommend_info?id={}&next=0".format(10000)
response = requests.get(url=url, headers=headers)
data = json.loads(response.content)["list"]
print(data)
if data is not None:

    # 看看有没有团战房

    sid_data = {"xiangqin": [], "tuanzhan": [], "luandou": [], "duorenshipin": []}
    for i, cleanData in enumerate(data):
        if data[i]["gameType"] == 7:
            sid_data["luandou"].append((data[i]["sid"], data[i]["ssid"]))
        if data[i]["gameType"] == 0 and data[i]["business"] == 1:
            sid_data["xiangqin"].append((data[i]["sid"], data[i]["ssid"]))
        if data[i]["gameType"] == 2:
            sid_data["tuanzhan"].append((data[i]["sid"], data[i]["ssid"]))
        if data[i]["gameType"] == 8:
            sid_data["duorenshipin"].append((data[i]["sid"], data[i]["ssid"]))
    print("相亲房数量：{}，团战房数量：{}，乱斗房数量：{}".format(len(sid_data["xiangqin"]), len(sid_data["tuanzhan"]),
                                              len(sid_data["luandou"])))
    print("相亲房数量：{}，团战房数量：{}，乱斗房数量：{}".format(len(sid_data["xiangqin"]), len(sid_data["tuanzhan"]),
                                                    len(sid_data["luandou"])))


    # gameType = gameType

    ii = []
    for channelId in data:
        if channelId['gameType'] == 2:
            a = '{},{}'.format(channelId['sid'], channelId['ssid'])
            ii.append(a)
            # break
    print(ii)
    b = random.choice(ii)
    x, y = b.split(',')
    print(x,y)

