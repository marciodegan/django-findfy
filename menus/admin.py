from django.contrib import admin
from .models import Menu, ItensMenu, CategoriasMenu, Ingredientes, IngredientesItem, OrdemDeCompra, OrdemDeCompraItens, Fornecedor, Medida, CategoriaOrdering
# Register your models here.

admin.site.register(Menu)
admin.site.register(ItensMenu)
admin.site.register(CategoriasMenu)
admin.site.register(Ingredientes)
admin.site.register(IngredientesItem)
admin.site.register(OrdemDeCompraItens)
admin.site.register(OrdemDeCompra)
admin.site.register(Fornecedor)
admin.site.register(Medida)
admin.site.register(CategoriaOrdering)



