import threading

# 创建子线程类，继承自 Thread 类
import requests


class my_Thread(threading.Thread):
    def __init__(self, add):
        threading.Thread.__init__(self)
        self.add = add

    # 重写run()方法
    def run(self):
        for arc in self.add:
            # 调用 getName() 方法获取当前执行该程序的线程名
            print(threading.current_thread().getName() + " " + arc)
            self.add_gift(arc)

    def add_gift(self, arc):
        url = "http://turnover-bg-test.yy.com/props/addProps/2"
        data = {
            "propId": 20421,
            "pricingId": 1010452,
            "uid": arc,
            "nums": 1,
            "countryCode": "cn"
        }
        response = requests.get(url=url, params=data)
        print(response.text)





# 定义为 run() 方法传入的参数
my_tuple = ["2711427642", "2711372130", "2711581533"]
# 创建子线程
mythread = my_Thread(my_tuple, prop_id, pricing_id, nums)
# 启动子线程
mythread.start()
# 主线程执行此循环
for i in range(len(my_tuple)):
    print(threading.current_thread().getName())
