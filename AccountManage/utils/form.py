from django import forms
from django.core.validators import ValidationError

from AccountManage import models
from AccountManage.utils.bootstrap import BootStrapModelForm
from AccountManage.utils.enctype import md5


class TesterInfo(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.TesterInfo
        fields = ["tester_name", "depart_name", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)

    def clean_confirm_password(self):
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        password = self.cleaned_data.get("password")
        # exists = models.Admin.objects.exclude(id=self.instance.pk).filter(
        #     username=self.cleaned_data["username"]).exists()
        if confirm_password != password:
            raise ValidationError("密码不一致")
        return confirm_password


class LoginForm(BootStrapModelForm):
    tester_name = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)

    class Meta:
        model = models.TesterInfo
        # fields = ["username", "password"]
        exclude = ["depart_name"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)


class Account(BootStrapModelForm):
    # upload = forms.CharField(label="上传文件", widget=forms.FileField)

    class Meta:
        model = models.Account
        # fields = "__all__"
        exclude = ["account_belong"]


class Upload(BootStrapModelForm):
    # upload = forms.CharField(label="上传文件", widget=forms.FileField)
    # bootstrap_exclude_files = ["upload"]
    # upload = forms.FileField(label="上传文件")

    class Meta:
        model = models.Account
        fields = ["account_belong"]


class HDID(BootStrapModelForm):

    class Meta:
        model = models.HDID
        fields = "__all__"
