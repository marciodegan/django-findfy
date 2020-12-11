from django.contrib import admin
from .models import Restaurante, AtendentesRestaurante, CaixasRestaurante, BarmanRestaurante, GerenteRestaurante, CozinhaRestaurante, PracasRestaurante, PracasUser, GoogleImport, AtendentesMaster, Ordering, Cardapio, OpenDate

admin.site.register(Restaurante)
admin.site.register(AtendentesRestaurante)
admin.site.register(CaixasRestaurante)
admin.site.register(BarmanRestaurante)
admin.site.register(GerenteRestaurante)
admin.site.register(CozinhaRestaurante)
admin.site.register(PracasRestaurante)
admin.site.register(PracasUser)
admin.site.register(GoogleImport)
admin.site.register(AtendentesMaster)
admin.site.register(Ordering)
admin.site.register(Cardapio)
admin.site.register(OpenDate)

