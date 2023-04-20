from django.db import connection
from django.shortcuts import render, HttpResponse, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from AccountManage import models
from AccountManage.utils.form import HDID
from AccountManage.utils.pagination import Pagination


def hdid_list(request):
    if request.method == "GET":
        form_list = HDID()
        data_dict = {}
        phone_name = request.GET.get("phone_name", "")
        if phone_name:
            data_dict["phone_name__contains"] = phone_name
        queryset = models.HDID.objects.filter(**data_dict).order_by("id")
        page_object = Pagination(request, queryset)
        page_queryset = page_object.page_queryset
        page_string = page_object.html()
        context = {
            "form_list": form_list,
            "form_data": page_queryset,
            "page_string": page_string,
            "search_data": phone_name
        }
        return render(request, "hdid_list.html", context)


@csrf_exempt
def hdid_add(request):
    """ 添加设备信息 """
    data = request.POST.copy()
    if not data["remark"]:
        data["remark"] = "/"
    if not data["zhuiwan"]:
        data["zhuiwan"] = "暂无"
    if not data["Yomi"]:
        data["Yomi"] = "暂无"
    if not data["YaYa"]:
        data["YaYa"] = "暂无"

    form = HDID(data)
    if form.is_valid():
        form.save()
        result = {"status": True}
        return JsonResponse(result)
    result = {"status": False, "error": form.errors}
    return JsonResponse(result)


def hdid_delete(request):
    hd_id = request.GET.get("hd_id")
    print(hd_id)
    models.HDID.objects.filter(id=hd_id).delete()
    result = {"status": True}
    return JsonResponse(result)


@csrf_exempt
def hdid_edit(request):
    """测试设别编辑"""
    hdid_id = request.GET.get("hd_id")
    row_object = models.HDID.objects.filter(id=hdid_id).first()
    print(hdid_id)
    if not row_object:
        result = {"stauts": False, "tips": "编辑失败"}
        return JsonResponse(result)

    data = request.POST.copy()

    if not data["remark"]:
        data["remark"] = "/"
    if not data["zhuiwan"]:
        data["zhuiwan"] = "暂未输入"
    if not data["Yomi"]:
        data["Yomi"] = "暂未输入"
    if not data["YaYa"]:
        data["YaYa"] = "暂未输入"

    form = HDID(data=data, instance=row_object)
    if form.is_valid():
        form.save()
        result = {"status": True}
        return JsonResponse(result)

    result = {"status": False, "error": form.errors}
    return JsonResponse(result)


def hdid_detail(request):
    """测试设备详情"""
    hd_id = request.GET.get("hd_id")
    print(hd_id)
    data_dict = models.HDID.objects.filter(id=hd_id).values("phone", "zhuiwan", "Yomi", "YaYa", "remark").first()
    print(data_dict)
    if not data_dict:
        result = {"status": False, "error": "未知错误"}
        return JsonResponse(result)
    result = {"status": True, "data": data_dict}
    return JsonResponse(result)
