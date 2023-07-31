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


cookie = "JSESSIONID=CF24BADCBED7084FF97FBE3A5AD4E597; Hm_lvt_f9ce0a3597664e1a306fa069969f2e69=1689589745; Hm_lpvt_f9ce0a3597664e1a306fa069969f2e69=1689589766; udb_c=; hd_newui=0.2632676869997579; hiido_ui=0.8866547699359595; yyuid=50047479; username=dw_wangchengqing; password=94E9CCD48155CF920E8EDA13F13A9F9DC64431BE; osinfo=C64664E3A6A4CAED9E1D2149EF426F528CEB5087; oauthCookie=; Hm_lvt_cdc8f428252cc07d59d8dc0d90181fcd=1688698550,1689216277; Hm_lpvt_cdc8f428252cc07d59d8dc0d90181fcd=1690785033; ab_sr=1.0.1_MmE4MDcxZjY5YjViMGExMzM2MGFjNmM4MmM4ZGM1YWI4M2Y3MGE5MTgzZGZhYjlmNzQ1Mjk3NjJjYjY1MjMxMTE0NzlhNGEzYTZiNDAzZjhkYWRhY2ZlYjgwODkxNTQzYjZiMGJkNzllZTI1NzNmOGI2MmZhODgxNTFiODAxY2U1MWRjMzc4YTI3ZWEwMDRkODgwYTU4MDlmYTcxZDYzZQ==; udb_oar=644118F8D797B2C3DB23954C5694393065EE617E5C6663B36072633757DA9200A0164EA20B3109C8314BC1012C4080725BEF6606ADB956BB92E3A2DE03455B401D3C56C08252887677C1C4617B0522DDE3327798FFA856F3B6153AD4CBCB9C7F389C8916A46A39B228167E46FA4A2E3A3D443D978E434C134EB02E205416EBC75E2B1D41632E5BE143D2272EE3B4FAD8E3A8075F1A5AE8F0C158EB2EB2A69F7A4194E5498962AF044A10FDD8D7193D8A629A133AD2C61235E1304D10C73DF4C15BCC1C1BE21DE563EF9D8C5309D924AEAC5BDF4F0C8FB8C1FF000FB8B5EAF0FFA477309BDEE4A7EE2472C746B624EDE84B7C9E70D45DE8C88663FFC331F65B344AEB06832B8A0B7E9931121984EBECAED34319B7EB059E83A5DCF8E3B7760DE5190DE7A11334903C9E21ACB3FA62D4ABA16AC8F67F0D9691718BDA81ED57BC68503E23DB0D38A3C1E384E09610619140CB20685F8FC1E9867891A466C27E6BA2A2CD9751AE26DBE9B624E621222E531C7CFB691FC7B8E84D53CB39E6D6030E6D; yadmin_token_test=39549799d27a43a5a4d08d415312235b"


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
    print(uid, nums, gift_list)
    gift_list = gift_list.split(",")
    print(uid, nums, gift_list)

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
