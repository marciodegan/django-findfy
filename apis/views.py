from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, F
from django.db.models.expressions import Func, Star
from django.db.models.fields import DecimalField, FloatField, IntegerField
from datetime import datetime, time
from django.utils import timezone

from tables.models import TableItens, Table
from restaurantes.models import Restaurante 
import json

# from rest_framework import viewsets
# from . import serializers


# class RestauranteViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.RestauranteSerializer
#     queryset = models.Restaurante.objects.all()


def vendas(request, rest, data_inicial, data_final):
    total_em_aberto = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True, table__open_date__date__range=(data_inicial, data_final))\
        .values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')

    data = {
        'data': [
            {
                'label': item['item__item'],
                'value': item['itemtotal']
            }
            for item in total_em_aberto
        ]
    }
    return JsonResponse(data)


def vendasfechadashoje(request, rest, data_inicial, data_final):
    total_em_aberto = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final))\
        .values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')

    data = {
        'data': [
            {
                'label': item['item__item'],
                'value': item['itemtotal']
            }
            for item in total_em_aberto
        ]
    }
    return JsonResponse(data)