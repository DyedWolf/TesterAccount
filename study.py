import pymongo, json

# 2.（1）与数据库访问器连接
client = pymongo.MongoClient(host='125.94.237.198', port=19999)
# 2.（2）连接到具体的mongodb服务器或副本集：
# client = pymongo.MongoClient(host='125.94.237.198:19999/fts_zhuiya_recommend_v2')

# 创建数据库 runoobdb :
mydb = client["fts_zhuiya_recommend_v2"]
# 创建集合：collection:
mycol = mydb["recommend_sid_picture_list"]

# 3、访问数据库
# db = client.mydb
# print(db)
exitData = []
results = mycol.find({"sid": 87814665, "ssid": 2805640284})  # .find_one({"sid": 1451119354, "ssid": 2798359950})
for result in results:
    exitData.append(result["_id"])
    print(result)
print(exitData)

"1355632767_2814984951_1"
addId = "1451119354_2791669992_1"
updateDate = mycol.find_one({"_id": addId})

allData = {
    "takeEffect": 0,
    "takeTitleEffect": 0,
    "featurePictureList": [

    ],
    "currentFeaturePicture": "",
    "uptime": 1679625475,
    "subTag": "",
    "labels": [

    ],
    "rating": "",
    "picture": "https://makefriends.bs2dl.yy.com/1679625466_8974eefad506b9a17b4a32c5885a3b38.jpg",
    "pictureStatus": 2,
    "pictureReason": "\u5185\u5ba1:2023.03.24 10:38",
    "title": "\u4e4c\u9e26\u5750\u98de\u673a~",
    "titleStatus": 2,
    "titleReason": "",
    "picture45": "",
    "pictureStatus45": 0,
    "pictureReason45": "",
    "picture169": "",
    "pictureStatus169": 0,
    "pictureReason169": "",
    "textTip": "",
    "textTipStatus": 0,
    "textTipReason": "",
    "uploadPicture1110": "",
    "uploadStatus1110": 0,
    "uploadReason1110": "",
    "uploadTime1110": 0,
    "contentLabel": ""}
# result = mycol.insert_one(portData)
result = mycol.update_one({"_id": "1451119354_2791669992_1"}, {"$set": allData})
print(result.acknowledged)
