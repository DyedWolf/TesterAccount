import re, requests, json

# x = 1111111111111150721
#
# for i in range(100):
#     x = x + i
# print(x)

url = "https://yomi1.yy.com/zhuiya_recommend/v2/get_recommend_info?id=32100&next=0"
headers = {
    "x-fts-platform": "4"
}
roomId = []
res = requests.get(url=url, headers=headers)
print(type(json.loads(res.content)))
data = res.json()

# 看看有没有团战房

sid_data = {"xiangqin": [], "tuanzhan": [], "luandou": []}

for i, cleanData in enumerate(data["list"]):
    if data["list"][i]["gameType"] == 7:
        sid_data["luandou"].append((data["list"][i]["sid"], data["list"][i]["ssid"]))
    if data["list"][i]["gameType"] == 0:
        sid_data["xiangqin"].append((data["list"][i]["sid"], data["list"][i]["ssid"]))
    if data["list"][i]["gameType"] == 2:
        sid_data["tuanzhan"].append((data["list"][i]["sid"], data["list"][i]["ssid"]))
print("相亲房数量：{}，团战房数量：{}，乱斗房数量：{}".format(len(sid_data["xiangqin"]), len(sid_data["tuanzhan"]), len(sid_data["luandou"])))