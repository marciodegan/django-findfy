from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('<uuid:rest>/vendas/<str:data_inicial>/<str:data_final>', views.vendas, name='vendas_api'),
    path('<uuid:rest>/vendasfechadashoje/<str:data_inicial>/<str:data_final>', views.vendasfechadashoje, name='vendasfechadashoje_api'),
    # path('restaurante, views')
]