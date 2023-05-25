import threading, requests


class MyThread(threading.Thread):
    def __init__(self, data=None):
        threading.Thread.__init__(self)
        self.add = data

    # 重写run()方法
    def run(self):
        for arc in self.add["data"]:
            # 调用 getName() 方法获取当前执行该程序的线程名
            # print(threading.current_thread().getName() + " " + str(arc))
            self.add_gift(uid=self.add["uid"], prop_id=arc[0], pricing_id=arc[1], nums=self.add["nums"])

    def add_gift(self, uid, prop_id, pricing_id, nums):
        url = "http://turnover-bg-test.yy.com/props/addProps/2"
        data = {
            "propId": prop_id,
            "pricingId": pricing_id,
            "uid": str(uid),
            "nums": nums,
            "countryCode": "cn"
        }
        response = requests.get(url=url, params=data)
        print(response.text)

    def use_threading(self, data):
        mythread = MyThread(data)
        # 启动子线程
        mythread.start()
        # 主线程执行此循环
        for i in range(len(data["data"])):
            print(threading.current_thread().getName())
