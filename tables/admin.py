from django.contrib import admin
from .models import Table, TableNumber, TableUser, TableItens, FormaDePagamento, Number, ValoresCaixa
# Register your models here.

admin.site.register(Table)
admin.site.register(TableNumber)
admin.site.register(TableUser)
admin.site.register(TableItens)
admin.site.register(FormaDePagamento)
admin.site.register(ValoresCaixa)
admin.site.register(Number)

