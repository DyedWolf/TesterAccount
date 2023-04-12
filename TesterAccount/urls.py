"""TesterAccount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AccountManage.views import tester, login, account, operation, hdid, information, recommend
from Friday.views import friday


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('sss/', account.cal),
    path('index/', account.index),

    # 登录
    path('login/', login.login),
    path('logout/', login.logout),

    # 我的信息
    path('my_information/', information.my_information),

    # 测试人员列表
    path('tester/list/', tester.tester_list),
    path('tester/add/', tester.tester_add),
    path('tester/delete/', tester.tester_delete),
    path('tester/edit/', tester.tester_edit),
    path('tester/detail/', tester.tester_detail),

    # 测试账号列表
    path('account/list/', account.account_list),
    path('account/multi/', account.account_multi),
    path('account/delete/', account.account_delete),
    path('account/detail/', account.account_detail),
    path('account/add/', account.account_add),
    path('account/edit/', account.account_edit),
    path('account/option/', account.account_option),
    path('download_excel/', account.download_excel),

    # 测试账号操作
    path('operation/<int:aid>', operation.operation_list),
    path('operation/newacc/', operation.operation_new_account),
    path('operation/addmoney/', operation.operation_balance),
    path('operation/search_balance/', operation.search_balance),
    path('operation/reset_noble/', operation.reset_noble),
    path('operation/reset_sign_log/', operation.reset_sign_log),
    path('operation/add_all_balance/', operation.add_all_balance),

    # 添加推荐uid和sid
    path('recommend/list/', recommend.recommend_list),
    path('recommend/', recommend.recommend),
    path('recommend/add_recommend_room/', recommend.add_recommend_room),
    path('recommend/add_recommend_uid/', recommend.add_recommend_uid),

    # 测试机HDID
    path('hdid/list/', hdid.hdid_list),
    path('hdid/add/', hdid.hdid_add),
    path('hdid/delete/', hdid.hdid_delete),
    path('hdid/detail/', hdid.hdid_detail),
    path('hdid/edit/', hdid.hdid_edit),


    # 分支测试进度表
    path('schedule/', operation.schedule),
    path('schedule/schedule_operate/', operation.schedule_operate),
    path('download_schedule/', account.download_schedule),
]
