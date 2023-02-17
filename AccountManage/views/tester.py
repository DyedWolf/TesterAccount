from django.shortcuts import HttpResponse, render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from AccountManage import models
from AccountManage.utils.form import TesterInfo
from AccountManage.utils.pagination import Pagination


def tester_list(request):
    """测试人员列表"""
    form_list = TesterInfo()
    data_dict = {}
    tester_name = request.GET.get('tester_name', '')
    if tester_name:
        data_dict["tester_name__contains"] = tester_name
    queryset = models.TesterInfo.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        "form_list": form_list,
        "form_data": page_queryset,
        "page_string": page_string,
        "search_data": tester_name
    }
    print(page_queryset)
    return render(request, "tester_list.html", context)


@csrf_exempt
def tester_add(request):
    """添加测试人员"""
    form = TesterInfo(data=request.POST)
    print(request.POST)
    if form.is_valid():
        form.save()
        result = {"status": True}
        return JsonResponse(result)
    result = {"status": False, "error": form.errors}
    return JsonResponse(result)


@csrf_exempt
def tester_edit(request):
    """编辑测试人员"""
    tid = request.GET.get('tid')
    row_object = models.TesterInfo.objects.filter(id=tid).first()
    print(tid)
    print(row_object)
    if not row_object:
        result = {"status": False, "tips": "编辑失败"}
        return JsonResponse(result)

    form = TesterInfo(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        result = {"status": True}
        return JsonResponse(result)

    result = {"status": False, "error": form.errors}
    return JsonResponse(result)


@csrf_exempt
def tester_delete(request):
    """删除测试人员"""
    tid = request.GET.get("tid")
    print(tid)
    models.TesterInfo.objects.filter(id=tid).delete()
    result = {"status": True}
    return JsonResponse(result)


def tester_detail(request):
    tid = request.GET.get("tid")
    print(tid)
    data_dict = models.TesterInfo.objects.filter(id=tid).values("tester_name", "depart_name", "password").first()
    if not data_dict:
        result = {"status": False, "error": "未知错误"}
        return JsonResponse(result)
    result = {"status": True, "data": data_dict}
    print(data_dict)
    return JsonResponse(result)
