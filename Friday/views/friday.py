import requests,json


def push_message():
    url = "http://apiin.im.baidu.com/api/msg/groupmsgsend?access_token=d9e12b1d1c062222bcae98d593e42aff3"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "message": {

            "header": {
                "toid": [6960818]
            },
            "body": [{"type": "TEXT", "content": "王木木真可爱!"}]
        }
    }

    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    res.encoding = 'utf-8'
    print(res)
    return res.text


def inflow_robot():
    webhook = "http://apiin.im.baidu.com/api/msg/groupmsgsend?access_token=d00711dbba0fa8cd350257efc3e2723fb"
    headers = {'content-type': 'application/json'}  # 请求头
    data = {
        "message": {
            "header": {
                "toid": [6960818]
            },
            "body": [
                {
                    "content": "asdf",
                    "type": "TEXT"
                }
            ]
        }
    }
    r = requests.post(webhook, headers=headers, data=json.dumps(data))
    r.encoding = 'utf-8'
    return r.text

if __name__ == "__main__":
    push_message()