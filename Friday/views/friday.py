import requests, json, os, time, threading


def push_message(app):
    url = "http://apiin.im.baidu.com/api/msg/groupmsgsend?access_token=d9e12b1d1c062222bcae98d593e42aff3"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "message": {

            "header": {
                "toid": [6960818]
            },
            "body": [{"type": "TEXT", "content": "{} 出新包了!".format(app)}]
        }
    }

    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    res.encoding = 'utf-8'
    print(res)
    return res.text


def get_android_app_count():
    path = '//repo.yy.com/dwbuild/mobile/android/zhuime/dreamer-android_1.14.0_yo_zwdev_feature/'  # 输入文件夹地址
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


def get_iOS_app_count():
    path = '//repo.yy.com/dwbuild/mobile/ios/Yomi/yomi_1.14.0_dev_feature/'  # 输入文件夹地址
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


# run函数
def run():
    before_android_num = get_android_app_count()
    before_iOS_num = get_iOS_app_count()
    timer = threading.Timer(60 * 15, run)  # 设置一个定时器，循环输出时间
    timer.start()  # 启动线程

    time.sleep(60 * 30)
    after_android_num = get_android_app_count()
    after_iOS_num = get_iOS_app_count()
    if before_android_num != after_android_num:
        print("android出新包了", before_android_num, after_android_num)
        push_message("android")
    elif before_android_num == after_android_num:
        print("没出新报", before_android_num, after_android_num)
    if before_iOS_num != after_iOS_num:
        print("iOS出新包了", before_iOS_num, after_iOS_num)
        push_message("iOS")
    elif before_iOS_num == after_iOS_num:
        print("没出新报", before_iOS_num, after_iOS_num)


if __name__ == "__main__":
    run()
