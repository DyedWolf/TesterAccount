# Generated by Django 4.1.2 on 2022-11-23 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountManage', '0008_alter_account_account_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_remarks',
            field=models.CharField(max_length=128, null=True, verbose_name='备注'),
        ),
    ]
