from django.db import models
from accounts.models import CustomUser
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import uuid
# from formatChecker import ContentTypeRestrictedFileField


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile = models.TextField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True, default="images/avatar.png")
    is_atendente = models.BooleanField(null=True, default=False)
    is_restaurante = models.BooleanField(null=True)
    visible = models.BooleanField(null=True, default=False)
    communicate = models.BooleanField(null=True, default=False)
    code = models.UUIDField(default=uuid.uuid4, null=True)
    instrucao_estabelecimento = models.BooleanField(null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.avatar)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (200,200) ) 
        imageTemproaryResized.save(outputIoStream , format='PNG', quality=100)
        outputIoStream.seek(0)
        self.avatar = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" %self.avatar.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(UserProfile, self).save(*args, **kwargs)


class Liker(models.Model):
    like_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="fromuser")
    like_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="touser")
    curtida = models.BooleanField(default=False, blank=True)
    block = models.BooleanField(default=False, blank=True)
    like_anonimo = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.like_from)