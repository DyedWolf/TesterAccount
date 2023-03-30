import requests, json, pymongo

from django.db import connection
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from AccountManage import models


def recommend_list(request):
    return render(request, "recommend_list.html")


@csrf_exempt
def add_recommend_room(request):
    client = pymongo.MongoClient(host='125.94.237.198', port=19999)
    mydb = client["fts_zhuiya_recommend_v2"]
    mycol = mydb["recommend_sid_picture_list"]

    sid = int(request.POST.get("sid"))
    ssid = int(request.POST.get("ssid"))
    businessType = int(request.POST.get("businessType"))

    if sid and ssid and businessType:
        results = mycol.find({"sid": sid, "ssid": ssid})
        exitData = []
        for result in results:
            # print(result)
            exitData.append(result["_id"])
        addData = str(sid) + "_" + str(ssid) + "_" + str(businessType)
        print(exitData, addData)
        if addData not in exitData:
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
            result = mycol.insert_one(data)
            print(result.acknowledged)
            response = {"status": True}
            client.close()
            return JsonResponse(response)
        if addData in exitData:
            data = {
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
            print("更新数据")
            updateDate = mycol.find_one({"_id": addData})
            print(updateDate)
            result = mycol.update_one({"_id": addData}, {"$set": data})
            print(result.acknowledged)
            response = {"status": True}
            client.close()
            return JsonResponse(response)

    client.close()
    response = {"status": False, "error": "未知错误！"}
    return JsonResponse(response)
