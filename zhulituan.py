import requests, json, re


def clear_cache(room_data):
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/clearCache"
    data = {
        "uid": room_data[-1],
        "sid": room_data[0],
        "ssid": room_data[1]
    }
    res = requests.get(url=url, params=data)
    print(res.text)
    print(res.url)


def get_hit_rule(user_data):
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/getHitRule"
    data = {
        "uid": user_data["uid"]
    }
    res = requests.get(url=url, params=data)
    print(res.url)
    data = json.loads(res.text)["data"]
    match_obj = re.match(r'(.*)uidEnterFirst:(.*?)\\n.*', str(data), re.M | re.I)
    print(match_obj)
    if match_obj:
        room_data = match_obj .group(2).split("/")
        room_data.append(user_data["uid"])
        return room_data
    else:
        print("No match!!")


if __name__ == "__main__":
    # iPhone7Plus
    data1 = {
        "uid": "141746805669898",
        "hdid": "1883f0eecd52807b6dba124776639a327878b725",
        "sid": "1457430095",
        "ssid": "1457430095"
    }
    # iPhone14
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
        "hdid": "1bdee9da694b72ec57fcbe22e3b3aa9c",  # 华为P40
        # "hdid": "5ea259affc2808778420bca55666b374",  # 三星NOTE20
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

    room_data = get_hit_rule(data4)
    print(room_data)
    clear_cache(room_data)

