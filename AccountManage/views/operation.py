import time, re

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


cookie = "hd_newui=0.2267517766883529; hiido_ui=0.21420199545666807; udb_c=; yyuid=50047479; username=dw_wangchengqing; ab_sr=1.0.1_MjQ0MzNjNzYwOWU2NDU3YWRiNTkyZWFhYWU0ODIzZTAzOTRkMjgyNzkzMWVlOTc2ZTE4ZGJmODdmYWNjZDcxYWViODFiMTU2MDFjNjcwZDE4N2MxYjE2ODBjNzJjZGRjN2YwMWNlNGZkZjBkYzhmY2VhZDFjYmIyZTBhODU4YmI4MTkyZmQyM2Q3NzM3NmNkZjZhOTMwMmYwMzkyOGNmMA==; password=DA5C45B4271708CD2749D7CE0BA6E3365B3A851F; osinfo=E11E514E249F7D66DF519F3FCEEB02ABB265AB49; udb_oar=42DCA0FD3DD2E2926DBD52FE8003A8267D5CBF342D0B990E13E925EC0E25E3EDDC7BB9D2DACCCD273130B5DF226E5253C723417A3922FB9E35843A2ECC96FC7806E91C1C7AE1E6FDC8E859B3F4401766950ADF89485B009C05623822F804853BAB63FD33BD44BCCFEEC016227F7EA85D336339309BBDC90C231422E7EE2779BE960565F188B05231942F27360D2701874801C339A93A9FEBA8EAFECFBC13EE991DA87B0A95CEDFB204B9A7E716BF79C5C84CA35E05BF13CDA76E5D86A7C2B2821ECEAB1FCCC02963DC985C395EAE458C9DF454BDBC04600EFCD32EDA3C743ACC24E5CADB22DCE9D6B68E527AC90A386ABB501BBBD27AEA2A32E661DC01B4B07C99B9F006B5028B1970F93AF42B7574BE74880E31694157987890ED2089E60332CE67C672EF44A0F6933A3FBB520442ABAB95E988AED15F459461308865BF26790ACC9A40A271F4922D0EAA42F80B3CAD9648F6F7C50BF92DE6A427279B4D7F6A16145840DE15D3B6AFA0DB16FAD73C815169BF5918F7800CBA3683F73249779C"


@csrf_exempt
def operation_new_account(request):
    """ 设置为新账号 """
    print(request.POST)
    hd_id = request.POST.get("hdid")
    hdid_data = models.HDID.objects.filter(id=hd_id).values("Yomi", "zhuiwan", "YaYa").first()
    print("hdid_data:{}".format(hdid_data))
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
        print("设置为新账号-res.url: {}".format(res.url))
        print("设置为新账号-json.loads(res.content): {}".format(json.loads(res.content)))
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
    type_value = 6
    if app.lower() == "pcyy":
        type_value = 8
    url = "https://zhuiya-test.yy.com/web/test/public/sign/delete"
    data = {
        "signDate": signDate,
        "app": app.lower(),
        "uid": uid,
        "type": type_value
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
    """ 批量加货币 """
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
    """ 给uid添加包裹礼物 """
    nums = request.POST.get("allNums")
    uid = request.POST.get("uid")
    gift_list = request.POST.get("giftList")
    gift_list = gift_list.split(",")

    print("uid:{}, nums:{}, gift_list:{}".format(uid, nums, gift_list))

    data = [(2, 1), (34, 68), (36, 1)]
    business = request.GET.get("business")
    status = []
    print("business: {}".format(business))
    for i in range(len(data)):
        if int(business) == data[i][0]:
            status = data[i]
    print("status: {}".format(status))

    mydb = mysql.connector.connect(
        host="125.94.240.75",  # 数据库主机地址
        port=8066,
        user="*dw_zhouhaihong@turnover_test@fix",  # 数据库用户名
        passwd="0PIXO58FR1I08ytEUcYrPWkN",  # 数据库密码
        database="turnover"
    )
    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT a.id,b.pricing_id,a.name FROM tb_to_props_meta a  JOIN tb_to_props_consume_rec b  ON b.prop_id=a.id WHERE a.app_id={} AND b.currency_type={} GROUP BY b.prop_id".format(
            status[0], status[1]))
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录

    final_gift_list = []
    if gift_list[0]:
        for num in myresult:
            if str(num[1]) in gift_list:
                final_gift_list.append(num)

        # 定义为 run() 方法传入的参数
        data = {"data": final_gift_list, "uid": uid, "nums": nums, "business": status[0]}
        print("部分礼物data:{}".format(data))
    else:
        data = {"data": myresult, "uid": uid, "nums": nums, "business": status[0]}
        print("全部礼物data:{}".format(data))
    # 创建子线程
    my_thread = MyThread()
    my_thread.use_threading(data)

    result = {"status": True}
    return JsonResponse(result)


def get_gift_list(request):
    """ 获取礼物列表 """
    mydb = mysql.connector.connect(
        host="125.94.240.75",  # 数据库主机地址
        port=8066,
        user="*dw_zhouhaihong@turnover_test@fix",  # 数据库用户名
        passwd="0PIXO58FR1I08ytEUcYrPWkN",  # 数据库密码
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
        "SELECT a.id,b.pricing_id,a.name FROM tb_to_props_meta a  JOIN tb_to_props_consume_rec b  ON b.prop_id=a.id WHERE a.app_id={} AND b.currency_type={} GROUP BY b.prop_id".format(
            status[0], status[1]))

    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    print("获取礼物列表myresult:{}".format(myresult))
    idData = []
    for i in range(len(myresult)):
        print("i:{}, myresult[i]:{}".format(i, myresult[i]))
        idData.append(myresult[i][0])
    print("idData:{}".format(idData))
    result = {"status": True, "data": myresult}
    return JsonResponse(result)


def schedule(request):
    return render(request, "schedule.html")


@csrf_exempt
def schedule_operate(request):
    """ 操作excel """
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


def get_hit_rule(user_data):
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/getHitRule"
    data = {
        "uid": user_data["uid"]
    }
    res = requests.get(url=url, params=data)
    print("res.url:{}".format(res.url))
    data = json.loads(res.text)["data"]
    match_obj = re.match(r'(.*)uidEnterFirst:(.*?)\\n.*', str(data), re.M | re.I)
    print("match_obj:{}".format(match_obj))
    if match_obj:
        room_data = match_obj.group(2).split("/")
        room_data.append(user_data["uid"])
        return room_data
    else:
        print("No match!!")


@csrf_exempt
def clean_room_cache(request):
    """ 清除进频道记录"""
    uid = int(request.POST.get("uid"))
    url = "https://zhuiya-test.yy.com/admin-web/robot/public/getHitRule"
    data = {
        "uid": uid
    }
    res = requests.get(url=url, params=data)
    data = json.loads(res.text)["data"]
    print("清除进频道记录的接口返回数据:{}".format(res.text))
    print("清除进频道记录的接口返回url:{}".format(res.url))
    match_obj = re.match(r'(.*)uidEnterFirst:(.*?)\\n.*', str(data), re.M | re.I)
    print("清除进频道记录的match_obj:{}".format(match_obj))

    room_data = match_obj.group(2).split("/")
    print("清除进频道记录的room_data:{}".format(room_data))
    if "null" not in room_data:
        url = "https://zhuiya-test.yy.com/admin-web/robot/public/clearCache"
        data = {
            "uid": uid,
            "sid": room_data[0],
            "ssid": room_data[1]
        }
        res = requests.get(url=url, params=data)
        print("清除进频道记录的res.text:{}".format(res.text))
        print("清除进频道记录的res.url:{}".format(res.url))
        return JsonResponse(json.loads(res.content))

    else:
        result = {"status": False, "error": "获取不到进频道记录"}
        return JsonResponse(result)
