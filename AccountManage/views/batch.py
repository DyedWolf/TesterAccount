import mysql.connector

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core.cache import cache

from AccountManage import models
from AccountManage.utils.pthread import MyThread


def batch_page(request):
    account_data = models.Account.objects.filter()
    result_data = {
        "account_data": account_data,
    }
    return render(request, 'batch_operation.html', result_data)


def search_gift(request):
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
    if not business:
        business = 2
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

    mycursor.close()
    mydb.close()


def get_gift_list(request):
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
    if not business:
        business = 2
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
    print("myResult:{}".format(myresult))
    cache.set('myResult', myresult, 200)
    print("cache.get('myResult'):{}".format(cache.get('myResult')))
    result = {
        "data": myresult,
        "status": True
    }
    mycursor.close()
    mydb.close()
    return JsonResponse(result)


@csrf_exempt
def uid_add_gift(request):
    """ 给uid添加包裹礼物 """
    nums = request.POST.get("allNums")
    uid = request.POST.get("uid")
    gift_list = request.POST.get("giftList")
    gift_list = gift_list.split(",")
    print("uid:{}, nums:{}, gift_list:{}".format(uid, nums, gift_list))

    data = [(2, 1), (34, 68), (36, 1)]
    business = request.POST.get("business")
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
    my_result_cache = cache.get('myResult')
    print("my_result_cache:{}".format(my_result_cache))
    final_gift_list = []
    if gift_list[0]:
        for num in myresult:
            if str(num[1]) in gift_list:
                final_gift_list.append(num)

        # 定义为 run() 方法传入的参数
        data = {"data": final_gift_list, "uid": uid, "nums": nums}
        print("data:{}".format(data))
    else:
        data = {"给uid添加包裹礼物的data": myresult, "uid": uid, "nums": nums}
        print(data)
    # 创建子线程
    my_thread = MyThread()
    my_thread.use_threading(data)
    mycursor.close()
    mydb.close()
    result = {"status": True}
    return JsonResponse(result)
