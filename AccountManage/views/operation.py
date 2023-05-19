import time

import requests, json, threading, mysql.connector

from openpyxl import *

from django.db import connection
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, FileResponse

from AccountManage import models


def operation_list(request, aid):
    print(aid)
    account_data = models.Account.objects.filter(id=aid).first()
    phone_data = models.HDID.objects.filter().values("id", "phone")
    print(phone_data)
    result_data = {
        "account_data": account_data,
        "phone_data": phone_data
    }
    return render(request, "operation_list.html", result_data)


cookie = "hd_newui=0.3709373329860539; Hm_lvt_c493393610cdccbddc1f124d567e36ab=1683283379; hiido_ui=0.8475475681936762; _ga=GA1.2.1811866272.1683537797; ab_sr=1.0.1_Y2FkOTA5NzUzZTMzMTYzOWM5NjZiMzY5Njk2MTUwYzkzMjJkM2FiYWQ4YWY2ODJkNGIwZjIxZDJlNjkwNTJmNmU2ZjFhZDQxZTMxZWI0YjhlZWQ4M2JmY2E0YTFjZjg2OGIwODMxYmY0Yzc3YTU4MzZhM2UwMzdkN2Y1NzcxYmJiZTA3Yzg3NTZiNGJjZGI4ZDdhY2Y2MWFmNzU1Mzc5Zg==; udb_c=; yyuid=50047479; username=dw_wangchengqing; password=01B3085E325E6B5EA973041ABB0C14A31E99D810; osinfo=3A8103E9D3647D66A73D79D32FC105DDD4E2F573; udb_oar=6A8BA5FA78C047484697A34FD34F7C794193C9BE2040919A97E085CD86D30A06D847146012A2D05B82E33007A2441FF2EF24DE59FB27B7E8D48CAC29CFC6FC702A1B44E3E13E6AE3C21ADD0C4DE10E345E08167E10EEC2F87B333F4271B526FD6DE9B9DA78B0D4BC4B621287710E2D763D55BCBD28DBB3CE97A83D05DD108D0A24F0B85B796EE61285E1AB354735B5664F96EE56C675EDFC0044E1F2D2A2BC33DCFA8AE78F583071E0483D30C3F5B7558857BDB34C7DB9F9E1C8E196241B5B8216ECD3C33DC153A6296DDC7924C009F4AF3E4E3091AC6512CADA4A00AC28E71104CBA6F2013B6F691719FFA42855C9DB47B04DD12C1FA106DB6F79C20FF027B31A72DDF0BC38B564BC367C17C7D52CA201F1711FAEAB5A3B43D085F41470C8D9CCA38BE6663F2B6E4E91B7679EF0422C72DAD8E1D1EBF4E4A0033CAA22F1720E46B94B0056D46774C4F256AD09CEBF7DC91CFA3002A05F1172F69A77663B85A282A9E3998E42D5BCC820D27489E2C5E8C11A121AD8D6D09E830F16E02B849CC7"


@csrf_exempt
def operation_new_account(request):
    """ 设置为新账号 """
    print(request.POST)
    hd_id = request.POST.get("hdid")
    hdid_data = models.HDID.objects.filter(id=hd_id).values("Yomi", "zhuiwan", "YaYa").first()
    app = request.POST.get("app")
    uid = request.POST.get("uid")
    env = request.POST.get("env")
    hdid = hdid_data[app]
    if hdid:
        header = {
            "cookie": cookie
        }
        param = {
            "uid": uid,
            "hdid": hdid,
            "app": app.lower()
        }

        url = "https://zhuiya-test.yy.com/web/reset/internal/resetUserFirst"
        if env == "official":
            url = "https://zhuiya.yy.com/web/reset/internal/resetUserFirst"
        res = requests.get(url=url, headers=header, params=param)
        print(res.url)
        print(json.loads(res.content))
        if res.content:
            return JsonResponse(json.loads(res.content))
    result = {"status": False, "error": "hdid不能为空"}
    return JsonResponse(result)


@csrf_exempt
def operation_balance(request):
    """ 添加货币 """
    print(request.POST)
    appid = request.POST.get("appid")
    quota = request.POST.get("quota")
    uid = request.POST.get("uid")
    print(appid, quota, uid)
    if not quota or quota == '0':
        result = {"status": False, "error": "请输入正确的充值额度"}
        return JsonResponse(result)
    if appid == '1':
        url = "http://turnover-bg-test.yy.com/yb/transfer_yb"
        param = {"yyuid": uid, "money": quota}
        res = requests.get(url=url, params=param)
        print(res.url)
        print(res.content)
        return JsonResponse(json.loads(res.content))
    if appid == '2':
        url = "http://turnover-bg-test.yy.com/addCurrency"
        param = {"uid": uid, "amount": quota, "description": "test", "currencyType": 1, "appid": 2, "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        result = json.loads(res.content)
        print(res.url)
        print(res)
        print(result)
        return JsonResponse(result)
    if appid == '34':
        url = "http://turnover-bg-test.yy.com/addCurrency"
        param = {"uid": uid, "amount": quota, "description": "test", "currencyType": 68, "appid": 34,
                 "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        print(res.url)
        print(res.content)
        return JsonResponse(json.loads(res.content))
    if appid == '36':
        url = "http://turnover-bg-test.yy.com/addCurrency"
        param = {"uid": uid, "amount": quota, "description": "test", "currencyType": 1, "appid": 36,
                 "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        print(res.url)
        print(res.content)
        return JsonResponse(json.loads(res.content))
    if appid == '58':
        url = "http://turnover-bg-test.yy.com/addCurrency"
        param = {"uid": uid, "amount": quota, "description": "test", "currencyType": 68, "appid": 58,
                 "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        print(res.url)
        print(res.content)
        return JsonResponse(json.loads(res.content))


@csrf_exempt
def search_balance(request):
    """ 查询余额 """
    print(request.POST)
    appid = request.POST.get("appid")
    uid = request.POST.get("uid")
    print(appid, uid)
    if appid == '1':
        "http://turnover-bg-test.yy.com/yb/getYb?uid=2711372130"
        url = "http://turnover-bg-test.yy.com/yb/getYb"
        param = {"uid": uid}
        res = requests.get(url=url, params=param)
        print(res.url)
        print(res.content)
        return JsonResponse(json.loads(res.content))
    if appid == '2':
        url = "http://turnover-bg-test.yy.com/getCurrency"
        param = {"uid": uid, "currencyType": 1, "appid": 2, "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        result = json.loads(res.content)
        print(url)
        print(res)
        print(result["allAmount"])
        return JsonResponse(result)
    if appid == '34':
        url = "http://turnover-bg-test.yy.com/getCurrency"
        param = {"uid": uid, "currencyType": 68, "appid": 34,
                 "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        print(url)
        print(res.content)
        return JsonResponse(json.loads(res.content))
    if appid == '36':
        url = "http://turnover-bg-test.yy.com/getCurrency"
        param = {"uid": uid, "currencyType": 1, "appid": 36,
                 "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        print(url)
        print(res.content)
        return JsonResponse(json.loads(res.content))
    if appid == '58':
        url = "http://turnover-bg-test.yy.com/getCurrency65"
        param = {"uid": uid, "currencyType": 68, "appid": 58, "countryCode": "cn"}
        res = requests.get(url=url, params=param)
        print(res.url)
        print(res.content)
        return JsonResponse(json.loads(res.content))


@csrf_exempt
def reset_noble(request):
    """ 清除超神贵族等级 """
    print(request.POST)
    uid = request.POST.get("uid")

    url = "https://fts-test.yy.com/ecology_noble/clean_data"
    param = {
        "uid": uid,
        "cleanType": 0
    }
    res = requests.get(url=url, params=param)
    print(res.url)
    print(json.loads(res.content))
    return JsonResponse(json.loads(res.content))


@csrf_exempt
def reset_sign_log(request):
    """ 清除签到 """
    signDate = str(request.POST.get("date")).replace("-", "")
    uid = request.POST.get("uid")
    app = request.POST.get("app")
    print(signDate, uid, app)
    url = "https://zhuiya-test.yy.com/web/test/public/sign/delete?type=6"
    data = {
        "signDate": signDate,
        "app": app.lower(),
        "uid": uid
    }
    res = requests.get(url=url, params=data)
    print(res)
    print(res.url)
    print(json.loads(res.content))
    if json.loads(res.content)["result"] == 0:
        return JsonResponse(json.loads(res.content))
    return JsonResponse(json.loads(res.content))


@csrf_exempt
def add_all_balance(request):
    account_belong_id = request.POST.get("account_belong_id")
    all_qute = request.POST.get("allQute")
    all_coin = request.POST.get("allCoin")
    print(account_belong_id, all_qute, all_coin)
    with connection.cursor() as cursor:
        sql = "SELECT `accountmanage_account`.`account_uid` FROM `accountmanage_account` WHERE account_belong_id = '{}';".format(
            account_belong_id)

        # print(sql)
        cursor.execute(sql)
        sql_data = cursor.fetchall()  # 获取一条数据, 使用fetchone()
        # print(sql_data)
        uids = ""
        for value in sql_data:
            uids += value[0] + ","
        print(uids)

        url = "http://turnover-bg-test.yy.com/batchAddCurrency"
        data = {
            "uids": uids,
            "amount": all_qute,
            "description": "test",
            "currencyType": 1,
            "appid": 2,
            "countryCode": "cn"
        }
        res = requests.get(url=url, params=data)
        print(res.text)
        print(res.status_code)
        if res.status_code == 200:
            result = {"status": True, "res": json.loads(res.text)}
            return JsonResponse(result)

        result = {"status": False, "res": res.text}
        return JsonResponse(result)


@csrf_exempt
def add_select_gift(request):
    uid = request.POST.get("uid")
    nums = request.POST.get("selectNums")
    gift_list = request.POST.get("giftList")
    data = request.POST
    print(data)
    print(uid, nums, gift_list)
    print(gift_list.split(','))

    result = {"status": True}
    return JsonResponse(result)


@csrf_exempt
def uid_add_gift(request):
    nums = request.POST.get("allNums")
    uid = request.POST.get("uid")
    gift_list = request.POST.get("giftList")
    print(uid, nums, gift_list)
    gift_list = gift_list.split(",")
    print(uid, nums, gift_list)

    mydb = mysql.connector.connect(
        host="125.94.240.75",  # 数据库主机地址
        port=8066,
        user="*dw_dingyong2@turnover_test@fix",  # 数据库用户名
        passwd="AMhDwC9xSK41OkLn427gC2MQ",  # 数据库密码
        database="turnover"
    )
    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT a.id,b.pricing_id FROM tb_to_props_meta a JOIN tb_to_props_consume_rec b ON b.prop_id=a.id WHERE a.app_id=2 AND b.currency_type=1 GROUP BY b.prop_id ")

    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    # print(myresult)
    # print(len(myresult))
    final_gift_list = []
    if gift_list[0]:
        for num in myresult:
            if str(num[1]) in gift_list:
                final_gift_list.append(num)

        # 定义为 run() 方法传入的参数
        data = {"data": final_gift_list, "uid": uid, "nums": nums}
        print(data)
    else:
        data = {"data": myresult, "uid": uid, "nums": nums}
        print(data)
    # 创建子线程
    use_threading(data)

    result = {"status": True}
    return JsonResponse(result)


def get_gift_list(request):
    mydb = mysql.connector.connect(
        host="125.94.240.75",  # 数据库主机地址
        port=8066,
        user="*dw_dingyong2@turnover_test@fix",  # 数据库用户名
        passwd="AMhDwC9xSK41OkLn427gC2MQ",  # 数据库密码
        database="turnover"
    )
    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT a.id,b.pricing_id,a.name FROM tb_to_props_meta a  JOIN tb_to_props_consume_rec b  ON b.prop_id=a.id WHERE a.app_id=2 AND b.currency_type=1 GROUP BY b.prop_id")

    myresult = mycursor.fetchall()  # fetchall() 获取所有记录

    result = {"status": True, "data": myresult}
    return JsonResponse(result)


def schedule(request):
    return render(request, "schedule.html")


@csrf_exempt
def schedule_operate(request):
    file_object = request.FILES.get("excSchedule")
    sname = request.POST.get("sheetName")
    print(type(file_object))
    print(file_object, sname)

    execl_op = Execl_Op(file_object, sname)
    execl_op.del_flsh_rows_cols([2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 21, 26, 27, 28, 29, 30])

    execl_op.create_sheet()

    return render(request, "schedule.html")


class Execl_Op:
    # 绑定
    def __init__(self, fname, sname):
        self.fname = fname
        self.wb = load_workbook(self.fname, data_only=True)
        self.ws = self.wb[sname]

    def del_flsh_rows_cols(self, cold):  # 基于文件名和表格名删除一些行和一些列
        """基于文件名和表格名删除一些行和一些列
        要删的行序数放在rowd表格中，要删的列序数放在cold表格中
        本程序的关键是删除的行或列序数都必须是从大的开始删除，这样才不会乱序"""
        # rowd = sorted(rowd, reverse=True)
        cold = sorted(cold, reverse=True)
        # for r in rowd:
        #     ws.delete_rows(r)
        for c in cold:
            self.ws.delete_cols(c)
        self.wb.save(self.fname)  # 记得要保存。

    # 获取某列所有值
    def get_col_value(self, column):
        rows = self.ws.max_row
        column_data = []
        for i in range(1, rows + 1):
            cell_value = self.ws.cell(row=i, column=column).value
            column_data.append(cell_value)
        return column_data

    # 获取某行所有值
    def get_row_value(self, row):
        columns = self.ws.max_column
        row_data = []
        for i in range(1, columns + 1):
            cell_value = self.ws.cell(row=row, column=i).value
            row_data.append(cell_value)
        return row_data

    def create_sheet(self):

        # 创建一个excel工作簿
        wb = Workbook()

        # 可以通过参数来指定sheet位置,0表示第一个
        first_sheet = wb.create_sheet("Android分支测试进度", 0)

        for i in range(1, 2):
            first_sheet.append(self.get_row_value(1))

        # sheet可以通过append来添加一行(row)
        for i in range(2, self.get_col_value(11).index('iOS') + 1):
            first_sheet.append(self.get_row_value(i))

        first_sheet = wb.create_sheet("iOS分支测试进度", 1)

        for i in range(1, 2):
            first_sheet.append(self.get_row_value(1))

        for i in range(self.get_col_value(11).index('iOS') + 1, self.get_col_value(11).index(None) + 1):
            first_sheet.append(self.get_row_value(i))

        wb.save('/TesterAccount/AccountManage/static/excel/schedule.xlsx')
        wb.close()


class my_Thread(threading.Thread):
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


def use_threading(data):
    mythread = my_Thread(data)
    # 启动子线程
    mythread.start()
    # 主线程执行此循环
    for i in range(len(data["data"])):
        print(threading.current_thread().getName())
