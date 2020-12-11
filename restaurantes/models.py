from django.db import models
from accounts.models import CustomUser
# from atendentes.models import Atendente
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


# ORDERNAÇÃO DOS ATENDENTES PARA GESTÃO MASTER
class Ordering(models.Model):
    order_number = models.IntegerField()

    def __str__(self):
        return str(self.order_number)


class Restaurante(models.Model):
    name = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="ownername")
    restaurante_ref = models.UUIDField(default=uuid.uuid4, null=True)
    logo = models.ImageField(upload_to='menu/', null=True, blank=True, default='menu/logotipo.png')
    imagem_menu = models.ImageField(upload_to='qr_codes', null=True, blank=True, default='menu/backgr.jpg')
    restaurante_ref_ao_redor = models.UUIDField(default=uuid.uuid4, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True, null=True)
    zap = models.CharField(max_length=255, blank=True, null=True)
    instagram_profile_name = models.CharField(max_length=30, blank=True, null=True)
    key_words = models.CharField(max_length=255, blank=True, null=True)
    cliente_pede = models.BooleanField(default=True)
    quem_esta = models.BooleanField(default=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code_id = models.UUIDField(default=uuid.uuid4, null=True)
    ativo = models.BooleanField(default=True)
    mensalidade = models.FloatField(null=True, blank=True)
    cardapio_gerado = models.BooleanField(default=False)
    mensagem_do_dia = models.CharField(max_length=255, blank=True, null=True)
    ativar_pracas = models.BooleanField(default=False, null=True)
    layout_completo = models.BooleanField(default=False, null=True)
    instrucoes_1 = models.BooleanField(default=False, null=True)
    instrucoes_2 = models.BooleanField(default=False, null=True)
    instrucoes_3 = models.BooleanField(default=False, null=True)
    instrucoes_4 = models.BooleanField(default=False, null=True)
    instrucoes_5 = models.BooleanField(default=False, null=True)
    deactivate = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('user', 'name')
    
    # PARA UTILIZAÇÃO DOS ALERTAS PARA PERÍODO DE TESTES 
    def whenpublished(self):
        now = timezone.now()
        
        diff= self.due_date - now

        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " dia"

            else:
                return str(days) + " dias"
    # SALVA IMAGEM LOGOTIPO
    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.logo)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((200,200) ) 
        imageTemproaryResized.save(outputIoStream , format='PNG', quality=200)
        outputIoStream.seek(0)
        self.logo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" %self.logo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Restaurante, self).save(*args, **kwargs)

    # SALVA IMAGEM DE FUNDO DO CARDÁPIO
    def save_background(self, *args, **kwargs):
        imageTemproary = Image.open(self.imagem_menu)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((200,200) ) 
        imageTemproaryResized.save(outputIoStream , format='PNG', quality=200)
        outputIoStream.seek(0)
        self.imagem_menu = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" %self.imagem_menu.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Restaurante, self).save(*args, **kwargs)


# ABERTURA E FECHAMENTO DO ESTABELECIMENTO
class OpenDate(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    date = models.DateField()
    opened = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

    
class Cardapio(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="cardapiocreator")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    cardapio_code = models.UUIDField(null=True)
    cardapio_oficial_code = models.CharField(max_length=255, null=True)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)
    table_code = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.cardapio_oficial_code)
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.cardapio_code}'+'.jpeg'
        buffer = BytesIO()
        canvas.save(buffer, 'JPEG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)



class AtendentesRestaurante(models.Model):
    atendente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="atendname")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, null=True)
    ordering = models.ForeignKey(Ordering, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.atendente.first_name + " - " + self.restaurante.name + " - " + str(self.status)


class AtendentesMaster(models.Model):
    atendentemaster = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="atendmastername")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CaixasRestaurante(models.Model):
    caixa = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="caixaname")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BarmanRestaurante(models.Model):
    barman = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="barmanname")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GerenteRestaurante(models.Model):
    gerente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="gerentename")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CozinhaRestaurante(models.Model):
    cozinha = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="cozinhaname")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PracasRestaurante(models.Model):
    name = models.CharField(max_length=255, null=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PracasUser(models.Model):
    praca_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="pracaname")
    praca = models.ForeignKey(PracasRestaurante, on_delete=models.CASCADE)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# TO BE REVIEWED
class SiteDetalhes(models.Model):
    tipo_site = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# TO BE REVIEWED
class Site(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    site = models.ForeignKey(SiteDetalhes, on_delete=models.CASCADE)
    photo1 = models.ImageField(upload_to="site_photos", blank=True)
    photo2 = models.ImageField(upload_to="site_photos", blank=True)
    photo3 = models.ImageField(upload_to="site_photos", blank=True)
    photo4 = models.ImageField(upload_to="site_photos", blank=True)
    photo5 = models.ImageField(upload_to="site_photos", blank=True)
    photo6 = models.ImageField(upload_to="site_photos", blank=True)
    photo7 = models.ImageField(upload_to="site_photos", blank=True)
    photo8 = models.ImageField(upload_to="site_photos", blank=True)
    photo9 = models.ImageField(upload_to="site_photos", blank=True)
    photo10 = models.ImageField(upload_to="site_photos", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# TO BE DISCONTINUED
class GoogleImport(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    place_id = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    types = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    hours = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
