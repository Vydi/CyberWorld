from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,verbose_name='Дата рождения', null=True)
    photo = models.ImageField(upload_to='users/photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
