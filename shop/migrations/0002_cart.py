# Generated by Django 2.0.4 on 2018-04-12 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('item', models.CharField(max_length=200, verbose_name='产品名称')),
                ('num', models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='数量')),
            ],
        ),
    ]
