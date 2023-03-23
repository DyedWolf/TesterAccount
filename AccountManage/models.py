from django.db import models


class Admin(models.Model):
    """管理员"""
    username = models.CharField(max_length=32, verbose_name="管理员账号")
    password = models.CharField(max_length=32, verbose_name="管理员密码")


class Department(models.Model):
    """部门"""
    depart_name = models.CharField(max_length=32, verbose_name="部门名称")

    # depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # depart是对象，输出对象时，通过__str__(self)定制显示内容，（重写call方法

    def __str__(self):
        return self.depart_name


class TesterInfo(models.Model):
    """测试人员信息"""
    tester_name = models.CharField(max_length=64, verbose_name="测试人姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
    # age = models.IntegerField(verbose_name="员工年龄")
    # account = models.DecimalField(verbose_name="账号余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")  # DateTimeField
    # gender_choices = ((1, "男"), (2, "女"))
    # gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1)
    # 级联删除
    depart_name = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE,
                                    default="互动直播测试小组")
    """" # 置空
    depart = models.ForeignKey(to="Department", to_field="id", null=True,  blank=True, on_delete=models.SET_NULL)
   """

    def __str__(self):
        return self.tester_name


class Account(models.Model):
    account_belong = models.ForeignKey(verbose_name="测试账号归属", to="TesterInfo", blank=True, on_delete=models.CASCADE)
    # account_nick = models.CharField(max_length=64, verbose_name='测试账号昵称')
    account_uid = models.CharField(max_length=128, verbose_name="测试账号UID", null=True)
    account_YY = models.CharField(max_length=128, verbose_name="测试账号YY", null=True)
    account_card = models.CharField(max_length=128, verbose_name="测试账号通行证", null=True)
    account_pwd = models.CharField(max_length=64, verbose_name="测试账号密码", null=True)
    account_remarks = models.CharField(max_length=128, verbose_name="备注", null=True)


class HDID(models.Model):
    phone = models.CharField(max_length=64, verbose_name="测试机")
    zhuiwan = models.CharField(max_length=64, verbose_name="追玩", null=True)
    Yomi = models.CharField(max_length=64, verbose_name="Yo语音", null=True)
    YaYa = models.CharField(max_length=64, verbose_name="YaYa", null=True)
    remark = models.CharField(max_length=128, verbose_name="备注", null=True, default="")
