from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys



class EnviarMensagem(models.Model):
    message_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_message")
    message_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_message")
    mensagem = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notificacao = models.BooleanField(null=True)

    def __str__(self):
        return str(self.message_from)


class Like(models.Model):
    like_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_like")
    like_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_like")
    like = models.BooleanField(null=True)
    smile = models.BooleanField(null=True)
    like_anonimo = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.like_from)

