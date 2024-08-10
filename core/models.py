from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    def save(self, *args, **kwargs):
        if self.pk and self.profile_picture:
            old_profile_picture = CustomUser.objects.get(pk=self.pk).profile_picture
            if old_profile_picture:
                old_profile_picture.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class MediaFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

    @property
    def file_size(self):
        """Retorna o tamanho do arquivo em bytes"""
        return self.file.size

    def get_file_name(self):
        return self.file.name


class ImageFile(MediaFile):
    IMAGE_MIME_CHOICES = [
        ("image/jpeg", "JPEG"),
        ("image/png", "PNG"),
        ("image/gif", "GIF"),
    ]

    mime_type = models.CharField(max_length=50, choices=IMAGE_MIME_CHOICES)
    width = models.IntegerField()
    height = models.IntegerField()
    color_depth = models.IntegerField()
    resolution = models.CharField(max_length=50)
    exif_data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["file"]),
        ]


class VideoFile(MediaFile):
    VIDEO_MIME_CHOICES = [
        ("video/mp4", "MP4"),
        ("video/avi", "AVI"),
        ("video/mkv", "MKV"),
    ]

    mime_type = models.CharField(max_length=50, choices=VIDEO_MIME_CHOICES)
    duration = models.DurationField()
    resolution = models.CharField(max_length=50)
    frame_rate = models.FloatField()
    video_codec = models.CharField(max_length=50)
    audio_codec = models.CharField(max_length=50)
    bitrate = models.IntegerField()
    genre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["file"]),
        ]


class AudioFile(MediaFile):
    AUDIO_MIME_CHOICES = [
        ("audio/mpeg", "MP3"),
        ("audio/wav", "WAV"),
        ("audio/aac", "AAC"),
    ]

    mime_type = models.CharField(max_length=50, choices=AUDIO_MIME_CHOICES)
    duration = models.DurationField()
    bitrate = models.IntegerField()
    sample_rate = models.IntegerField()
    channels = models.IntegerField()
    genre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["file"]),
        ]
