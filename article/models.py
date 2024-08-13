from django.db import models
from django.contrib.auth.models import User


class UserArticle(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=255, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户文章'
        verbose_name_plural = '用户文章'
        ordering = ['-createTime']  # 按创建时间降序排序

    def __str__(self):
        return self.title
