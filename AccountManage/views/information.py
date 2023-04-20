from django.db import connection
from django.shortcuts import render, HttpResponse, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from AccountManage import models
from AccountManage.utils.form import HDID
from AccountManage.utils.pagination import Pagination


def my_information(request):
    account_belong_id = request.session["info"]["id"]
    print(account_belong_id)
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) FROM accountmanage_account WHERE account_belong_id ={}".format(account_belong_id)

        print(sql)
        cursor.execute(sql)
        sql_data = cursor.fetchone()  # 获取一条数据, 使用fetchone()
        print(sql_data[0])
        result = {
            "form_data": sql_data[0]
        }
    return render(request, "my_information.html", result)
