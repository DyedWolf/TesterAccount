from django.shortcuts import HttpResponse, render, redirect

from AccountManage import models
from AccountManage.utils.form import LoginForm


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        # form = LoginModelForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        # user_input_code = form.cleaned_data.pop("code")
        # code = request.session.get("code_string", "")
        # print(user_input_code, code)
        # if user_input_code.upper() != code.upper():
        #     form.add_error("code", "验证码错误")
        #     return render(request, "login.html", {"form": form})

        tester_object = models.TesterInfo.objects.filter(**form.cleaned_data).first()
        print("tester_object:{}".format(tester_object))
        if not tester_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        request.session["info"] = {"id": tester_object.id, "name": tester_object.tester_name}
        print("登录者的信息：{}".format(request.session["info"]))
        request.session.set_expiry(60 * 60 * 24 * 7)
        if tester_object.id == 11:
            return redirect("/recommend/")
        else:
            return redirect("/account/list/")
    return render(request, "login.html", {"form": form})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/login/')


def try_loading(request):
    return render(request, "try_loading.html")