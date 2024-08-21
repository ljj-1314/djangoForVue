# Generated by Django 5.0.7 on 2024-08-16 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('title', models.CharField(max_length=100, verbose_name='类型名')),
                ('description', models.TextField(verbose_name='描述')),
            ],
            options={
                'verbose_name': '商品类别',
                'verbose_name_plural': '商品类别',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('title', models.CharField(max_length=100, verbose_name='商品名')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='售价')),
                ('manufacturer', models.CharField(max_length=100, verbose_name='厂家')),
                ('store_type', models.ManyToManyField(to='store.storetype', verbose_name='商品类别')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
    ]
