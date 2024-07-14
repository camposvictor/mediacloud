# mediacloud/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def save(self, *args, **kwargs):
        if self.pk and self.profile_picture:
            old_profile_picture = CustomUser.objects.get(pk=self.pk).profile_picture
            if old_profile_picture:
                old_profile_picture.delete(save=False) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
