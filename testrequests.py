import requests, json

url = "https://yomi1-test.yy.com/zhuiya_recommend/v2/get_recommend_info?id={}&next=0".format(11400)
headers = {"x-fts-platform": "4"}
response = requests.get(url=url, headers=headers)
data = json.loads(response.content)["list"]
print(data)