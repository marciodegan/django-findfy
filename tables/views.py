from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum, Q, Count, F, Func, FloatField
from datetime import datetime, time, timedelta
from django.contrib import messages

from . models import Table, TableNumber, TableUser, TableItens, FormaDePagamento, ValoresCaixa
from restaurantes.models import Restaurante, AtendentesRestaurante, CaixasRestaurante, BarmanRestaurante, GerenteRestaurante, CozinhaRestaurante, PracasRestaurante, PracasUser, AtendentesMaster, OpenDate
from menus.models import ItensMenu, CategoriasMenu, Menu, IngredientesItem
from profiles.models import UserProfile
# from mensagens.models import EnviarMensagem

from . forms import TableForm, LancamentoForm, DateForm
import uuid

import qrcode

import random
import string

def create_ref_code():
    return ''.join(random.choices(string.digits, k=9))

@login_required
def indexTables(request):
    tables = TableUser.objects.filter(table__paid=False, table_user=request.user.id)
    tables_paid = TableUser.objects.filter(table__paid=True, table_user=request.user.id)
    
    return render(request, 'tables/index-cliente.html', {'tables':tables, 'tables_paid':tables_paid})


# ATENDENTE
@login_required
def viewRestaurantesAtendente(request):
    atendenteativo = AtendentesRestaurante.objects.filter(atendente=request.user.id, status=True)
    
    return render(request, 'tables/index-atendente.html', {'atendenteativo': atendenteativo})


# working / but can improve queries
@login_required
def solicitacoesAtendenteView(request, rest, atendente):
    get_atendente = get_object_or_404(AtendentesRestaurante, code=atendente, restaurante__restaurante_ref=rest, status=True, restaurante__deactivate=False)
    
    itens_confirmados = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=True).order_by('-created_at')
    items_garconconfirmed = itens_confirmados.filter(garconconfirmed=True).order_by('-updated_at')
    last_ten_items_garconconfirmed = items_garconconfirmed[0:10]
    
    all_tables = Table.objects.filter(restaurante__restaurante_ref=rest, paid=False)
    tables_atendente = all_tables.filter(atendentes__code=atendente)
    tables_conta = all_tables.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False, atendentes__code=atendente)
    
    tables_available = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
    timenow = datetime.now()
    itens_cancelados = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=False).order_by('-created_at')
    
    return render(request, 'tables/solicitacoes-atendente.html', {'tables_conta': tables_conta, 'timenow': timenow, 'get_atendente': get_atendente, 'itens_confirmados': itens_confirmados, 
        'tables_atendente': tables_atendente, 'tables_available': tables_available,
        'last_items_garconconfirmed': last_ten_items_garconconfirmed,
        'itens_cancelados': itens_cancelados})


# working / but can improve queries
@login_required
def solicitacoesAtendenteInstrucoesView(request, rest, atendente):
    get_atendente = get_object_or_404(AtendentesRestaurante, code=atendente, restaurante__restaurante_ref=rest, status=True)
    
    itens_confirmados = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=True).order_by('-created_at')
    items_garconconfirmed = itens_confirmados.filter(garconconfirmed=True).order_by('-updated_at')
    last_ten_items_garconconfirmed = items_garconconfirmed[0:10]
    
    all_tables = Table.objects.filter(restaurante__restaurante_ref=rest, paid=False)
    tables_atendente = all_tables.filter(atendentes__code=atendente)
    tables_conta = all_tables.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False, atendentes__code=atendente)
    
    tables_available = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
    timenow = datetime.now()
    itens_cancelados = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=False).order_by('-created_at')
    
    return render(request, 'tables/instrucoes-solicitacoes-atendente.html', {'tables_conta': tables_conta, 'timenow': timenow, 'get_atendente': get_atendente, 'itens_confirmados': itens_confirmados, 
        'tables_atendente': tables_atendente, 'tables_available': tables_available,
        'last_items_garconconfirmed': last_ten_items_garconconfirmed,
        'itens_cancelados': itens_cancelados})


# working / but can improve queries
@login_required
def solicitacoesAtendenteInstrucoes2View(request, rest, atendente):
    get_atendente = get_object_or_404(AtendentesRestaurante, code=atendente, restaurante__restaurante_ref=rest, status=True)
    
    itens_confirmados = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=True).order_by('-created_at')
    items_garconconfirmed = itens_confirmados.filter(garconconfirmed=True).order_by('-updated_at')
    last_ten_items_garconconfirmed = items_garconconfirmed[0:10]
    
    all_tables = Table.objects.filter(restaurante__restaurante_ref=rest, paid=False)
    tables_atendente = all_tables.filter(atendentes__code=atendente)
    tables_conta = all_tables.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False, atendentes__code=atendente)
    
    tables_available = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
    timenow = datetime.now()
    itens_cancelados = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=False).order_by('-created_at')
    
    return render(request, 'tables/instrucoes2-solicitacoes-atendente.html', {'tables_conta': tables_conta, 'timenow': timenow, 'get_atendente': get_atendente, 'itens_confirmados': itens_confirmados, 
        'tables_atendente': tables_atendente, 'tables_available': tables_available,
        'last_items_garconconfirmed': last_ten_items_garconconfirmed,
        'itens_cancelados': itens_cancelados})


# working
@login_required
def viewTablesAtendenteEnviarCozinha(request, rest, id, item):
    item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user)
    item.garcon_to_cozinha=True
    item.save()
    
    return redirect('solicitacoes-atendente-view', rest=rest, atendente=item.table.atendentes.code)


#working
@login_required
def viewTablesAtendenteEnviarBar(request, rest, id, item):
    item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user)
    item.garcon_to_bar=True
    item.save()
    
    return redirect('solicitacoes-atendente-view', rest=rest, atendente=item.table.atendentes.code)


#working
@login_required
def viewTablesAtendenteCancel(request, rest, id, item):
    item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user)
    item.confirmed=False
    item.save()
    
    return redirect('solicitacoes-atendente-view', rest=rest, atendente=item.table.atendentes.code)


@login_required
def PreNewTable(request, rest, atend, mesa):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest)
    get_mesa = get_object_or_404(TableNumber, table_ref=mesa, openstatus=False)
 
    return render(request, 'tables/table-pre-open.html', {'get_mesa': get_mesa, 'get_restaurante': get_restaurante})


#IMPROVE THIS
@login_required
def viewTables(request, rest):
    tables_opened = Table.objects.filter(table_number__openstatus=True, paid=False, restaurante__restaurante_ref=rest).order_by('table_number')
    tables_closed = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
    atendenteativo = get_object_or_404(AtendentesRestaurante, restaurante__restaurante_ref=rest)
    table_atendente = Table.objects.filter(table_number__openstatus=True, paid=False, restaurante__restaurante_ref=rest, atendente=request.user).order_by('table_number')
    
    return render(request, 'tables/view_tables.html', {'tables_opened': tables_opened, 'tables_closed': tables_closed, 'atendenteativo': atendenteativo, 'table_atendente': table_atendente})


# WORKING FINE. IMPROVE LATER
@login_required
def newTable(request, rest, mesa):
    get_mesa = get_object_or_404(TableNumber, table_ref=mesa, restaurante__restaurante_ref=rest, openstatus=False)
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest)
    get_open_date = get_object_or_404(OpenDate, restaurante__restaurante_ref=rest, opened=True)
    atendentes = get_object_or_404(AtendentesRestaurante, atendente=request.user.id, restaurante__restaurante_ref=rest, status=True)
 
    # GENERATES QR CODE FOR NEW TABLE OPENING
    initial = "https://findfy.herokuapp.com/table/"
    restaurante = str(rest)
    mesa = str(mesa)
    table_coder = str(uuid.uuid4())
    myTuple = (initial, restaurante, '/', table_coder)
    x = "".join(myTuple)
    
    status = get_object_or_404(TableNumber, table_ref=mesa)
    if(status.openstatus == False):
        status.openstatus = True
        status.save()
        Table.objects.create(table_code=x, table_check_number=table_coder, table_number=get_mesa, paid=False, restaurante=get_restaurante, atendente=request.user, atendentes=atendentes, open_date=get_open_date)
        
    obj = Table.objects.get(table_check_number=table_coder)

    return redirect('confirmed-new-table', rest=rest, mesa=table_coder)


@login_required
def ConfirmedNewTable(request, rest, mesa):
    restaurante_check = get_object_or_404(Restaurante, restaurante_ref=rest)
    obj = Table.objects.get(table_check_number=mesa)

    return render(request, 'tables/table_open_confirmation.html', {'obj': obj})


# ATENDENTE-MASTER
@login_required
def AtendenteMasterIndexView(request):
    restaurantes = AtendentesMaster.objects.filter(atendentemaster=request.user.id)
    
    return render(request, 'tables/index-atendente-master.html', {'restaurantes': restaurantes})


# THIS VIEW COMBINES ALL ATENDENTES TOGETHER IN ONE SCREEN
@login_required
def viewTablesAll(request, rest, atendentemaster):
    all_tables = Table.objects.filter(restaurante__restaurante_ref=rest)
    tables_opened = all_tables.filter(table_number__openstatus=True, paid=False)
    tables_pay = all_tables.filter(table_number__openstatus=True, paid=False, pagamento_solicitado=True)
    
    tables_closed = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
      
    get_atendentemaster = get_object_or_404(AtendentesMaster, restaurante__restaurante_ref=rest, code=atendentemaster, atendentemaster=request.user.id, status=True)
    atendentesativos = AtendentesRestaurante.objects.filter(restaurante__restaurante_ref=rest, status=True)
    
    all_tables_items = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__paid=False, garconconfirmed=False).order_by('-created_at')
    atendente1 = all_tables_items.filter(table__atendentes__ordering=1)
    atendente2 = all_tables_items.filter(table__atendentes__ordering=2)
    atendente3 = all_tables_items.filter(table__atendentes__ordering=3)
    atendente4 = all_tables_items.filter(table__atendentes__ordering=4)
    atendente5 = all_tables_items.filter(table__atendentes__ordering=5)
    atendente6 = all_tables_items.filter(table__atendentes__ordering=6)
    atendente7 = all_tables_items.filter(table__atendentes__ordering=7)
    atendente8 = all_tables_items.filter(table__atendentes__ordering=8)
    atendente9 = all_tables_items.filter(table__atendentes__ordering=9)
    atendente10 = all_tables_items.filter(table__atendentes__ordering=10)
    
    atendentename = AtendentesRestaurante.objects.filter(restaurante__restaurante_ref=rest)
    atendentename1 = atendentename.filter(ordering=1)
    atendentename2 = atendentename.filter(ordering=2)
    atendentename3 = atendentename.filter(ordering=3)
    atendentename4 = atendentename.filter(ordering=4)
    atendentename5 = atendentename.filter(ordering=5)
    atendentename6 = atendentename.filter(ordering=6)
    atendentename7 = atendentename.filter(ordering=7)
    atendentename8 = atendentename.filter(ordering=8)
    atendentename9 = atendentename.filter(ordering=9)
    atendentename10 = atendentename.filter(ordering=10)
    
    atendente1_table_pay = tables_pay.filter(atendentes__ordering=1)
    atendente2_table_pay = tables_pay.filter(atendentes__ordering=2)
    atendente3_table_pay = tables_pay.filter(atendentes__ordering=3)
    atendente4_table_pay = tables_pay.filter(atendentes__ordering=4)
    atendente5_table_pay = tables_pay.filter(atendentes__ordering=5)
    atendente6_table_pay = tables_pay.filter(atendentes__ordering=6)
    atendente7_table_pay = tables_pay.filter(atendentes__ordering=7)
    atendente8_table_pay = tables_pay.filter(atendentes__ordering=8)
    atendente9_table_pay = tables_pay.filter(atendentes__ordering=9)
    atendente10_table_pay = tables_pay.filter(atendentes__ordering=10)

    return render(request, 'tables/view-tables-all.html', 
        {'tables_opened': tables_opened, 'tables_closed': tables_closed, 
        'get_atendentemaster': get_atendentemaster, 
        'atendentesativos': atendentesativos, 'all_tables_items': all_tables_items, 
        'atendente1': atendente1, 'atendente2': atendente2, 'atendente3': atendente3,
        'atendente4': atendente4, 'atendente5': atendente5, 'atendente6': atendente6,
        'atendente7': atendente7, 'atendente8': atendente8, 'atendente9': atendente9,
        'atendente10': atendente10,
        'atendentename1': atendentename1, 'atendentename2': atendentename2, 'atendentename3': atendentename3,
        'atendentename4': atendentename4, 'atendentename5': atendentename5, 'atendentename6': atendentename6,
        'atendentename7': atendentename7, 'atendentename8': atendentename8, 'atendentename9': atendentename9,
        'atendentename10': atendentename10, 
        'atendente1_table_pay': atendente1_table_pay, 'atendente2_table_pay': atendente2_table_pay, 'atendente3_table_pay': atendente3_table_pay,
        'atendente4_table_pay': atendente4_table_pay, 'atendente5_table_pay': atendente5_table_pay, 'atendente6_table_pay': atendente6_table_pay,
        'atendente7_table_pay': atendente7_table_pay, 'atendente8_table_pay': atendente8_table_pay, 'atendente9_table_pay': atendente9_table_pay,
        'atendente10_table_pay': atendente10_table_pay})


# WORKING
@login_required
def SolicitacoesAtendenteMasterView(request, rest, atendente):
    get_atendente = get_object_or_404(AtendentesRestaurante, code=atendente, restaurante__restaurante_ref=rest, status=True)
    get_atendentemaster = get_object_or_404(AtendentesMaster, atendentemaster=request.user.id, restaurante__restaurante_ref=rest, status=True)
    
    itens_confirmados = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=True).order_by('-created_at')
    items_garconconfirmed = itens_confirmados.filter(garconconfirmed=True).order_by('-updated_at')
    last_ten_items_garconconfirmed = items_garconconfirmed[0:10]
    
    all_tables = Table.objects.filter(restaurante__restaurante_ref=rest, paid=False)
    tables_atendente = all_tables.filter(atendentes__code=atendente)
    tables_conta = all_tables.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False, atendentes__code=atendente)
    
    tables_available = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
    timenow = datetime.now()
    itens_cancelados = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=False).order_by('-created_at')
    
    return render(request, 'tables/solicitacoes-atendente-masterview.html', {'tables_conta': tables_conta, 'timenow': timenow, 'get_atendente': get_atendente, 'get_atendentemaster': get_atendentemaster, 'itens_confirmados': itens_confirmados, 'tables_atendente': tables_atendente, 'tables_available': tables_available, 'itens_cancelados': itens_cancelados, 'last_items_garconconfirmed': last_ten_items_garconconfirmed})


# THIS IS FOR OPENING A TABLE IN THE MASTERVIEW. SHOULD BE REVIEWED FOR IMPROVEMENTS
@login_required
def PreNewTableMasterView(request, rest, atend, mesa):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest)
    get_mesa = get_object_or_404(TableNumber, table_ref=mesa, openstatus=False, restaurante__restaurante_ref=rest)
    get_atendente_master = get_object_or_404(AtendentesMaster, atendentemaster=request.user.id)
    get_atendente = get_object_or_404(AtendentesRestaurante, code=atend, restaurante__restaurante_ref=rest, status=True)

    return render(request, 'tables/table-pre-open.html', {'get_mesa': get_mesa, 'get_atendente': get_atendente, 'get_restaurante': get_restaurante })


@login_required
def newTableMaster(request, rest, atend, mesa):
    restaurante_check = get_object_or_404(Restaurante, restaurante_ref=rest)
    get_mesa_number = get_object_or_404(TableNumber, table_ref=mesa, openstatus=False)
    atendente_master = get_object_or_404(AtendentesMaster, atendentemaster=request.user.id, status=True)
    atendentes = get_object_or_404(AtendentesRestaurante, code=atend, status=True)
 
    initial = "https://findfy.herokuapp.com/table/"
    restaurante = str(rest)
    atendente = str(atend)
    mesa = str(mesa)
    table_coder = create_ref_code()
    myTuple = (initial, restaurante, '/', table_coder)
    x = "".join(myTuple)
    
    status = get_object_or_404(TableNumber, table_ref=mesa)
    if(status.openstatus == False):
        status.openstatus = True
        status.save()
    Table.objects.create(table_code=x, table_check_number=table_coder, table_number=get_mesa_number, paid=False, restaurante=restaurante_check, atendentes=atendentes)
     
    obj = Table.objects.get(table_check_number=table_coder)

    return redirect('confirmed-new-table', rest=rest, atend=atend, mesa=table_coder)


# WORKKING
@login_required
def viewTablesAtendenteEnviarCozinhaMaster(request, rest, id, item):
    item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user)
    item.garcon_to_cozinha=True
    item.save()
    return redirect('solicitacoes-atendente-master-view', rest=rest, atendente=item.table.atendentes.code)


@login_required
def viewTablesAtendenteMasterEnviarCozinha(request, rest, mesa, pk, atendente):
    get_atendentemaster = get_object_or_404(AtendentesMaster, atendentemaster=request.user.id, status=True, restaurante__restaurante_ref=rest)
    get_item = get_object_or_404(TableItens, pk=pk, table__paid=False, table__restaurante__restaurante_ref=rest, table__table_check_number=mesa)
    get_item.garcon_to_cozinha = True
    get_item.save()
    return redirect('solicitacoes-atendente-master-view', rest=rest, atendente=atendente)


@login_required
def viewTablesAtendenteMasterEnviarBar(request, rest, mesa, pk, atendente):
    get_atendentemaster = get_object_or_404(AtendentesMaster, atendentemaster=request.user.id, status=True, restaurante__restaurante_ref=rest)
    get_item = get_object_or_404(TableItens, pk=pk, table__paid=False, table__restaurante__restaurante_ref=rest, table__table_check_number=mesa)
    get_item.garcon_to_bar = True
    get_item.save()
    return redirect('solicitacoes-atendente-master-view', rest=rest, atendente=atendente)


# COZINHA
@login_required
def CozinhaView(request):
    restaurantes = CozinhaRestaurante.objects.filter(cozinha=request.user.id)
    return render(request, 'tables/index-cozinha.html', {'restaurantes': restaurantes})


@login_required
def viewTablesCozinha(request, rest):
    nova_solicitacao = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, garconconfirmed=False).order_by('-created_at')
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest)
    restaurante_cozinha = get_object_or_404(CozinhaRestaurante, restaurante__restaurante_ref=rest, cozinha=request.user, status=True)
    itensprato = IngredientesItem.objects.filter(ingrediente__restaurante__restaurante_ref=rest)
    if get_restaurante.layout_completo == True:
        return render(request, 'tables/cozinha-solicitacoes.html', {'nova_solicitacao': nova_solicitacao, 'itensprato': itensprato})
    else:
        return render(request, 'tables/solicitacoes-cozinha-simples.html', {'nova_solicitacao': nova_solicitacao, 'itensprato': itensprato})


@login_required
def viewTablesCozinhaEnviarGarcon(request, rest, id, item):
    item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
    item.cozinha_to_garcon=True
    item.save()
    
    return redirect('view-tables-cozinha', rest=rest)


# BAR
@login_required
def BarView(request):
    restaurantes = BarmanRestaurante.objects.filter(barman=request.user.id)
    return render(request, 'tables/index-bar.html', {'restaurantes': restaurantes})


@login_required
def viewTablesBar(request, rest):
    nova_solicitacao = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, garconconfirmed=False).order_by('-created_at')
    restaurante_bar = get_object_or_404(BarmanRestaurante, restaurante__restaurante_ref=rest, barman=request.user, status=True)
    itensprato = IngredientesItem.objects.filter(ingrediente__restaurante__restaurante_ref=rest)
    return render(request, 'tables/solicitacoes-bar.html', {'nova_solicitacao': nova_solicitacao, 'itensprato': itensprato})


@login_required
def viewTablesBarEnviarGarcon(request, rest, id, item):
    item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
    item.bar_to_garcon=True
    item.save()
    
    return redirect('view-tables-bar', rest=rest)


@login_required
def PreNewTableItem(request, rest, id, item):
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
    itensbebidas = itensmenu.filter(categoria=2)
    itenspratos = itensmenu.filter(categoria=1)
    itensdrinks = itensmenu.filter(categoria=3)
    itenssobremesas = itensmenu.filter(categoria=4)
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    categbebidas = categ.filter(categoria=2)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    no_local = TableUser.objects.all()
    itensmenucheck = get_object_or_404(ItensMenu, pk=item)
    tableitems = TableItens.objects.filter(table=obj)

    return render(request, 'tables/confirmaritem.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 'no_local': no_local, 'user_check': user_check, 'categbebidas': categbebidas, 'itensbebidas':itensbebidas, 'itenspratos': itenspratos, 'itenssobremesas': itenssobremesas, 'itensdrinks': itensdrinks, 'tableitems':tableitems, 'itensmenucheck':itensmenucheck})


# PRE-NEW-TABLE-ITEM
# WORKING FINE. NEED TO CORRECT VARIABLE NAMES
@login_required
def PreNewTableItemClienteConfirmedNew(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        mesa = request.POST.get('mesa')
        price = request.POST.get('price')
        restaurante = request.POST.get('restaurante')
        bookId = request.POST.get('bookId')
        obs = request.POST.get('obs')
        obj = get_object_or_404(Table, paid=False, pagamento_solicitado=False, table_check_number=mesa)
        itensmenucheck = get_object_or_404(ItensMenu, pk=bookId)
        tableitems = TableItens.objects.filter(table=obj)    
        item_coder = create_ref_code()
        
        TableItens.objects.create(table=obj, item_user=request.user, item=itensmenucheck, price=price, confirmed=True, order_obs=obs, item_code=item_coder)    

        response_data['mesa'] = mesa
        response_data['price'] = price
        response_data['restaurante'] = restaurante
        response_data['bookId'] = bookId    
        
    return HttpResponse('ok')


# WORKING FINE. NEED TO CORRECT VARIABLE NAMES
@login_required
def PreNewTableItemAtendente(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        mesa = request.POST.get('mesa')
        price = request.POST.get('price')
        restaurante = request.POST.get('restaurante')
        bookId = request.POST.get('bookId')
        obs = request.POST.get('obs')
        obj = get_object_or_404(Table, paid=False, pagamento_solicitado=False, table_check_number=mesa)
        get_item = get_object_or_404(ItensMenu, pk=bookId)
        tableitems = TableItens.objects.filter(table=obj)    
        item_coder = create_ref_code()
        
        TableItens.objects.create(table=obj, atendente_insert=request.user, item=get_item, price=price, confirmed=True, order_obs=obs, item_code=item_coder)    

        response_data['mesa'] = mesa
        response_data['price'] = price
        response_data['restaurante'] = restaurante
        response_data['bookId'] = bookId    
        
    return HttpResponse('ok')


# NEW-TABLE-ITEM
#ok
@login_required
def NewTableItemAtendente(request, rest, mesa, pk):
    get_atendente = AtendentesRestaurante.objects.get(atendente=request.user, restaurante__restaurante_ref=rest)
    get_item = get_object_or_404(TableItens, pk=pk, table__paid=False, table__restaurante__restaurante_ref=rest, table__table_check_number=mesa)
    get_item.garconconfirmed = True
    get_item.who_confirmed = request.user
    get_item.save()
    return redirect('solicitacoes-atendente-view', rest=rest, atendente=get_atendente.code)


@login_required
def NewTableItemGarcomMaster(request, rest, mesa, pk, atendente):
    get_atendentemaster = get_object_or_404(AtendentesMaster, atendentemaster=request.user.id, status=True, restaurante__restaurante_ref=rest)
    get_item = get_object_or_404(TableItens, pk=pk, table__paid=False, table__restaurante__restaurante_ref=rest, table__table_check_number=mesa)
    get_item.garconconfirmed = True
    get_item.who_confirmed = request.user
    get_item.save()
    return redirect('solicitacoes-atendente-master-view', rest=rest, atendente=atendente)


# CAIXA VIEWS
@login_required
def CaixaView(request):
    restaurantes = CaixasRestaurante.objects.filter(caixa=request.user.id)
    return render(request, 'tables/index-caixa.html', {'restaurantes': restaurantes})


@login_required
def viewTablesCaixa(request, rest):
    restaurante = get_object_or_404(Restaurante, restaurante_ref=rest)
    restaurante_caixa = get_object_or_404(CaixasRestaurante, restaurante__restaurante_ref=rest, caixa=request.user, status=True)
    
    tables_opened = Table.objects.filter(table_number__openstatus=True, paid=False, restaurante__restaurante_ref=rest).order_by('table_number')
    tables_closed = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
    all_tables_items = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__paid=False, confirmed=True).order_by('-created_at')
    tables_conta = Table.objects.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False)
    tables_conta_cliente_confirmed = Table.objects.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False, paid=False)
    tables_pagas = TableItens.objects.filter(table__paid=True, table__restaurante__restaurante_ref=rest).values('table__table_check_number').annotate(total=Sum('item__price')).values('total', 'table__table_check_number', 'table__table_number__table_number', 'table__updated_at', 'table__created_at', 'table__atendente__first_name').order_by('-table__updated_at')
    
    return render(request, 'tables/caixa.html', {'all_tables_items': all_tables_items, 'tables_opened': tables_opened, 'tables_closed': tables_closed, 'restaurante': restaurante, 'tables_conta': tables_conta, 'tables_conta_cliente_confirmed': tables_conta_cliente_confirmed, 'restaurante_caixa': restaurante_caixa, 'restaurante': restaurante, 'tables_pagas': tables_pagas})


@login_required
def CaixaContaView(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.filter(table__table_check_number=id).annotate(total=Sum('item__price')).annotate(counter=Count('item_user')).values('total', 'item_user__first_name')
    table_final_total = TableItens.objects.filter(table__table_check_number=id).aggregate(Sum('item__price'))['item__price__sum']
    
    return render(request, 'tables/caixa-conta-view.html', {'obj':obj, 'tableuser': tableuser, 'user_check':user_check, 'table_items_total': table_items_total, 'table_items': table_items, 'table_final_total': table_final_total})


@login_required
def fecharMesaZerada(request, rest, mesa):
    get_table = get_object_or_404(Table, paid=False, table_check_number=mesa)
    get_table.paid = True
    get_table.save()
    get_table_number = get_object_or_404(TableNumber, id=get_table.table_number.id)
    get_table_number.openstatus = False
    get_table_number.save()
    
    return redirect('view-tables-caixa', rest=rest)


@login_required
def CaixaContaPrintView(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.filter(table__table_check_number=id).annotate(total=Sum('item__price')).annotate(counter=Count('item_user')).values('total', 'item_user__first_name')
    table_final_total = TableItens.objects.filter(table__table_check_number=id).aggregate(Sum('item__price'))['item__price__sum']
    
    return render(request, 'tables/caixa-conta-print-view.html', {'obj':obj, 'tableuser': tableuser, 'user_check':user_check, 'table_items_total': table_items_total, 'table_items': table_items, 'table_final_total': table_final_total})


# WORKING FINE. BUT SHOULD BE REVIEWED
@login_required
def CaixaContaLancamento(request, rest, id):
    local = get_object_or_404(Restaurante, restaurante_ref=rest)
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    check_caixa = get_object_or_404(CaixasRestaurante, caixa=request.user.id, restaurante__restaurante_ref=rest)
    
    table_items_subtotal = TableItens.objects.filter(table__table_check_number=id)
    table_items_totalz = table_items_subtotal.aggregate(Sum('item__price'))['item__price__sum']
    floatnum = round(table_items_totalz, 2)
    table_items_total = TableItens.objects.filter(table__table_check_number=id).aggregate(Sum('item__price'))['item__price__sum']
    formasdepagamento = FormaDePagamento.objects.filter(restaurante__restaurante_ref=rest)
    
    valorescaixa = ValoresCaixa.objects.filter(table__restaurante__restaurante_ref=rest, table__table_check_number=id)
    total_lancado = valorescaixa.aggregate(Sum('valor'))['valor__sum']
    if total_lancado:
        tot = float(total_lancado)
    else:
        pass
    form = LancamentoForm(local)
    return render(request, 'tables/caixa-conta-lancamento.html', {'form': form, 'obj':obj, 'table_items_total': table_items_total, 'formasdepagamento': formasdepagamento, 'valorescaixa': valorescaixa, 'total_lancado': total_lancado, 'table_items_totalz':table_items_totalz})


@login_required
def CaixaLancamento(request, rest, id):
    check_caixa = get_object_or_404(CaixasRestaurante, caixa=request.user.id, restaurante__restaurante_ref=rest)
    table = get_object_or_404(Table, paid=False, table_check_number=id)
    local = get_object_or_404(Restaurante, restaurante_ref=rest)

    if request.method == 'POST':
        form = LancamentoForm(local, request.POST)
        
        if form.is_valid():
            lanc = form.save(commit=False)
            lanc.table = table
            lanc.user = request.user
            lanc.save()
            return redirect('caixa-conta-lancamento-view', rest=rest, id=id)
   

@login_required
def CaixaLancamentoDelete(request, rest, id, lancamento):
    try:
        task = get_object_or_404(ValoresCaixa, pk=lancamento)
        task.delete()
        return redirect('caixa-conta-lancamento-view', rest=rest, id=id)
    except:
        return redirect('caixa-conta-lancamento-view', rest=rest, id=id)
    

@login_required
def MesaPaga(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id, restaurante__restaurante_ref=rest)
    obj.paid = True
    obj.save()

    mesa = get_object_or_404(TableNumber, table_number=obj.table_number.table_number, restaurante__restaurante_ref=rest)
    mesa.openstatus = False
    mesa.save()
    
    return redirect('view-tables-caixa', rest=rest)
  
# NOT READY YET
@login_required
def SolicitacaoDePagamento(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.values('item_user').annotate(total=Sum('item__price')).annotate(counter=Count('item_user')).values('total', 'item_user__first_name')
    # table_items_total = table_items.annotate(total=Sum('item__price')).values('item_user', 'item__price')
    # return redirect('solicitacao-de-pagamento-conta-final', rest=rest, id=id)
    return render(request, 'tables/solic-pag-conta-final.html', {'obj':obj, 'tableuser': tableuser, 'user_check':user_check, 'table_items_total': table_items_total, 'table_items': table_items})


# NOT READY YET
@login_required
def SolicitacaoDePagamentoContaFinal(request, rest, id):
    obj = get_object_or_404(Table, paid=False, pagamento_solicitado=False, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.filter(table__table_check_number=id).values('item_user').annotate(total=Sum('item__price'), counter=Count('item_user')).values('total', 'item_user')
    pagamento_coder = create_ref_code()
    obj.pagamento_solicitado_code = pagamento_coder
    obj.pagamento_solicitado = True
    obj.save()

    return redirect('cliente-aguardando-conta', rest=rest, id=id)





# CLIENTE
@login_required
def EntrarMesaCliente(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id, pagamento_solicitado=False)
    itensmenu = ItensMenu.objects.filter(menus__restaurante__restaurante_ref=rest, menus__ativo=True)
    itenscat1 = itensmenu.filter(categoria__ordem_categoria=1)
    itenscat2 = itensmenu.filter(categoria__ordem_categoria=2)
    itenscat3 = itensmenu.filter(categoria__ordem_categoria=3)
    itenscat4 = itensmenu.filter(categoria__ordem_categoria=4)
    itenscat5 = itensmenu.filter(categoria__ordem_categoria=5)
    itenscat6 = itensmenu.filter(categoria__ordem_categoria=6)
    itenscat7 = itensmenu.filter(categoria__ordem_categoria=7)
    itenscat8 = itensmenu.filter(categoria__ordem_categoria=8)
    itenscat9 = itensmenu.filter(categoria__ordem_categoria=9)
    itenscat10 = itensmenu.filter(categoria__ordem_categoria=10)
    itenscat11 = itensmenu.filter(categoria__ordem_categoria=11)
    itenscat12 = itensmenu.filter(categoria__ordem_categoria=12)
    itenscat13 = itensmenu.filter(categoria__ordem_categoria=13)
    itenscat14 = itensmenu.filter(categoria__ordem_categoria=14)
    itenscat15 = itensmenu.filter(categoria__ordem_categoria=15)
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    categ1 = categ.filter(ordem_categoria=1)
    categ2 = categ.filter(ordem_categoria=2)
    categ3 = categ.filter(ordem_categoria=3)
    categ4 = categ.filter(ordem_categoria=4)
    categ5 = categ.filter(ordem_categoria=5)
    categ6 = categ.filter(ordem_categoria=6)
    categ7 = categ.filter(ordem_categoria=7)
    categ8 = categ.filter(ordem_categoria=8)
    categ9 = categ.filter(ordem_categoria=9)
    categ10 = categ.filter(ordem_categoria=10)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    # no_local = TableUser.objects.all()
    tableitems = TableItens.objects.filter(table=obj, confirmed=True).order_by('-id')
    table_items_total = TableItens.objects.filter(table=obj, confirmed=True).values('item_user__first_name').annotate(total=Sum('item__price')).values('total', 'item_user__first_name')
    UserProfile.objects.get_or_create(user=request.user)
    if user_check.exists():
        pass
    else:
        TableUser.objects.create(table=obj, table_user=request.user)
    
    return render(request, 'tables/mesa-oficial.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 
        'user_check': user_check,  
        'itenscat1': itenscat1, 'itenscat2': itenscat2, 'itenscat3': itenscat3, 
        'itenscat4': itenscat4, 'itenscat5': itenscat5, 'itenscat6': itenscat6,
        'itenscat7': itenscat7, 'itenscat8': itenscat8, 'itenscat9': itenscat9,
        'itenscat10': itenscat10, 'itenscat11': itenscat11, 'itenscat12': itenscat12,
        'itenscat13': itenscat13, 'itenscat14': itenscat14, 'itenscat15': itenscat15,
        'tableitems':tableitems, 'user_check': user_check, 
        'table_items_total':table_items_total, 
        'categ1': categ1, 'categ2': categ2, 'categ3': categ3, 
        'categ4': categ4, 'categ5': categ5, 'categ6': categ6, 
        'categ7': categ7, 'categ8': categ8, 'categ9': categ9, 
        'categ10': categ10 })


@login_required
def cardapioView(request, rest, cardapio):
    obj = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest)
    code = get_object_or_404(Cardapio, restaurante__restaurante_ref_ao_redor=rest)
    itensmenu = ItensMenu.objects.filter(menus__restaurante__restaurante_ref_ao_redor=rest, menus__ativo=True)
    itenscat1 = itensmenu.filter(categoria__ordem_categoria=1)
    itenscat2 = itensmenu.filter(categoria__ordem_categoria=2)
    itenscat3 = itensmenu.filter(categoria__ordem_categoria=3)
    itenscat4 = itensmenu.filter(categoria__ordem_categoria=4)
    itenscat5 = itensmenu.filter(categoria__ordem_categoria=5)
    itenscat6 = itensmenu.filter(categoria__ordem_categoria=6)
    itenscat7 = itensmenu.filter(categoria__ordem_categoria=7)
    itenscat8 = itensmenu.filter(categoria__ordem_categoria=8)
    itenscat9 = itensmenu.filter(categoria__ordem_categoria=9)
    itenscat10 = itensmenu.filter(categoria__ordem_categoria=10)
    itenscat11 = itensmenu.filter(categoria__ordem_categoria=11)
    itenscat12 = itensmenu.filter(categoria__ordem_categoria=12)
    itenscat13 = itensmenu.filter(categoria__ordem_categoria=13)
    itenscat14 = itensmenu.filter(categoria__ordem_categoria=14)
    itenscat15 = itensmenu.filter(categoria__ordem_categoria=15)
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    categ1 = categ.filter(ordem_categoria=1)
    categ2 = categ.filter(ordem_categoria=2)
    categ3 = categ.filter(ordem_categoria=3)
    categ4 = categ.filter(ordem_categoria=4)
    categ5 = categ.filter(ordem_categoria=5)
    categ6 = categ.filter(ordem_categoria=6)
    categ7 = categ.filter(ordem_categoria=7)
    categ8 = categ.filter(ordem_categoria=8)
    categ9 = categ.filter(ordem_categoria=9)
    categ10 = categ.filter(ordem_categoria=10)
    tableuser = TableUser.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=False)
    
    return render(request, 'tables/cardapio.html', {'itensmenu': itensmenu, 'tableuser': tableuser, 'obj': obj, 'code': code,
        'itenscat1': itenscat1, 'itenscat2': itenscat2, 'itenscat3': itenscat3, 
        'itenscat4': itenscat4, 'itenscat5': itenscat5, 'itenscat6': itenscat6,
        'itenscat7': itenscat7, 'itenscat8': itenscat8, 'itenscat9': itenscat9,
        'itenscat10': itenscat10, 'itenscat11': itenscat11, 'itenscat12': itenscat12,
        'itenscat13': itenscat13, 'itenscat14': itenscat14, 'itenscat15': itenscat15,
        'categ1': categ1, 'categ2': categ2, 'categ3': categ3, 
        'categ4': categ4, 'categ5': categ5, 'categ6': categ6, 
        'categ7': categ7, 'categ8': categ8, 'categ9': categ9, 
        'categ10': categ10 })



# corrigir table_items_total
@login_required
def EntrarMesaGarcon(request, rest, atend, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id, atendentes__code=atend, restaurante__restaurante_ref=rest)
    itensmenu = ItensMenu.objects.filter(menus__restaurante__restaurante_ref=rest, menus__ativo=True)
    itenscat1 = itensmenu.filter(categoria__ordem_categoria=1)
    itenscat2 = itensmenu.filter(categoria__ordem_categoria=2)
    itenscat3 = itensmenu.filter(categoria__ordem_categoria=3)
    itenscat4 = itensmenu.filter(categoria__ordem_categoria=4)
    itenscat5 = itensmenu.filter(categoria__ordem_categoria=5)
    itenscat6 = itensmenu.filter(categoria__ordem_categoria=6)
    itenscat7 = itensmenu.filter(categoria__ordem_categoria=7)
    itenscat8 = itensmenu.filter(categoria__ordem_categoria=8)
    itenscat9 = itensmenu.filter(categoria__ordem_categoria=9)
    itenscat10 = itensmenu.filter(categoria__ordem_categoria=10)
    itenscat11 = itensmenu.filter(categoria__ordem_categoria=11)
    itenscat12 = itensmenu.filter(categoria__ordem_categoria=12)
    itenscat13 = itensmenu.filter(categoria__ordem_categoria=13)
    itenscat14 = itensmenu.filter(categoria__ordem_categoria=14)
    itenscat15 = itensmenu.filter(categoria__ordem_categoria=15)
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    categ1 = categ.filter(ordem_categoria=1)
    categ2 = categ.filter(ordem_categoria=2)
    categ3 = categ.filter(ordem_categoria=3)
    categ4 = categ.filter(ordem_categoria=4)
    categ5 = categ.filter(ordem_categoria=5)
    categ6 = categ.filter(ordem_categoria=6)
    categ7 = categ.filter(ordem_categoria=7)
    categ8 = categ.filter(ordem_categoria=8)
    categ9 = categ.filter(ordem_categoria=9)
    categ10 = categ.filter(ordem_categoria=10)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    tableitems = TableItens.objects.filter(table=obj, confirmed=True).order_by('-id')
    table_items_total = TableItens.objects.filter(table=obj, confirmed=True).values('item_user__first_name').annotate(total=Sum('item__price')).values('total', 'item_user__first_name')
  
    return render(request, 'tables/mesa-atendente.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 
        'user_check': user_check,  
        'itenscat1': itenscat1, 'itenscat2': itenscat2, 'itenscat3': itenscat3, 
        'itenscat4': itenscat4, 'itenscat5': itenscat5, 'itenscat6': itenscat6,
        'itenscat7': itenscat7, 'itenscat8': itenscat8, 'itenscat9': itenscat9,
        'itenscat10': itenscat10, 'itenscat11': itenscat11, 'itenscat12': itenscat12,
        'itenscat13': itenscat13, 'itenscat14': itenscat14, 'itenscat15': itenscat15,
        'tableitems':tableitems, 'user_check': user_check, 
        'table_items_total':table_items_total, 
        'categ1': categ1, 'categ2': categ2, 'categ3': categ3, 
        'categ4': categ4, 'categ5': categ5, 'categ6': categ6, 
        'categ7': categ7, 'categ8': categ8, 'categ9': categ9, 
        'categ10': categ10 })



@login_required
def EntrarMesaGarcomAlternativo(request, rest, atend, id):
    obj = get_object_or_404(Table, table_check_number=id, paid=False, restaurante__restaurante_ref=rest)
    itensmenu = ItensMenu.objects.all()
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
    itensbebidas = itensmenu.filter(categoria=2)
    itenspratos = itensmenu.filter(categoria=1)
    itensdrinks = itensmenu.filter(categoria=3)
    itenssobremesas = itensmenu.filter(categoria=4)
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    categbebidas = categ.filter(categoria=2)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    no_local = TableUser.objects.all()
    tableitems = TableItens.objects.filter(table=obj).order_by('-id')
    table_items_total = TableItens.objects.filter(table=obj).values('item_user').annotate(total=Sum('item__price')).values('total', 'item_user')
        
    return render(request, 'tables/mesa_garcom_alternativo.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 'no_local': no_local, 'user_check': user_check, 'categbebidas': categbebidas, 'itensbebidas':itensbebidas, 'itenspratos': itenspratos, 'itenssobremesas': itenssobremesas, 'itensdrinks': itensdrinks, 'tableitems':tableitems, 'user_check': user_check, 'table_items_total':table_items_total})


def chamarAtendente(request, rest, mesa):
    get_table = get_object_or_404(Table, restaurante__restaurante_ref=rest, table_check_number=mesa)
    get_table.chamar_atendente = True
    get_table.save()
    return redirect('entrar-mesa', rest=rest, id=mesa)

def deschamarAtendente(request, rest, mesa):
    get_table = get_object_or_404(Table, restaurante__restaurante_ref=rest, table_check_number=mesa)
    get_table.chamar_atendente = False
    get_table.save()
    return redirect('entrar-mesa', rest=rest, id=mesa)


def deschamarAtendenteConfirma(request, rest, mesa):
    get_table = get_object_or_404(Table, restaurante__restaurante_ref=rest, table_check_number=mesa)
    get_table.chamar_atendente = False
    get_table.save()
    return redirect('solicitacoes-atendente-view', rest=rest, atendente=get_table.atendentes.code)


def vendas(request, rest):
    get_local = get_object_or_404(Restaurante, restaurante_ref=rest)

    if request.method == "POST":
        data_inicial = request.POST.get('jqueryDateInicial')
        data_final = request.POST.get('jqueryDateFinal')
        data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
        data_final = datetime.strptime(data_final, '%d/%m/%Y')
        
        total_em_aberto = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True, table__open_date__date__range=(data_inicial, data_final))
        total_items_agg = total_em_aberto.values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')
        total_geral_open = total_em_aberto.values('price').aggregate(totalgeral=Sum('price'))
        
        total_fechado = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final))
        total_paid_agg = total_fechado.values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')
        total_geral_paid = total_fechado.values('price').aggregate(totalgeral=Sum('price'))
        
        mesas_em_aberto = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True, table__open_date__date__range=(data_inicial, data_final))
        mesas_em_aberto_ann = mesas_em_aberto.values('table__table_number__table_number').annotate(itemtotal=Sum('price')).values('itemtotal', 'table__table_number__table_number', 'table__atendentes__atendente__first_name')
    
        tables_pagas = TableItens.objects.filter(confirmed=True, table__paid=True, table__restaurante__restaurante_ref=rest).values('table__table_check_number').annotate(total=Sum('item__price')).values('total', 'table__table_check_number', 'table__table_number__table_number', 'table__updated_at', 'table__created_at', 'table__atendente__first_name').order_by('-table__updated_at')

        mesas_fechadas = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final)).annotate(itemtotal=Sum('price')).values('itemtotal', 'table', 'table__table_number__table_number', 'table__atendentes__atendente__first_name', 'table__created_at', 'table__updated_at')
        mesas_fechadas_ann = mesas_fechadas.values('table').annotate(itemtotal=Sum('price')).values('itemtotal', 'table', 'table__table_number__table_number', 'table__atendentes__atendente__first_name', 'table__created_at', 'table__updated_at')
        mesas_fechadas_ann_total = mesas_fechadas.values('price').aggregate(totalgeral=Sum('price'))
    
        vendas_por_atendente = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__open_date__date__range=(data_inicial, data_final)).values('table__atendentes__atendente__first_name').annotate(itemtotal=Sum('price')).values('itemtotal', 'table__atendentes__atendente__first_name')
    
        formas_de_pagamento = ValoresCaixa.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final))
        formas_de_pagamento_ann = formas_de_pagamento.values('forma_pagamento__forma_pagamento').annotate(itemtotal=Sum('valor')).values('itemtotal', 'forma_pagamento__forma_pagamento')
        formas_de_pagamento_ann_total = formas_de_pagamento.values('valor').aggregate(totalgeral=Sum('valor'))
    
        ingredientes = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__open_date__date__range=(data_inicial, data_final)).values('item__ingredientes__ingrediente__ingrediente').annotate(itemtotal=Sum('item__ingredientes__quantity')).values('itemtotal', 'item__ingredientes__ingrediente__ingrediente', 'item__ingredientes__medida__medida', 'item__ingredientes__ingrediente__price')
        ingredientes_total = TableItens.objects.filter(table__restaurante__restaurante_ref=rest).aggregate(total=Sum(F('item__ingredientes__quantity')*F('item__ingredientes__ingrediente__price'),output_field=FloatField()))
        
        itens_cancelados = TableItens.objects.filter(confirmed=False, table__restaurante__restaurante_ref=rest, table__open_date__date__range=(data_inicial, data_final))

        return render(request, 'tables/gerencia.html', {'total_em_aberto': total_em_aberto, 'get_local': get_local, 'total_items_agg': total_items_agg, 'total_paid_agg': total_paid_agg,
                'total_geral_paid': total_geral_paid, 'total_geral_open':total_geral_open, 'mesas_em_aberto_ann': mesas_em_aberto_ann,
                'mesas_fechadas_ann': mesas_fechadas_ann, 'mesas_fechadas_ann_total': mesas_fechadas_ann_total, 
                'vendas_por_atendente': vendas_por_atendente, 'formas_de_pagamento_ann': formas_de_pagamento_ann,
                'formas_de_pagamento_ann_total': formas_de_pagamento_ann_total, 'ingredientes': ingredientes, 
                'ingredientes_total': ingredientes_total, 'data_inicial': data_inicial, 'data_final': data_final, 'mesas_fechadas': mesas_fechadas, 'tables_pagas': tables_pagas, 'itens_cancelados': itens_cancelados})

    else:
        try:
            opendate = get_object_or_404(OpenDate, restaurante=get_local, opened=True)
            data_inicial = opendate.date
            data_final = opendate.date
            total_em_aberto = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True, table__open_date__date__range=(data_inicial, data_final))
            total_items_agg = total_em_aberto.values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')
            total_geral_open = total_em_aberto.values('price').aggregate(totalgeral=Sum('price'))
            
            total_fechado = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final))
            total_paid_agg = total_fechado.values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')
            total_geral_paid = total_fechado.values('price').aggregate(totalgeral=Sum('price'))
            
            mesas_em_aberto = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True, table__open_date__date__range=(data_inicial, data_final))
            mesas_em_aberto_ann = mesas_em_aberto.values('table__table_number__table_number').annotate(itemtotal=Sum('price')).values('itemtotal', 'table__table_number__table_number', 'table__atendentes__atendente__first_name')
        
            tables_pagas = TableItens.objects.filter(table__paid=True, table__restaurante__restaurante_ref=rest).values('table__table_check_number').annotate(total=Sum('item__price')).values('total', 'table__table_check_number', 'table__table_number__table_number', 'table__updated_at', 'table__created_at', 'table__atendente__first_name').order_by('-table__updated_at')

            mesas_fechadas = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final)).annotate(itemtotal=Sum('price')).values('itemtotal', 'table', 'table__table_number__table_number', 'table__atendentes__atendente__first_name', 'table__created_at', 'table__updated_at')
            mesas_fechadas_ann = mesas_fechadas.values('table').annotate(itemtotal=Sum('price')).values('itemtotal', 'table', 'table__table_number__table_number', 'table__atendentes__atendente__first_name', 'table__created_at', 'table__updated_at')
            mesas_fechadas_ann_total = mesas_fechadas.values('price').aggregate(totalgeral=Sum('price'))
        
            vendas_por_atendente = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__open_date__date__range=(data_inicial, data_final)).values('table__atendentes__atendente__first_name').annotate(itemtotal=Sum('price')).values('itemtotal', 'table__atendentes__atendente__first_name')
        
            formas_de_pagamento = ValoresCaixa.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=True, table__open_date__date__range=(data_inicial, data_final))
            formas_de_pagamento_ann = formas_de_pagamento.values('forma_pagamento__forma_pagamento').annotate(itemtotal=Sum('valor')).values('itemtotal', 'forma_pagamento__forma_pagamento')
            formas_de_pagamento_ann_total = formas_de_pagamento.values('valor').aggregate(totalgeral=Sum('valor'))
        
            ingredientes = TableItens.objects.filter(confirmed=True, table__restaurante__restaurante_ref=rest, table__open_date__date__range=(data_inicial, data_final)).values('item__ingredientes__ingrediente__ingrediente').annotate(itemtotal=Sum('item__ingredientes__quantity')).values('itemtotal', 'item__ingredientes__ingrediente__ingrediente', 'item__ingredientes__medida__medida', 'item__ingredientes__ingrediente__price')
            ingredientes_total = TableItens.objects.filter(table__restaurante__restaurante_ref=rest).aggregate(total=Sum(F('item__ingredientes__quantity')*F('item__ingredientes__ingrediente__price'),output_field=FloatField()))
            form = DateForm()
            
            itens_cancelados = TableItens.objects.filter(confirmed=False, table__restaurante__restaurante_ref=rest, table__open_date__date__range=(data_inicial, data_final))

            return render(request, 'tables/gerencia.html', {'total_em_aberto': total_em_aberto, 'get_local': get_local, 'form': form, 'total_items_agg': total_items_agg, 'total_paid_agg': total_paid_agg,
                'total_geral_paid': total_geral_paid, 'total_geral_open':total_geral_open, 'mesas_em_aberto_ann': mesas_em_aberto_ann,
                'mesas_fechadas_ann': mesas_fechadas_ann, 'mesas_fechadas_ann_total': mesas_fechadas_ann_total, 
                'vendas_por_atendente': vendas_por_atendente, 'formas_de_pagamento_ann': formas_de_pagamento_ann,
                'formas_de_pagamento_ann_total': formas_de_pagamento_ann_total, 'ingredientes': ingredientes, 
                'ingredientes_total': ingredientes_total, 'itens_cancelados': itens_cancelados, 'data_inicial': data_inicial, 'data_final': data_final})

        except:
            form = DateForm()
            return render(request, 'tables/gerencia.html', {"form": form, 'get_local': get_local})



# BELOW THIS NOT READY YET
@login_required
def ClienteAguardandoConta(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.values('item_user').annotate(total=Sum('item__price')).annotate(counter=Count('item_user')).values('total', 'item_user__first_name')
    
    return render(request, 'tables/cliente-aguarda-conta.html', {'obj':obj, 'tableuser': tableuser, 'user_check':user_check, 'table_items_total': table_items_total, 'table_items': table_items})


@login_required
def GarcomVerAguardandoConta(request, rest, id):
    obj = get_object_or_404(Table, paid=False, pagamento_solicitado=True, table_check_number=id)
    table_items_total = TableItens.objects.values('item_user').annotate(total=Sum('item__price')).annotate(counter=Count('item_user')).values('total', 'item_user__first_name')
    
    return render(request, 'tables/garcom-ver-aguardando-conta.html', {'obj':obj, 'table_items_total': table_items_total})


@login_required
def GarcomConfirmacaoFecharConta(request, rest, id):
    obj = get_object_or_404(Table, paid=False, pagamento_solicitado=True, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.annotate(total=Sum('item__price')).values('total')
    return render(request, 'tables/garcom-confirmacao-fechar-conta.html', {'obj':obj, 'tableuser': tableuser, 'user_check':user_check, 'table_items_total': table_items_total, 'table_items': table_items})


@login_required
def GarcomConfirmadoFecharConta(request, rest, id):
    obj = get_object_or_404(Table, paid=False, pagamento_solicitado=True, table_check_number=id)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.annotate(total=Sum('item__price')).values('total')
    table_check = get_object_or_404(TableNumber, pk=obj.table_number.id)
    table_check.openstatus = False
    obj.garcom_confirmado_pagamento = True
    obj.save()
    table_check.save()
    return redirect('view-tables-atendente', rest=rest)


@login_required
def GarcomVerConta(request, rest, id):
    obj = get_object_or_404(Table, paid=False, table_check_number=id)
    mesa_check = get_object_or_404(Table, pagamento_solicitado_code=obj.pagamento_solicitado_code)
    tableuser = TableUser.objects.filter(table__table_check_number=id)
    user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    table_items = TableItens.objects.filter(table__table_check_number=id)
    table_items_total = TableItens.objects.values('item_user').annotate(total=Sum('item__price')).annotate(counter=Count('item_user')).values('total', 'item_user__first_name')
    
    return render(request, 'tables/cliente-aguarda-conta.html', {'obj':obj, 'tableuser': tableuser, 'user_check':user_check, 'table_items_total': table_items_total, 'table_items': table_items})


# DESCONTINUED

# @login_required
# def PessoasNoLocal(request, rest, id):

#     obj = get_object_or_404(Table, table_number__table_ref=id, paid=False, restaurante__restaurante_ref=rest)
#     itensmenu = ItensMenu.objects.all()
#     tableuser = TableUser.objects.filter(table__table_check_number=id)

#     return render(request, 'tables/mesa.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser})


  # @login_required
# def PreNewTableItemClienteConfirmed(request, rest, id, item):    
#     obj = get_object_or_404(Table, paid=False, pagamento_solicitado=False, table_check_number=id)
#     itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
#     itensbebidas = itensmenu.filter(categoria=2)
#     itenspratos = itensmenu.filter(categoria=1)
#     itensdrinks = itensmenu.filter(categoria=3)
#     itenssobremesas = itensmenu.filter(categoria=4)
#     categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
#     categbebidas = categ.filter(categoria=2)
#     tableuser = TableUser.objects.filter(table__table_check_number=id)
#     user_check = TableUser.objects.filter(table=obj, table_user=request.user)
#     no_local = TableUser.objects.all()
#     itensmenucheck = get_object_or_404(ItensMenu, pk=item)
#     tableitems = TableItens.objects.filter(table=obj)    
#     item_coder = create_ref_code()
#     TableItens.objects.create(table=obj, item_user=request.user, item=itensmenucheck, confirmed=True, item_code=item_coder)    

#     # return redirect('entrar-mesa-cliente', rest=rest, id=id, cliente=request.user.id)
#     return redirect('entrar-mesa', rest=rest, id=id)
    

# @login_required
# def PreNewTableItemGarconConfirmed(request, rest, id, item):
#     get_table = get_object_or_404(Table, paid=False, table_check_number=id)
#     get_item = get_object_or_404(ItensMenu, pk=item)
#     tableitems = TableItens.objects.filter(table=obj)    
#     item_coder = create_ref_code()
#     TableItens.objects.create(table=get_table, item_user=request.user, item=get_item, confirmed=True, item_code=item_coder)    

    # itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
    # itensbebidas = itensmenu.filter(categoria=2)
    # itenspratos = itensmenu.filter(categoria=1)
    # itensdrinks = itensmenu.filter(categoria=4)
    # itenssobremesas = itensmenu.filter(categoria=3)
    # categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    # categbebidas = categ.filter(categoria=2)
    # tableuser = TableUser.objects.filter(table__table_check_number=id)
    # user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    # no_local = TableUser.objects.all()
    
    # return redirect('entrar-mesa-garcom', rest=rest, id=id, atend=request.user.id )


# @login_required
# def NewTableItem(request, rest, id, item):
#     obj = get_object_or_404(Table, paid=False, table_check_number=id)
#     itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
#     TableItens.objects.create(table=obj, item_user=request.user, item=itensmenucheck)
#     tableitems = TableItens.objects.filter(table=obj)
#     table_items_total = TableItens.objects.values('item_user').annotate(total=Sum('item__price'), counter=Count('item_user')).values('total', 'item_user')

#     return redirect('entrar-mesa', rest=rest, id=id)


# @login_required
# def NewTableItemGarcom(request, rest, id, item, pk):
#     obj = get_object_or_404(Table, paid=False, restaurante__restaurante_ref=rest, table_check_number=id)
#     itensmenucheck = get_object_or_404(TableItens, pk=pk)
#     itensmenucheck.garconconfirmed = True
#     itensmenucheck.save()
    # itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
    # tableitems = TableItens.objects.filter(table=obj)
    # table_items_total = TableItens.objects.values('item_user').annotate(total=Sum('item__price'), counter=Count('item_user')).values('total', 'item_user')
    # itensbebidas = itensmenu.filter(categoria=2)
    # itenspratos = itensmenu.filter(categoria=1)
    # itensdrinks = itensmenu.filter(categoria=3)
    # itenssobremesas = itensmenu.filter(categoria=4)
    # categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    # categbebidas = categ.filter(categoria=2)
    # tableuser = TableUser.objects.filter(table__table_check_number=id)
    # user_check = TableUser.objects.filter(table=obj, table_user=request.user)
    # no_local = TableUser.objects.all()
    # TableItens.objects.create(table=obj, item_user=request.user, item=itensmenucheck)
    # return render(request, 'tables/mesa.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 'no_local': no_local, 'user_check': user_check, 'categbebidas': categbebidas, 'itensbebidas':itensbebidas, 'itenspratos': itenspratos, 'itenssobremesas': itenssobremesas, 'itensdrinks': itensdrinks, 'tableitems':tableitems, 'user_check': user_check, 'table_items_total':table_items_total})
    # return redirect('view-tables-atendente', rest=rest)



    # @login_required
# def EntrarMesaGarcom(request, rest, atend, id):
#     obj = get_object_or_404(Table, table_check_number=id, paid=False, restaurante__restaurante_ref=rest, atendentes__atendente_code=atend)
#     itensmenu = ItensMenu.objects.all()
#     tableuser = TableUser.objects.filter(table__table_check_number=id)
#     itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest, status=True)
#     ct1 = itensmenu.filter(categoria__ordem_categoria=1)
#     ct2 = itensmenu.filter(categoria__ordem_categoria=2)
#     ct3 = itensmenu.filter(categoria__ordem_categoria=3)
#     ct4 = itensmenu.filter(categoria__ordem_categoria=4)
#     categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
#     categbebidas = categ.filter(categoria=2)
#     tableuser = TableUser.objects.filter(table__table_check_number=id)
#     user_check = TableUser.objects.filter(table=obj, table_user=request.user)
#     no_local = TableUser.objects.all()
#     tableitems = TableItens.objects.filter(table=obj).order_by('-id')
#     table_items_total = TableItens.objects.filter(table=obj).values('item_user').annotate(total=Sum('item__price')).values('total', 'item_user')

#     return render(request, 'tables/mesa_garcom.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 'no_local': no_local, 'user_check': user_check, 'categbebidas': categbebidas, 'itensbebidas': ct2, 'itenspratos': ct1, 'itenssobremesas': ct4, 'itensdrinks': ct3, 'tableitems':tableitems, 'user_check': user_check, 'table_items_total':table_items_total})

# @login_required
# def solicitacoesAtendenteView(request, rest, atendente):
#     get_atendente = get_object_or_404(AtendentesRestaurante, code=atendente, restaurante__restaurante_ref=rest, status=True)
#     itens_confirmados = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendentes__code=atendente, confirmed=True).order_by('-created_at')
#     all_tables = Table.objects.filter(restaurante__restaurante_ref=rest, paid=False)
#     tables_atendente = all_tables.filter(atendentes__code=atendente)
#     tables_conta = all_tables.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False, atendentes__code=atendente)
#     tables_available = TableNumber.objects.filter(openstatus=False, restaurante__restaurante_ref=rest).order_by('table_number')
#     timenow = datetime.now()
    
    # table_atendente = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user, confirmed=True, garconconfirmed=False).order_by('-created_at')
    # # restaurante = get_object_or_404(Restaurante, restaurante_ref=rest)
    # restaurante = get_object_or_404(AtendentesRestaurante, restaurante__restaurante_ref=rest, atendente=request.user, status=True)
    # tables_conta = Table.objects.filter(pagamento_solicitado=True, garcom_confirmado_pagamento=False)
    # itens_na_cozinha = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user, cozinha_to_garcon=False, garcon_to_cozinha=True)
    # itens_no_bar = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, table__atendente=request.user, bar_to_garcon=False, garcon_to_bar=True)
    # timenow = datetime.now()
    # return render(request, 'tables/solicitacoes-atendente.html', {'tables_atendente': tables_atendente, 'tables_conta': tables_conta, 'itens_na_cozinha': itens_na_cozinha, 'itens_no_bar': itens_no_bar, 'timenow': timenow})


# @login_required
# def viewTablesPraca1(request, rest):
#     nova_solicitacao = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, garconconfirmed=False).order_by('-created_at')
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     return render(request, 'tables/praca-solicitacoes.html', {'nova_solicitacao': nova_solicitacao})


# @login_required
# def viewTablesPraca1Aceite(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca1_aceite=True
#     item.save()
#     return redirect('view-tables-praca1', rest=rest)


# @login_required
# def viewTablesPraca1Entrega(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca1_entrega=True
#     item.save()
#     return redirect('view-tables-praca1', rest=rest)


# @login_required
# def viewTablesPraca1AceiteDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca1_aceite=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def viewTablesPraca1EntregaDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca1_entrega=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def viewTablesPraca2(request, rest):
#     nova_solicitacao = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, garconconfirmed=False).order_by('-created_at')
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=2, status=True)
#     return render(request, 'tables/praca-2-solicitacoes.html', {'nova_solicitacao': nova_solicitacao})


# @login_required
# def viewTablesPraca2Aceite(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=2, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca2_aceite=True
#     item.save()
#     return redirect('view-tables-praca2', rest=rest)


# @login_required
# def viewTablesPraca2Entrega(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=2, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca2_entrega=True
#     item.save()
#     return redirect('view-tables-praca2', rest=rest)


# @login_required
# def viewTablesPraca2AceiteDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca2_aceite=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def viewTablesPraca2EntregaDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=1, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca2_entrega=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def viewTablesPraca3(request, rest):
#     nova_solicitacao = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, garconconfirmed=False).order_by('-created_at')
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=3, status=True)
#     return render(request, 'tables/praca-3-solicitacoes.html', {'nova_solicitacao': nova_solicitacao})


# @login_required
# def viewTablesPraca3Aceite(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=3, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca3_aceite=True
#     item.save()
#     return redirect('view-tables-praca3', rest=rest)


# @login_required
# def viewTablesPraca3Entrega(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=3, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca3_entrega=True
#     item.save()
#     return redirect('view-tables-praca3', rest=rest)


# @login_required
# def viewTablesPraca3AceiteDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=3, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca3_aceite=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def viewTablesPraca3EntregaDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=3, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca3_entrega=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)



# @login_required
# def viewTablesPraca4(request, rest):
#     nova_solicitacao = TableItens.objects.filter(table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest, garconconfirmed=False).order_by('-created_at')
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=4, status=True)
#     return render(request, 'tables/praca-4-solicitacoes.html', {'nova_solicitacao': nova_solicitacao})


# @login_required
# def viewTablesPraca4Aceite(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=4, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca4_aceite=True
#     item.save()
#     return redirect('view-tables-praca4', rest=rest)


# @login_required
# def viewTablesPraca4Entrega(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=4, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca4_entrega=True
#     item.save()
#     return redirect('view-tables-praca4', rest=rest)


# @login_required
# def viewTablesPraca4AceiteDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=4, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca4_aceite=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def viewTablesPraca4EntregaDirect(request, rest, id, item):
#     restaurante_praca = get_object_or_404(PracasUser, restaurante__restaurante_ref=rest, praca_user=request.user, praca=4, status=True)
#     item = get_object_or_404(TableItens, id=item, table__table_number__openstatus=True, table__restaurante__restaurante_ref=rest)
#     item.praca4_entrega=True
#     item.save()
#     return redirect('view-tables-cozinha', rest=rest)


# @login_required
# def Praca1View(request):
#     restaurantes = PracasUser.objects.filter(praca_user=request.user.id)
#     return render(request, 'tables/praca1-view.html', {'restaurantes': restaurantes})


# @login_required
# def Praca2View(request):
#     restaurantes = PracasUser.objects.filter(praca_user=request.user.id)
#     return render(request, 'tables/praca2-view.html', {'restaurantes': restaurantes})


# @login_required
# def Praca3View(request):
#     restaurantes = PracasUser.objects.filter(praca_user=request.user.id)
#     return render(request, 'tables/praca3-view.html', {'restaurantes': restaurantes})


# @login_required
# def Praca4View(request):
#     restaurantes = PracasUser.objects.filter(praca_user=request.user.id)
#     return render(request, 'tables/praca4-view.html', {'restaurantes': restaurantes})

# @login_required
# def TableView(request, id):
#     id = id
#     obj = Table.objects.get(pk=id, paid=False)
    
#     return render(request, 'tables/qrcode.html', {'obj': obj})



# @login_required
# def EntrarMesa(request, rest, id):
#     obj = get_object_or_404(Table, paid=False, table_check_number=id, restaurante__restaurante_ref=rest)
#     itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
#     itensbebidas = itensmenu.filter(categoria=2)
#     itenspratos = itensmenu.filter(categoria=1)
#     itensdrinks = itensmenu.filter(categoria=3)
#     itenssobremesas = itensmenu.filter(categoria=4)
#     # itensmenu = ItensMenu.objects.all()
#     tableuser = TableUser.objects.filter(table__table_check_number=id)
#     no_local = TableUser.objects.all()
#     user_check = TableUser.objects.filter(table=obj, table_user=request.user)

#     return render(request, 'tables/mesa.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 'no_local': no_local, 'user_check': user_check, 'itensbebidas':itensbebidas, 'itenspratos': itenspratos, 'itenssobremesas': itenssobremesas, 'itensdrinks': itensdrinks})


# @login_required
# def PreNewTableItemGarcom(request, rest, id, item):
#     obj = get_object_or_404(Table, paid=False, table_check_number=id)
#     itensmenu = ItensMenu.objects.filter(menu__restaurante__restaurante_ref=rest)
#     itensbebidas = itensmenu.filter(categoria=2)
#     itenspratos = itensmenu.filter(categoria=1)
#     itensdrinks = itensmenu.filter(categoria=3)
#     itenssobremesas = itensmenu.filter(categoria=4)
#     categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
#     categbebidas = categ.filter(categoria=2)
#     tableuser = TableUser.objects.filter(table__table_check_number=id)
#     user_check = TableUser.objects.filter(table=obj, table_user=request.user)
#     no_local = TableUser.objects.all()
#     itensmenucheck = get_object_or_404(ItensMenu, pk=item)
#     tableitems = TableItens.objects.filter(table=obj)

#     return render(request, 'tables/confirmaritem-garcom.html', {'obj': obj, 'itensmenu': itensmenu, 'tableuser': tableuser, 'no_local': no_local, 'user_check': user_check, 'categbebidas': categbebidas, 'itensbebidas':itensbebidas, 'itenspratos': itenspratos, 'itenssobremesas': itenssobremesas, 'itensdrinks': itensdrinks, 'tableitems':tableitems, 'itensmenucheck':itensmenucheck})

# def gerencia_by_date(request, rest):
#     if request.method == "POST":
#         data_inicial = request.POST.get('data_inicial')
#         data_final = request.POST.get('data_final')
#         total_em_aberto = TableItens.objects.raw('select * where created_at between "'+data_inicial+'" and "'+data_final+'"')
#         return render(request, 'tables/gerencia.html',{'total_em_aberto': total_em_aberto})
    
#     total_em_aberto = TableItens.objects.raw(table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True)
#     total_items_agg = total_em_aberto.values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')
#     total_geral_open = total_em_aberto.values('price').aggregate(totalgeral=Sum('price'))
#     total_fechado = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=True)
#     total_paid_agg = total_fechado.values('item__item', 'price').annotate(itemtotal=Sum('price')).annotate(itemcounter=Count('item')).values('item__item', 'itemtotal', 'itemcounter')
#     total_geral_paid = total_fechado.values('price').aggregate(totalgeral=Sum('price'))
#     mesas_em_aberto = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=False, table__table_number__openstatus=True)
#     mesas_em_aberto_ann = mesas_em_aberto.values('table__table_number__table_number').annotate(itemtotal=Sum('price')).values('itemtotal', 'table__table_number__table_number', 'table__atendentes__atendente__first_name')
#     mesas_fechadas = TableItens.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=True)
#     mesas_fechadas_ann = mesas_fechadas.values('table').annotate(itemtotal=Sum('price')).values('itemtotal', 'table', 'table__table_number__table_number', 'table__atendentes__atendente__first_name', 'table__created_at', 'table__updated_at')
#     mesas_fechadas_ann_total = mesas_fechadas.values('price').aggregate(totalgeral=Sum('price'))
#     vendas_por_atendente = TableItens.objects.filter(table__restaurante__restaurante_ref=rest).values('table__atendentes__atendente__first_name').annotate(itemtotal=Sum('price')).values('itemtotal', 'table__atendentes__atendente__first_name')
#     formas_de_pagamento = ValoresCaixa.objects.filter(table__restaurante__restaurante_ref=rest, table__paid=True)
#     formas_de_pagamento_ann = formas_de_pagamento.values('forma_pagamento__forma_pagamento').annotate(itemtotal=Sum('valor')).values('itemtotal', 'forma_pagamento__forma_pagamento')
#     formas_de_pagamento_ann_total = formas_de_pagamento.values('valor').aggregate(totalgeral=Sum('valor'))
#     ingredientes = TableItens.objects.values('item__ingredientes__ingrediente__ingrediente').annotate(itemtotal=Sum('item__ingredientes__quantity')).values('itemtotal', 'item__ingredientes__ingrediente__ingrediente', 'item__ingredientes__medida__medida', 'item__ingredientes__ingrediente__price')
#     ingredientes_total = TableItens.objects.filter(table__restaurante__restaurante_ref=rest).aggregate(total=Sum(F('item__ingredientes__quantity')*F('item__ingredientes__ingrediente__price'),output_field=FloatField()))
#     get_local = get_object_or_404(Restaurante, restaurante_ref=rest)

#     return render(request, 'tables/gerencia.html', {'total_em_aberto': total_em_aberto, 'get_local': get_local, 'dates': dates, 'form': form, 'total_items_agg': total_items_agg, 'total_paid_agg': total_paid_agg,
#         'total_geral_paid': total_geral_paid, 'total_geral_open':total_geral_open, 'mesas_em_aberto_ann': mesas_em_aberto_ann,
#         'mesas_fechadas_ann': mesas_fechadas_ann, 'mesas_fechadas_ann_total': mesas_fechadas_ann_total, 
#         'vendas_por_atendente': vendas_por_atendente, 'formas_de_pagamento_ann': formas_de_pagamento_ann,
#         'formas_de_pagamento_ann_total': formas_de_pagamento_ann_total, 'ingredientes': ingredientes, 
#         'ingredientes_total': ingredientes_total})


