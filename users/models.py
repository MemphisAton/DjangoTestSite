from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser): #расширение модели, потом надо подклбчить в админ.py
    photo = models.ImageField(upload_to="users/%Y/%m/%d/",
                              blank=True,
                              null=True,
                              verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name="Дата рождения")
