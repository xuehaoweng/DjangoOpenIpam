# Generated by Django 3.1 on 2022-10-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_ipam', '0003_auto_20221012_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='tag',
            field=models.PositiveSmallIntegerField(choices=[(0, '空闲'), (1, '已分配已使用'), (2, '保留'), (3, '未分配已使用'), (4, '已分配未使用')], default=0, verbose_name='状态'),
        ),
        migrations.AddIndex(
            model_name='subnet',
            index=models.Index(fields=['subnet'], name='subnet_idx'),
        ),
    ]
