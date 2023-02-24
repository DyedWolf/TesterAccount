import requests, json

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


cookie = "hd_newui=0.16506903087708658; hiido_ui=0.2686670761989436; _ga=GA1.2.29981751.1676343893; udb_c=; _gid=GA1.2.825170573.1676861138; ab_sr=1.0.1_ZjI3NjM1YzUzZjBlY2IwNDg5YjM4MTRjMTg4MWM2ODRlNDAxNmZjMTNlZGFiN2U4ZWU2NzE3MzA0M2E0ZTE1OTAxYmUyMThjNTllNjBjNzk1MzI2NWIxYjdjNzg5ZjQ0ODllMTRiZDcyZjJhMjNhNWIwYjUwY2M2YmU0ZDk2NmUxNjM4NTFmMWYwZTBhMTNlNWU0MjI2NjcwYzc2NGI4Mw==; yyuid=50047479; username=dw_wangchengqing; password=3D2106A62C65842A5C198785032FE2FCE105B2D2; osinfo=BD0430E21C72C575BF54B9665AD85181B85A6459; udb_oar=0FDD169286299670B6825CE2A90255B06ED440F8D3E9C1EFF9391529E2F6B8E5F17A6AE4DFEB0789188C7A58D554350A24884538948E32DB7A5312ADBC2C9C543B209162E034AF11BDD12FE8341A758985C25F2360969D0837196748DA1FA80C67DD6748E7E0DAE902C54040A060DA469501A189931099231D61A10C789791008A91421F852900C6ED4EDF091AFEF17F11EC72D94409F1F7A3D9BBC53B80ECAF57D9C816F89E4A74E0268C943772087EC64332D448FBD683AF03A19BD547A0C65687EFEC7865B745286798178C039A38350092314EF71471C9E3A902105B31DB9FEBAE9D3F9DD5DBFC7C7A27A0423A679D09B740CC0E4792F015600BF7693C8F3161FDAF580EB492463C94F6EE6A23CA295A38E247650C1748433DBFB6F83D7DE265C7A4DA8FA616D59CBBE26BEE57448032576AE7A9E775A5FCE89627B2B19545AE73AA9BF4C95088E47B9795633871D2F0757C1C70E2189E27EF4D2F03AB3B90FBD867D21D46B00F0AD0C8FF52303AB66AB74CFA16FF0AF27BCD84F1E0F831"


@csrf_exempt
def operation_new_account(request):
    print(request.POST)
    hd_id = request.POST.get("hdid")
    hdid = models.HDID.objects.filter(id=hd_id).values("Yomi", "zhuiwan", "YaYa").first()
    print(hd_id, hdid)
    print(hdid["zhuiwan"])
    print(hdid["Yomi"])
    app = request.POST.get("app")
    uid = request.POST.get("uid")
    if hdid:
        url = "https://zhuiya-test.yy.com/web/reset/internal/resetUserFirst"
        header = {
            "cookie": cookie
        }
        param = {
            "uid": uid,
            "hdid": hdid,
            "app": app
        }
        res = requests.get(url=url, headers=header, params=param)
        print(res.url)
        print(json.loads(res.content))
        return JsonResponse(json.loads(res.content))
    result = {"status": False, "error": "hdid不能为空"}
    return JsonResponse(result)


@csrf_exempt
def operation_balance(request):
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
