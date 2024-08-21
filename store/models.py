from django.db import models
from django.contrib.auth.models import User


class StoreType(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=100, verbose_name='类型名')
    description = models.TextField(verbose_name='描述')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = '商品类别'


class Store(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=100, verbose_name='商品名')
    store_type = models.ManyToManyField(StoreType, verbose_name='商品类别')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='售价')
    manufacturer = models.CharField(max_length=100, verbose_name='厂家')

    def __str__(self):
        types_titles = ', '.join([item.title for item in self.store_type.all()])
        return f'title: {self.title}, value: {self.value}, manufacturer: {self.manufacturer}, types: {types_titles}'

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
