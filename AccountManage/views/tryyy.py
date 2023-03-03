import time, json

import requests, random


def test1(data):
    room = [1454962223, 1454962223]
    url = "https://zhuiya.yy.com/admin-web/robot/public/getHitRule"
    data = {
        "uid": data["uid"]
    }
    res = requests.get(url=url, params=data)
    print(res.text)
    if "uidEnterFirst" in json.loads(res.text)["data"]:
        sid = json.loads(res.text)["data"]["uidEnterFirst"][0:10]
        ssid = json.loads(res.text)["data"]["uidEnterFirst"][11:21]
        print(sid, ssid)
        room[0] = json.loads(res.text)["data"]["uidEnterFirst"][0:10]
        room[1] = json.loads(res.text)["data"]["uidEnterFirst"][11:21]
        return room
    return room


def test2(data):
    url = "https://zhuiya.yy.com/admin-web/robot/public/getPhoneMask"
    data = {
        "uid": data["uid"]
    }
    res = requests.get(url=url, params=data)
    print(res.text)


def test3(data):
    url = "https://zhuiya.yy.com/admin-web/robot/public/clearCache"
    data = {
        "uid": data["uid"],
        "sid": data["sid"],
        "ssid": data["ssid"]

    }
    res = requests.get(url=url, params=data)
    print(res.text)


def sss(data):
    room = test1(data)
    time.sleep(1)
    test2(data)
    time.sleep(1)
    data["sid"] = room[0]
    data["ssid"] = room[1]
    test3(data)
    time.sleep(1)
    test1(data)


if __name__ == '__main__':
    # 小米mix4
    data1 = {
        "uid": "2756691246",
        "hdid": "986a530d4445481e3888135884da4690",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # 	iPhone13ProMax
    data2 = {
        "uid": "2712301607",
        "hdid": "036fd0c9826ca50cb1ce07513daee5349c9993bd",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # 一加OnePlus9
    data3 = {
        "uid": "2729331104",
        "hdid": "617d53b1ebe50ac6050a714b7b3b627f",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # iPhone12ProMax
    data4 = {
        "uid": "2689641056",
        "hdid": "bd2c51d13bca1394441132fab7054dbeeadb9cee",
        "sid": "1454054224",
        "ssid": "2807602905"
    }

    data11 = {
        "uid": "2902910285",
        "hdid": "b0bb246b39b03864ca4a6a7e2da5dc252b38099a",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    data22 = {
        "uid": "2902914739",
        "hdid": "b0bb246b39b03864ca4a6a7e2da5dc252b38099a",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    data33 = {
        "uid": "2901401484",
        "hdid": "3c69113314374152e30ada30668aq4fa3",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    data44 = {
        "uid": "2902910344",
        "hdid": "3c69113314374152e30ada30668aq4fa3",
        "sid": "1454054224",
        "ssid": "2807602905"
    }

    test1(data4)