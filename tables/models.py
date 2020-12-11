from django.db import models
from django.contrib.auth import get_user_model
import uuid

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from restaurantes.models import Restaurante, PracasRestaurante, AtendentesRestaurante, OpenDate
from django.contrib.auth import get_user_model
from menus.models import ItensMenu
from django.utils import timezone

import math



class Number(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

class TableNumber(models.Model):
    table_number = models.IntegerField()
    table_ref = models.UUIDField(default=uuid.uuid4)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True)
    openstatus = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return "Mesa " + str(self.table_number) + " - " + self.restaurante.name + " - aberta: " + str(self.openstatus) 
    
    class Meta:
        unique_together = ('table_number', 'restaurante')


class Table(models.Model):
    table_code = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)
    table_check_number = models.UUIDField(default=uuid.uuid4, null=True)
    table_number = models.ForeignKey(TableNumber, on_delete=models.CASCADE)
    atendente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    atendentes = models.ForeignKey(AtendentesRestaurante, on_delete=models.CASCADE, null=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pagamento_solicitado = models.BooleanField(default=False)
    pagamento_solicitado_code = models.IntegerField(null=True)
    garcom_confirmado_pagamento = models.BooleanField(default=False)
    chamar_atendente = models.BooleanField(default=False, null=True)
    open_date = models.ForeignKey(OpenDate, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.table_check_number)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.table_code)
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.table_check_number}'+'.jpeg'
        buffer = BytesIO()
        canvas.save(buffer, 'JPEG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class TableItens(models.Model):
    item_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="itemuser", null=True)
    atendente_insert = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="atendenteuser", null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    item = models.ForeignKey(ItensMenu, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(default=timezone.now)
    order_obs = models.CharField(max_length=144, null=True)
    price = models.FloatField(null=True)
    confirmed = models.BooleanField(default=False)
    garconconfirmed = models.BooleanField(default=False)
    who_confirmed = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="whoconfirmed", null=True)
    garcon_to_bar = models.BooleanField(default=False)
    bar_to_garcon = models.BooleanField(default=False)
    garcon_to_cozinha = models.BooleanField(default=False)
    cozinha_to_garcon = models.BooleanField(default=False)
    praca1_aceite = models.BooleanField(default=False)
    praca1_entrega = models.BooleanField(default=False)    
    praca2_aceite = models.BooleanField(default=False)
    praca2_entrega = models.BooleanField(default=False)    
    praca3_aceite = models.BooleanField(default=False)
    praca3_entrega = models.BooleanField(default=False)    
    praca4_aceite = models.BooleanField(default=False)
    praca4_entrega = models.BooleanField(default=False)    
    
    item_code = models.IntegerField(null=True)
    
    # função para mostrar tempo de espera dos pedidos
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "segundo"
                # return str("menos de 1 minuto")
            else:
                return str(seconds) + " segundos"
                # return str("menos de 1 minuto")

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 86400:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minuto"
            
            else:
                return str(minutes) + " minutos"



        # if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        #     hours= math.floor(diff.seconds/3600)

        #     if hours == 1:
        #         return str(hours) + "horas"

        #     else:
        #         return str(hours) + " horas"

        # # 1 day to 30 days
        # if diff.days >= 1 and diff.days < 30:
        #     days= diff.days
        
        #     if days == 1:
        #         return str(days) + " dias"

        #     else:
        #         return str(days) + " dias"

        # if diff.days >= 30 and diff.days < 365:
        #     months= math.floor(diff.days/30)
            

        #     if months == 1:
        #         return str(months) + " meses atrás"

        #     else:
        #         return str(months) + " meses atrás"


        # if diff.days >= 365:
        #     years= math.floor(diff.days/365)

        #     if years == 1:
        #         return str(years) + " anos atrás"

        #     else:
        #         return str(years) + " anos atrás"
    
    def checker(self):
        now = timezone.now()
        
        diff= now - self.created_at

        if diff.seconds >= 0 and diff.seconds < 10:
            return "cancelar"
        else:
            pass


class TableUser(models.Model):
    table_user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(null=True, default=False)
    communicate = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.table_user)


# need to move this model to Restaurante.models
class FormaDePagamento(models.Model):
    forma_pagamento = models.CharField(max_length=10)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.forma_pagamento


class Caixa(models.Model):
    caixa = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="caixa")
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ValoresCaixa(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="caixauser")
    valor = models.FloatField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaDePagamento, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
