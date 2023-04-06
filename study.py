import requests, json, re, pymongo
#
# url = "http://repo.yy.com/dwbuild/mobile/ios/Yomi/yomi_1.14.0_dev_feature/"
# res = requests.get(url=url)
# print(res.text)
# response = json.dumps(res.text)
# reData = re.match(r'(.*)href="(.*?)".*', response, re.M | re.I)
# print(reData)


# import os
# path = '//repo.yy.com/dwbuild/mobile/ios/Yomi/yomi_1.14.0_dev_feature/'      # 输入文件夹地址
# files = os.listdir(path)   # 读入文件夹
# num_png = len(files)       # 统计文件夹中的文件个数
# print(num_png)             # 打印文件个数
# # 输出所有文件名
# print("所有文件名:")
# for file in files:
#     print(file)



client = pymongo.MongoClient(host='125.94.237.198', port=19999)
mydb = client["fts_zhuiya_recommend_v2"]
mycol = mydb["recommend_compere_picture_list"]

results = mycol.find({"compereUID": 2711427642, 'businessType': 201})
exitData = []
for result in results:
    print(result)
    exitData.append(result["_id"])
print(exitData)