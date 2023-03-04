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


cookie = "hd_newui=0.16506903087708658; hiido_ui=0.2686670761989436; _ga=GA1.2.29981751.1676343893; ab_sr=1.0.1_MTMyNGE2MzRlNmE4ZGQ3MzVkNDk5ZDEyOGVjMGFjNTIwZGYxNzgzZjM5Njk3MGRjZjRmMTUxNWY3M2I0ZWE2MmMxZmQ1MTE5NTBmNWJjYjNhZGFkN2U0M2U2YzcwNzg2MWM2MWY2MmYwMmRiZGZhMmQ1NjZlNDVjZjA3MDNiZWQ0YjcyYjJhZjAwZTk3OGNmNTMyM2Y1YzhjODcxOWY0Nw==; udb_c=; yyuid=50047479; username=dw_wangchengqing; password=0771D09F6DAA17A46F3D2767DEC7ADF22CE98F20; osinfo=4B10F09D01FE6FA2754767E99FF907162DFA8083; udb_oar=07F813B54346815977F838E550F8CCC77CEC9612FBB9E97E4298828644BFF30D397B6B820744D09820C9331E169E1D6E14AB12C3F4F0ACD9D9237608F9EAE7F4491DAEEC428E303CC640439460BB62A8F3A5798110DAECDC002D71B491EE01EC8821FBE49E22E9B75F57F310AEBD16BA4473834FE097F694F05D42C0299E90F12D9204DFE834E1F035C7DBADA211AD5BB22727D22B6A832A81F1C7E192E4382E683D5F3EA5AB14AD2B2C89EAFF37E868CDE4C186497D5D5D420CE988A6B732663EE992E121CA00DA1E657DEDF92D4B46972AB5FB8E25A5C05F8E906E10389A1BE3F9CFD2B4280E63719EC3F867D080D7520FFFCA4AB744DC46BF9DA764E8B5CF26D4691B87BC3E6A9F246EB881342B7E676DE0EF79064BD2C920CBE25DC1581AE5336A2E396A9159ADDE1114CAB4C2D2F827562FC08EE29B37CB0CE1BBF0FFDF45CAB9DC4E2D4022D17977F7BB667A32D6B9C13F763961CC4E96B92B2D717F622EB0F4A8EE221E61EA6E5D7262993024ED178946E4C6950FF71F280B75D0DB37; _gid=GA1.2.1804574923.1677655641"


@csrf_exempt
def operation_new_account(request):
    print(request.POST)
    hd_id = request.POST.get("hdid")
    hdid_data = models.HDID.objects.filter(id=hd_id).values("Yomi", "zhuiwan", "YaYa").first()
    app = request.POST.get("app")
    uid = request.POST.get("uid")
    hdid = hdid_data[app]
    if hdid:
        url = "https://zhuiya-test.yy.com/web/reset/internal/resetUserFirst"
        header = {
            "cookie": cookie
        }
        param = {
            "uid": uid,
            "hdid": hdid,
            "app": app.lower()
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


@csrf_exempt
def reset_sign_log(request):
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
    print(res.url)
    print(json.loads(res.content))
    if json.loads(res.content)["result"] == 0:
        return JsonResponse(json.loads(res.content))
    return JsonResponse(json.loads(res.content))
