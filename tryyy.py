import pymongo

client = pymongo.MongoClient(
    "mongodb://fts_mgo4_test2:de5HTRXfRXm0lncRA1eRKJE5@10.12.36.22:10011,10.26.130.24:10007,10.26.2.210:10007/fts_zhuiya_recommend_v2?replicaSet=ftsmgo4test21")
mydb = client["fts_zhuiya_recommend_v2"]
mycol1 = mydb["recommend_jy_list"]
mycol = mydb["recommend_sid_picture_list"]

results = mycol1.find({"sid": 1459037660, "ssid": 1459037660})


new_data = {
    "_id": "1459037660:1459037660:11400",
    "mode": 1,
    "recommend_end": 1691587400,
    "recommend_start": 1690896200,
    "sid": 1459037660,
    "ssid": 1459037660,
    "weight": 21,
    "zoneid": 11400
}
result = mycol1.update_one({"_id": "{}".format("1459037660:1459037660:11400")}, {"$set": new_data}, upsert=True)
print(result.acknowledged)
client.close()
