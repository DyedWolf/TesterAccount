import requests, json, pymongo

from django.db import connection
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from AccountManage import models


def recommend_list(request):
    return render(request, "recommend_list.html")


def recommend(request):
    return render(request, "recommend.html")


s = "mongodb://fts_mgo4_test2:de5HTRXfRXm0lncRA1eRKJE5@10.12.36.22:10011,10.26.130.24:10007,10.26.2.210:10007/fts_zhuiya_recommend_v2?replicaSet=ftsmgo4test21"
a = "mongodb://125.94.237.198:19999/fts_zhuiya_recommend_v2"


@csrf_exempt
def add_recommend_room(request):
    client = pymongo.MongoClient("mongodb://fts_mgo4_test2:de5HTRXfRXm0lncRA1eRKJE5@10.12.36.22:10011,10.26.130.24:10007,10.26.2.210:10007/fts_zhuiya_recommend_v2?replicaSet=ftsmgo4test21")
    mydb = client["fts_zhuiya_recommend_v2"]
    mycol = mydb["recommend_sid_picture_list"]

    sid = int(request.POST.get("sid"))
    ssid = int(request.POST.get("ssid"))
    title = str(request.POST.get("title"))
    businessType = int(request.POST.get("businessType"))
    addId = str(sid) + "_" + str(ssid) + "_" + str(businessType)

    if sid and ssid and businessType:
        results = mycol.find({"sid": sid, "ssid": ssid})
        exitData = []
        for result in results:
            # print(result)
            exitData.append(result["_id"])
        print(exitData, addId, title)

        if addId not in exitData:
            print("插入数据")
            data = {"_id": "{}_{}_{}".format(sid, ssid, businessType),
                    "businessType": businessType,
                    "sid": sid,
                    "ssid": ssid,
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
                    "title": title,
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
            result = mycol.insert_one(data)
            print(result.acknowledged)
            if result.acknowledged:
                response = {"status": True}
                client.close()
                return JsonResponse(response)
        if addId in exitData:
            allData = {
                "_id": "{}_{}_{}".format(sid, ssid, businessType),
                "businessType": businessType,
                "sid": sid,
                "ssid": ssid,
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
                "title": title,
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
            print("更新数据")
            result = mycol.update_one({"_id": "{}".format(addId)}, {"$set": allData})
            print(result.acknowledged)
            if result.acknowledged:
                response = {"status": True}
                client.close()
                return JsonResponse(response)

    client.close()
    response = {"status": False, "error": "未知错误！"}
    return JsonResponse(response)


@csrf_exempt
def add_recommend_uid(request):
    client = pymongo.MongoClient("mongodb://fts_mgo4_test2:de5HTRXfRXm0lncRA1eRKJE5@10.12.36.22:10011,10.26.130.24:10007,10.26.2.210:10007/fts_zhuiya_recommend_v2?replicaSet=ftsmgo4test21")
    mydb = client["fts_zhuiya_recommend_v2"]
    mycol = mydb["recommend_compere_picture_list"]

    title = str(request.POST.get("title"))
    uid = int(request.POST.get("uid"))
    businessType = int(request.POST.get("businessType"))
    addId = str(uid) + "_" + str(businessType)

    results = mycol.find({"compereUID": uid})
    exitData = []
    for result in results:
        # print(result)
        exitData.append(result["_id"])
    print(exitData, addId, title)

    allData = {
        'businessType': businessType,
        'compereUID': uid,
        'takeEffect': 0,
        'takeTitleEffect': 0,
        'featurePictureList': [],
        'currentFeaturePicture': '',
        'uptime': 1662106386,
        'subTag': '',
        'labels': [],
        'rating': '',
        'picture': 'https://makefriends.bs2dl.yy.com/1662106385_84d5c31e95e671b73ad3be0599c2d09b.JPG',
        'pictureStatus': 2,
        'pictureReason': '内审:2022.09.02 16:13',
        'title': title,
        'titleStatus': 2,
        'titleReason': '',
        'picture45': '',
        'pictureStatus45': 0,
        'pictureReason45': '',
        'picture169': '',
        'pictureStatus169': 0,
        'pictureReason169': '',
        'textTip': '',
        'textTipStatus': 0,
        'textTipReason': '',
        'uploadPicture1110': '',
        'uploadStatus1110': 0,
        'uploadReason1110': '',
        'uploadTime1110': 0,
        'contentLabel': ''
    }
    print("更新数据")
    result = mycol.update_one({"_id": "{}".format(addId)}, {"$set": allData}, upsert=True)
    print(result.acknowledged)
    if result.acknowledged:
        response = {"status": True}
        client.close()
        return JsonResponse(response)

    client.close()
    response = {"status": False, "error": "未知错误！"}
    return JsonResponse(response)
