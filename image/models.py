import os

from django.db import models
import random
import string


class ImageSave(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    id = models.CharField(max_length=8, unique=True, verbose_name='ID', editable=False)
    image = models.ImageField(upload_to='images/', verbose_name='图片')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # 获取文件扩展名
        ext = os.path.splitext(self.image.name)[1]
        # 构造新的文件名
        self.image.name = f'{self.id}{ext}'

        super(ImageSave, self).save(*args, **kwargs)

    def __str__(self):
        return self.id
