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


cookie = "hd_newui=0.6742548609320695; hiido_ui=0.7209432742384059; CHrt_ed28_saltkey=E0lQ0W7A; CHrt_ed28_lastvisit=1681796607; _ga=GA1.2.122252118.1681972843; CHrt_ed28_visitedfid=214D215D219D218D232; CHrt_ed28_ulastactivity=bb6c5fso5SA1xroC7bGPknamFB46iFjJ8CImtZdpvi3Z/pisT0fB; CHrt_ed28_auth=da86ZPV+3y4N+WvIaKgqcQQERsMv4SxoVnxJ4Ff0T/KNbSGY9KBwJqAbRKVdB0Gbp3lQbAZBmTXKsWDX/b7Bnv510fec; CHrt_ed28_lastcheckfeed=1119973|1681975034; CHrt_ed28_smile=4D1; CHrt_ed28_forum_lastvisit=D_232_1681800302D_218_1681800520D_219_1681800642D_215_1681874102D_367_1681876468D_214_1681975079; ab_sr=1.0.1_NGZlM2FlODU5ODg4ODdlMzBiZTQ4ZjE4NmUwMzVkODkzNzQwNTA1MWEwOWViZjlkZDVjZmFjYWI0MDJkZTU4NGRmNTQ4NmNkZDAyZDNhY2I4Mzk2ZTg5YzAzNjhmYjJiOTY0YmI5Mjc4NWNjMjU3MmZhYmI5ZGIyMjljNDcxYzdhMDEzZWIwZDdiMDBlZGE2NWM5N2U4ZjkyNWE3ZTI0NQ==; udb_c=; yyuid=50047479; username=dw_wangchengqing; password=33B5307CFFB612A87AB12F0345C75402241AB093; osinfo=2D2760C9214D7E5472884C2D9B1F41DC4AC9E396; udb_oar=75686C82A0287C6860F114BFFC303F15564DB4A108721DECFD34F0A447ACE65180866CC84C0C804B2C339D0CAD359060347D8EE61C2AD087344FD8FDEF3335B0664031BCF409DC58CD6AD6A4DF417B5D1A0F9FB27DF305E4EEA2BEACD24B5006B046AD842FA469708E7AC5CED68AFCBE14C614291D7DBFE5629939B38CDFB0633F1F3A38A5A11773AC02ABAFC356B033DECF6A5B73D5DEA1D131EB07B0A28457C4EB0FDC87BF7D8F341E897523F88C46D5EA2AB24BEB390FB3F2C00A393DB06310FAEA2247AE7A8CDAF93030E99F33868F6C004B8B188C38FAC1D8B9955E4E37726350E530F2D7226F21E50A5520602591507D96937ED03B2F4B9E59715A6453673C1E22AB7802A04E3F15A3F626C49E229C9E02018BC3A61F936471C9CF1CD0D0CFB7F6D96966D071EC1F206A3BEE5D8B0051D21B86796FE820AEB7C672FA772CCF7D45DCEC227B55581D783BF14AC6731860B529626C6F84F7A3BCDAE93EF7D8E5E33FF1188684623B10F53B22FE91BC6C4F196D4356E144A14843468A09A1"


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
    execl_op.del_flsh_rows_cols([2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 26, 27, 28, 29, 30])

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
        for i in range(2, self.get_col_value(12).index('iOS') + 1):
            first_sheet.append(self.get_row_value(i))

        first_sheet = wb.create_sheet("iOS分支测试进度", 1)

        for i in range(1, 2):
            first_sheet.append(self.get_row_value(1))

        for i in range(self.get_col_value(12).index('iOS') + 1, self.get_col_value(12).index(None) + 1):
            first_sheet.append(self.get_row_value(i))

        wb.save('/TesterAccount/AccountManage/static/excel/schedule.xlsx')
        wb.close()
