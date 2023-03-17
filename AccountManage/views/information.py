from django.db import connection
from django.shortcuts import render, HttpResponse, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from AccountManage import models
from AccountManage.utils.form import HDID
from AccountManage.utils.pagination import Pagination


def my_information(request):
    pass
