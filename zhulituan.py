import time, json

import requests, random


def test1(data):
    room = [1454962223, 1454962223]
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/getHitRule"
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
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/getPhoneMask"
    data = {
        "uid": data["uid"]
    }
    res = requests.get(url=url, params=data)
    print(res.text)


def test3(data):
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/clearCache"
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
    # iPhone7Plus
    data1 = {
        "uid": "141746805669898",
        "hdid": "1883f0eecd52807b6dba124776639a327878b725",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # 	iPhone14
    data2 = {
        "uid": "2718596829",
        "hdid": "009e66ecdf97f911e3e0c814082c78f5a6132a4a",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # Redmi K40
    data3 = {
        "uid": "2678035356",
        "hdid": "1db0f59a5407fa61f496804a515f28fa",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # 三星NOTE20
    data4 = {
        "uid": "2756691246",
        "hdid": "5ea259affc2808778420bca55666b374",
        "sid": "1454054224",
        "ssid": "2807602905"
    }
    # OPPO R17
    data5 = {
        "uid": "2818222471",
        "hdid": "679bd65640faeef7235cf9e21e4d8b39",
        "sid": "1454054224",
        "ssid": "2807602905"
    }

    test1(data1)
