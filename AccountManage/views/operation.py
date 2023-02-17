import requests, json

from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from AccountManage import models


def operation_list(request, aid):
    print(aid)
    account_data = models.Account.objects.filter(id=aid).first()

    return render(request, "operation_list.html", {"account_data": account_data})


cookie = "hd_newui=0.6508860464612294; hiido_ui=0.984833494616951; sysop_privilege_user_id=50047479; sysop_privilege_global_user_id=50047479; ab_sr=1.0.1_N2I3ODRlMWZkMjMwODAxYTFmMDQxNTM0YTc0Yjg3ZmY4M2FmZWJlYjI1NWZjMWVmZDkxNjZiMWJlZWEwODM3OWQxMjJlZDk1MjY1MTBiNWE1MDUwOTY2MjdjODNhNDgwMjAyMmMxZDg1Yzc0M2Y0NDhmM2ZlY2M4OTUwNDNjOGE5YWFkMWI2MDFiOGFlMGMxODgyMzJlOWQwOTc2NzI0OA==; udb_c=; yyuid=50047479; username=dw_wangchengqing; password=D9ABF7FDAADE73B0ED90CE1173DB2286B1F0F5AA; osinfo=14A3D3B0CFE7978E0BEEEF5BDB81629240006E88; udb_oar=02904DEA496073F4A69DA83F5894EAD4EA64207DF6DEAAF8B6EB6F5340BCDD42CB1D7DECFAD6A86F3BB61678204356103E90D10D64452A748459961C18F6E7825E80641336274A016EAC49E284B8D9D6A77F5495DE8FA3C811F323F221DB42B598E4F8F36E1BC4D3CE6AA7C97A8622F535FFA1D976ABAAA664C44F4E62BB8CBA4623D5FAA8313D3FC07E1D608235F42DD6CD9C80A66418BE9351B239871CC296B279ED6ACDCCEE57AAD2508E0789DC5C6F81A5DA0B54A0C95094F16CE39B986B09ADB78415C516DF1F1FC465A4EB4C4320FC4725EB463D8B06904E44AD93C9A40C991CC374D4560D7C959A3A710E0F7EA6BEFE931DD8C12D4D2CD4C2096D5DFB76543F7D788721C39DD204D12596760E92E25E735FE192FCDD18949B16CF975770ED715D6AC1AC3876B60E4EF21AEBC056F6AB91A920B45E6C82C4C3AA09712E65470A64D5868C951296AF3CC5DFBC9AED34CDEAC2AF20BAEE6528C26D9D828378BF9E70100BCEF434DFC4BAC2495F31587796A4F9AE359498BBA9BA162B20A3"


@csrf_exempt
def operation_new_account(request):
    print(request.POST)
    hdid = request.POST.get("hdid")
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
        param = {"uid": uid, "amount": quota, "description": "test", "currencyType": 68, "appid": 58, "countryCode": "cn"}
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
