# Generated by Django 4.1 on 2022-10-31 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccountManage', '0003_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_uid', models.CharField(max_length=128, verbose_name='测试账号UID')),
                ('account_YY', models.CharField(max_length=128, verbose_name='测试账号YY')),
                ('account_card', models.CharField(max_length=128, verbose_name='测试账号通行证')),
                ('account_pwd', models.CharField(max_length=64, verbose_name='测试账号密码')),
                ('account_belong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AccountManage.testerinfo', verbose_name='测试账号归属')),
            ],
        ),
    ]
