import time

import requests, json, pymongo

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


cookie = "CHrt_ed28_saltkey=E0lQ0W7A; CHrt_ed28_lastvisit=1681796607; CHrt_ed28_visitedfid=214D215D219D218D232; CHrt_ed28_ulastactivity=bb6c5fso5SA1xroC7bGPknamFB46iFjJ8CImtZdpvi3Z/pisT0fB; CHrt_ed28_auth=da86ZPV+3y4N+WvIaKgqcQQERsMv4SxoVnxJ4Ff0T/KNbSGY9KBwJqAbRKVdB0Gbp3lQbAZBmTXKsWDX/b7Bnv510fec; CHrt_ed28_lastcheckfeed=1119973|1681975034; hd_newui=0.060556767692634406; hiido_ui=0.8694076315662636; _ga=GA1.2.1463216810.1682563192; ab_sr=1.0.1_OGJlNDNjNTgwNWNlNjhiNWExODM4MjlkMDBiYWJiMzY0MjNjYzQyNThhNjhiOWZmNzFkZjAxOWU1ZjRmODBkYjExMWZiNzM4Y2JkMWExN2ZhYjZkMTA5ZTM3NTBhMDAyZTQ1YWNkNmJlZjM5M2Q4ZGM5YjMwNjQ2MmY2YTc0ZjlmNTIyYTg5Y2RlMTAxNjc1ZDAxNWExMzI2YmI3MWFmNw==; udb_c=; yyuid=50047479; username=dw_wangchengqing; password=73E974684B55BFDF04C573429ED667E541333C17; osinfo=AE91D768475EC96E931E0EE3DE26453E1B565DF6; udb_oar=04D36EBA30ABADAAE77C86BB40E163B3F121A72460641AB429A38DBB75F2AC9350BBA7786E7931724159BF2DC4745DD4ED83B70341D7098861B929D2BDCBEEB012306E9F34B82DBF3E9627FDA8E30EFC2E3F615031EA903CE743D730EC417822CC4D4904D2A12326C9746B27529958F2DA204FB7508F3AA7EBE8420642B12F615C143000771BF19FF363AB813F8B520D5B3222F9D189A9CCDF7773E848F6C8F38AB3FF27327CFC1CA8AD65E1F426EB94621B55B05820BC554236AD8BE95FE2C20F691059913D046D22D39A00F7495CDD39C87E251B0B61C0E5F1BA995DD7819FB22EF89141B7796CD739DA735140E888827D36EB30E4CA29E8C1C1630339B7A79D09040872C2B52F040081EF74ABFA93AAB20DB76180FBA9049CEA478EB6572A65332BD88D3743BC8C1931D7D6B6A3E42AD68CFFD9BAE72E5FDDA1F6DCBD8B4D4B2E1C4B1B7695A5764946C3211AB79A87BB271D58A78261253D92628B2880B70EA8D5A4333D7007F81BC87EE1B080CB039075789E3E281CB052733F7A5B38B3"


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
        sql = "SELECT `accountmanage_account`.`account_uid` FROM `accountmanage_account` WHERE account_belong_id = '{}' ".format(
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
