import requests, json, pymongo

from django.db import connection
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

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


cookie = "udb_c=; hd_newui=0.9862089992719061; hiido_ui=0.7456936830136831; osinfo=3E530F41DA01E8A3D22EB4880B3B1021E0607174; ab_sr=1.0.1_OTQxNjFhYWU1MGY3MGZmMmQzMTg4NzVkZjg0ZGM1OTlmYzhmOWFiYTgyZmQ5ZTRkNmRkNTU2N2Y3MzlmN2Y5M2U4MWEyYzVjM2M5OGI3ZWY1ZWM0OTI2NGVkYmU0OGJkODUwZGQwZWM4M2E5YTlkZmRhYTA0NTRlNWVlNDZmNzM0YzUwZTY0MGFmN2VlZTRhYjY0YjFjZDlmMTI5ZTcxMg==; yyuid=50047479; username=dw_wangchengqing; password=17BDE1FD368AB0B164FA5BF0EA297B85EE4C0324; udb_oar=1651F9D2DEE56EFAC2024C862CA921EF6EE209F766907F5880E48C065BBCC2CD0BFE86B49A7331BEEEF4689B773F197312525472F9350A8B6C6668F6CFD9F96E2B38162CF31133A611F9EE46850B7C8F7C724CEF2A7DCF0A79A90DAC195DB47AE4F779E41CC7932F55E8B851A0D6B03F21E1C4D3458E365CDCF7634DB8517CBB023ECE983833533BE982628432A6945ADED091C6FE1219F5C691CAB0F6BC8444815719B45AAF351498807A36990647C32F7E4CFECECE85CDAABC061392B4E7A068F9FDBC8A0CA14C8710042380F44C53C6FC3DE9E01003E345F1E655D25AA06D88459567FB83DAF29DDFBB44535522CC7F5551889C96DFC232160CA228A3FAA4400C5AB907CC1C20E959603CB45A462AA5B1F57122D28FCB5F92C1B40002E2097C0929E370F146A5BE00689848DC2CE743428B8FA7CFA916D1EA7235A09823EB026F49F655FEE2F1ACAD3085D499E6C81AF160A2FEBB4164F5A1713A760B66B4B24566E77A5078E4231A80A28640FB14E12815D6886616CED9223BDC7226EA7D"


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
