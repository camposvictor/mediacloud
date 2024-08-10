from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

    def get_file_name(self):
        return self.file.name

    @property
    def file_size(self):
        """Retorna o tamanho do arquivo em bytes"""
        return self.file.size

    class Meta:
        indexes = [
            models.Index(fields=['file']),
        ]

