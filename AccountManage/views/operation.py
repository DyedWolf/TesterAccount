import time

import requests, json, mysql.connector

from openpyxl import *

from django.db import connection
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from AccountManage import models
from AccountManage.utils.pthread import MyThread
from AccountManage.utils.excel_op import ExeclOp


def operation_list(request, aid):
    print(aid)
    account_data = models.Account.objects.filter(id=aid).first()
    phone_data = models.HDID.objects.filter().values("id", "phone")
    print("phone_data:{}".format(phone_data))
    result_data = {
        "account_data": account_data,
        "phone_data": phone_data
    }
    return render(request, "operation_list.html", result_data)


cookie = "JSESSIONID=206B7805C6503CC137B31C2141DDDEBD; Hm_lvt_f9ce0a3597664e1a306fa069969f2e69=1661497469; CHrt_ed28_saltkey=hJYOWg2g; Hm_lvt_cdc8f428252cc07d59d8dc0d90181fcd=1686798688,1687243560,1687658217,1687680687; yyuid=50047479; username=dw_wangchengqing; hd_newui=0.06322537892639568; hiido_ui=0.12445796011643617; JSESSIONID=node01b46ltkmwf1nnbbvhchrv7yal884264.node0; _ga=GA1.2.1556408309.1687836035; password=F245320C45CFE79286FC825C13C13710C0BFABAC; osinfo=2F75E9B720993EE7CAF80FF28918E21934C362F8; udb_l=; udb_n=; udb_c=; ab_sr=1.0.1_MTdhNmRjOTc4Nzk4ZWY5YWU5NDM1YjQ3MjNmYmM3YzZjZGMxZTAwM2E5OTkyNGE3MmVmYTI3OTUyMGNlZWIyNTExZDY5Zjk2YTM4NTRhMDdjNDBiYWNhY2Q2ZjFlODcwNWQ2MWM0ZjMzZjA0ZTUyNDljOGZjYzJlNzIxNTYwYzE0YzM5MWQ0MGM4M2VmODc2MjVmYjNhZjI0YzYxYjcxMA==; udb_oar=B9DBDEE3BF67F66D90546E1469BC4C174F41176DB3254761E877B0E77B69885E720258FFDB5AAAFCE6BBAFDDDC3BE25A8C6ACC4C6B444632AAF2EE986AAE494045BDE5CB4B2D928D0CB4C98489E05FF9D56B9772BAD1F4CC047B357F4A977142230B14A9DD46BD0B37FBA96AA60D44AD7D76DFD4927DC963C395FBB7E7457FF988E0AF856FD21657D5D5E6400EA33DEA4BCB9FEC73F4BC7D57A5524511953EAC76FD8EBC6B91B543A5D9228A43EB6A40998A8385600022F36A97CC5483374CB14AF809CE8D76EC4BA28FF78142F98F1478E67F229812E632FAC6F8B2A0486A7C8E475845A24917EFA0BAFCE594C6B3B7844648A6028DF58A7127DB55EF3283714041C4528A369A1BEEB2BC8EC1B4744602B1B1BCB4474E73E9D751273AE5AABFAC7ABA0E1B31E9DA60FA29E8D19B6167C868F19D7B4EC49F239D2DEFCC959BF1AE303616D4730DDC6C756C9AA6D3DB38717E9CA93EFB02E37C0F6EF47B9F959D556C5C8D59976594C4B34B2EEC6B4658FDB5045E458F8A5E6789AF4B405C3251; Hm_lpvt_cdc8f428252cc07d59d8dc0d90181fcd=1688349869"


@csrf_exempt
def operation_new_account(request):
    """ 设置为新账号 """
    print(request.POST)
    hd_id = request.POST.get("hdid")
    hdid_data = models.HDID.objects.filter(id=hd_id).values("Yomi", "zhuiwan", "YaYa").first()
    app = request.POST.get("app")
    uid = request.POST.get("uid")
    env = request.POST.get("env")
    # cookie = request.POST.get("webCookie")
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
    my_thread = MyThread()
    my_thread.use_threading(data)

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
    data = [(2, 1), (34, 68), (36, 1)]
    business = request.GET.get("business")
    status = []
    print("business: {}".format(business))
    for i in range(len(data)):
        if int(business) == data[i][0]:
            status = data[i]
    print("status: {}".format(status))
    mycursor.execute(
        "SELECT a.id,b.pricing_id,a.name FROM tb_to_props_meta a  JOIN tb_to_props_consume_rec b  ON b.prop_id=a.id WHERE a.app_id={} AND b.currency_type={} GROUP BY b.prop_id".format(status[0], status[1]))

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
    if file_object:
        execl_op = ExeclOp(file_object, sname)
        execl_op.del_flsh_rows_cols([2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 21, 26, 27, 28, 29, 30])
        execl_op.create_sheet()

        return render(request, "schedule.html")
    result = {"status": False, "error": "未上传excel"}
    return JsonResponse(result)
