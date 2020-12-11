from django.db import models
from restaurantes.models import Restaurante, PracasRestaurante
import uuid


class CategoriaOrdering(models.Model):
    order_number = models.IntegerField()

    def __str__(self):
        return str(self.order_number)


class Menu(models.Model):
    nome = models.CharField(max_length=255, null=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class CategoriasMenu(models.Model):
    categoria = models.CharField(max_length=255)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    ordem_categoria = models.ForeignKey(CategoriaOrdering, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('ordem_categoria', 'restaurante',)

    def __str__(self):
        return self.categoria


class Medida(models.Model):
    medida = models.CharField(max_length=10)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medida



class Ingredientes(models.Model):
    ingrediente = models.CharField(max_length=255)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ingrediente)


class IngredientesItem(models.Model):
    ingrediente = models.ForeignKey(Ingredientes, on_delete=models.CASCADE)
    # item = models.ForeignKey(ItensMenu, on_delete=models.CASCADE)
    quantity = models.FloatField()
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True)
    # praca = models.ForeignKey(PracasRestaurante, on_delete=models.CASCADE, null=True)
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ingrediente)


class ItensMenu(models.Model):
    item = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    categoria = models.ManyToManyField(CategoriasMenu)
    # menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, null=True)
    code_id = models.UUIDField(default=uuid.uuid4, null=True)
    menus = models.ManyToManyField(Menu, related_name="menu")
    name_image = models.ImageField(upload_to='menu', null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cozinha = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    praca1 = models.BooleanField(default=False)
    praca2 = models.BooleanField(default=False)
    praca3 = models.BooleanField(default=False)
    praca4 = models.BooleanField(default=False)
    ingpraca1a = models.CharField(max_length=255, null=True, blank=True)
    ingpraca1b = models.CharField(max_length=255, null=True, blank=True)
    ingpraca1c = models.CharField(max_length=255, null=True, blank=True)
    ingpraca1d = models.CharField(max_length=255, null=True, blank=True)
    ingpraca2a = models.CharField(max_length=255, null=True, blank=True)
    ingpraca2b = models.CharField(max_length=255, null=True, blank=True)
    ingpraca2c = models.CharField(max_length=255, null=True, blank=True)
    ingpraca2d = models.CharField(max_length=255, null=True, blank=True)
    ingpraca3a = models.CharField(max_length=255, null=True, blank=True)
    ingpraca3b = models.CharField(max_length=255, null=True, blank=True)
    ingpraca3c = models.CharField(max_length=255, null=True, blank=True)
    ingpraca3d = models.CharField(max_length=255, null=True, blank=True)
    ingpraca4a = models.CharField(max_length=255, null=True, blank=True)
    ingpraca4b = models.CharField(max_length=255, null=True, blank=True)
    ingpraca4c = models.CharField(max_length=255, null=True, blank=True)
    ingpraca4d = models.CharField(max_length=255, null=True, blank=True)
    ingredientes = models.ManyToManyField(IngredientesItem)

    def __str__(self):
        return self.item


class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


# NOT READY YET
class OrdemDeCompra(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurante


class OrdemDeCompraItens(models.Model):
    ordem_compra = models.ForeignKey(OrdemDeCompra, on_delete=models.CASCADE)
    item = models.ForeignKey(Ingredientes, on_delete=models.CASCADE)
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ordem_compra
