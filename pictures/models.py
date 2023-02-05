from django.contrib.auth.models import User
from django.db import models


class Picture(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    file = models.ImageField(verbose_name='Фото', upload_to='pictures')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.title
