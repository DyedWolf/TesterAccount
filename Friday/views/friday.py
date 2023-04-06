import requests, json, os, time, threading


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
            "body": [{"type": "TEXT", "content": "王承庆快可以走了!"}]
        }
    }

    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    res.encoding = 'utf-8'
    print(res)
    return res.text


def get_app_count():
    path = '//repo.yy.com/dwbuild/mobile/android/zhuime/dreamer-android_1.13.0_yo_maint/'  # 输入文件夹地址
    files = os.listdir(path)  # 读入文件夹
    num_png = len(files)  # 统计文件夹中的文件个数
    return num_png
    # print("打印文件个数:{}".format(num_png))
    # if app_account[0] != int(num_png):
    #     print("出新包了", app_account)
    #     app_account.clear()
    #     app_account.append(num_png)
    # if app_account[0] == int(num_png):
    #     print("没出新报", app_account)
    # 输出所有文件名
    # print("所有文件名:")
    # for file in files:
    #     print(file)


app_account = []


# run函数
def run():
    before_num = get_app_count()
    app_account.append(before_num)
    timer = threading.Timer(60 * 15, run)  # 设置一个定时器，循环输出时间
    timer.start()  # 启动线程

    after_num = get_app_count()
    if app_account[-1] != after_num:
        print("出新包了", app_account, after_num)
    elif app_account[-1] == after_num:
        print("没出新报", app_account, after_num)


if __name__ == "__main__":
    run()
