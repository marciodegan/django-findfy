from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum, Q, Count

import uuid
from datetime import datetime, timedelta

from restaurantes.models import Restaurante, AtendentesRestaurante, AtendentesMaster, CaixasRestaurante, BarmanRestaurante, GerenteRestaurante, CozinhaRestaurante, Site, GoogleImport, Cardapio, Ordering, OpenDate
from menus.models import ItensMenu, CategoriasMenu, Menu, IngredientesItem, CategoriaOrdering, Ingredientes, Medida
from profiles.models import UserProfile, Liker
from mensagens.models import EnviarMensagem
from tables.models import TableUser, TableNumber, FormaDePagamento

from .forms import NewRestauranteForm, NewTableForm, NewCategoriaForm, NewMenuForm, NewProdutoForm, EditProdutoForm, NewAtendenteForm, NewAtendenteMasterForm, NewCozinhaForm, NewBarForm, EditLocalForm, NewLogoForm, NewAddressForm, NewPhotoBackForm, NewCaixaForm, NewPhotoForm, OpenDateForm

# import random
# import string


@login_required
def localPageView(request, rest, mesa):
    obj = Restaurante.objects.get(restaurante_ref=rest)
    who_is_here = TableUser.objects.filter(table__paid=False, table__restaurante__restaurante_ref=rest, table__table_number__openstatus=True)
    code = Cardapio.objects.get(restaurante__restaurante_ref=rest)
    instagram_profile_name = obj.instagram_profile_name
    like_check = Liker.objects.filter(like_from=request.user)
    like = like_check.filter(curtida=True)
    like_anonimo = like_check.filter(like_anonimo=True)
    return render(request, 'restaurantes/local-page.html', {'obj': obj, 'who_is_here': who_is_here, 'code': code, 'instagram_profile_name': instagram_profile_name, 'like': like, 'like_anonimo': like_anonimo, 'mesa': mesa})


@login_required
def indexLocal(request):
    locais = Restaurante.objects.filter(user=request.user.id, deactivate=False)
    UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NewRestauranteForm(request.POST, request.FILES)

        try: 
            if form.is_valid():
                local = form.save(commit=False)
                local.user = request.user
                local.save()
                return redirect('/local')
        except:
            return redirect('/local')
            
    else:
        form = NewRestauranteForm()
    
        return render(request, 'restaurantes/index-local.html', {'locais': locais, 'form': form})

        # return render(request, 'restaurantes/create-local.html', {'form': form})


@login_required
def local(request, rest):
    get_local = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user.id)
    form = NewPhotoForm()

    if request.method == 'POST':
        form = NewPhotoForm(request.POST or None, request.FILES or None, instance=get_local)
    
        if form.is_valid():
            form.save()

            return redirect('local', rest=rest)
    else:
        try: 
            get_atendente = get_object_or_404(AtendentesRestaurante, restaurante__restaurante_ref=rest, atendente=request.user.id)
            get_atendente_master = get_object_or_404(AtendentesMaster, restaurante__restaurante_ref=rest, atendentemaster=request.user.id)
            get_menu = get_object_or_404(Cardapio, restaurante__restaurante_ref=rest)
            form = NewPhotoForm()
            open_date_check = OpenDate.objects.filter(restaurante__restaurante_ref=rest, opened=True)
            open_date_form = OpenDateForm()

            return render(request, 'restaurantes/local.html', {'get_local': get_local, 'get_atendente': get_atendente, 'get_menu': get_menu, 'get_atendente_master': get_atendente_master, 'form': form, 'open_date_form': open_date_form, 'open_date_check': open_date_check })
        except:
            return render(request, 'restaurantes/local.html', {'get_local': get_local, 'form': form})


@login_required
def fecharLocal(request, rest, id):
    try:
        get_instance = get_object_or_404(OpenDate, restaurante__restaurante_ref=rest, restaurante__user=request.user, pk=id)
        get_instance.opened = False
        get_instance.save()
        return redirect('local', rest=rest)
    except:
        return redirect('local', rest=rest)


@login_required
def createDate(request, rest):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
        
    if request.method == 'POST':
        date = request.POST.get('jqueryDate')
        data = datetime.strptime(date, '%d/%m/%Y')

        try:
            get_date = get_object_or_404(OpenDate, date=data, restaurante=local)
            get_date.opened = True
            get_date.save()
            return redirect('local', rest=rest)

        except:
            open_date = OpenDate.objects.get_or_create(date=data, restaurante=local, opened=True)
 
    return redirect('local', rest=rest)


@login_required
def createLocal(request):
         
    if request.method == 'POST':
        form = NewRestauranteForm(request.POST, request.FILES)
        
        if form.is_valid():
            local = form.save(commit=False)
            local.user = request.user
            local.save()
            return redirect('/local')
    
    else:
        form = NewRestauranteForm()
    
        return render(request, 'restaurantes/create-local.html', {'form': form})

# REVIEW THIS
@login_required
def createLocalPost(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        nome = request.POST.get('nome')
        
        Restaurante.objects.create(name=nome, user=request.user)    

        response_data['nome'] = nome        
    
    return HttpResponse('ok')


@login_required
def editPhoto(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest, user=request.user)
    form = NewLogoForm(instance=local)

    if request.method == 'POST':
        form = NewLogoForm(request.POST, request.FILES, instance=local)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('view-cardapio-fybasic', rest=rest)


@login_required
def editPhotoBack(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest, user=request.user)
    form = NewPhotoBackForm(instance=local)

    if request.method == 'POST':
        form = NewPhotoBackForm(request.POST, request.FILES, instance=local)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('view-cardapio-fybasic', rest=rest)


@login_required
def editAddress(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest, user=request.user)
    form = NewAddressForm(instance=local)

    if request.method == 'POST':
        form = NewAddressForm(request.POST, instance=local)

        if form.is_valid():
            address = form.save(commit=False)
            address.save()
            return redirect('view-cardapio-fybasic', rest=rest)


@login_required
def editLocal(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest, user=request.user)
    form = EditLocalForm(instance=local)

    if request.method == 'POST':
        form = EditLocalForm(request.POST, request.FILES, instance=local)        
        if form.is_valid():
            local = form.save(commit=False)
            local.save()
            return redirect('local', rest=local.restaurante_ref)
           
    else:
    
        return render(request, 'restaurantes/edit-local.html', {'form': form})


    
# CADASTRO MESA
@login_required
def createTable(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref=rest)
    list = TableNumber.objects.filter(restaurante__restaurante_ref=rest).order_by('table_number')
    if request.method == 'POST':
        form = NewTableForm(request.POST)
        
        if form.is_valid():
            try: 
                table = form.save(commit=False)
                table.restaurante = local
                table.save()
                return redirect('create-mesa', rest=rest)
            except:
                return HttpResponse('Mesa não criada. Possivelmente por já existir mesa com este número. Retorne e tente novamente.')
    else:
        form = NewTableForm()
    
        return render(request, 'restaurantes/create-mesa.html', {'form': form, 'list': list, 'local': local})



@login_required
def deleteMesa(request, rest, id):
    try:
        get_instance = get_object_or_404(TableNumber, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user, openstatus=False)
        get_instance.delete()
        return redirect('create-mesa', rest=rest)
    except:
        return redirect('create-mesa', rest=rest)


# CADASTRO CATEGORIA MENU
@login_required
def createCategoria(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref=rest)
    if request.method == 'POST':
        form = NewCategoriaForm(request.POST)
        
        if form.is_valid():
            try: 
                categoria = form.save(commit=False)
                categoria.restaurante = local
                categoria.save()
                return redirect('create-categoria', rest=rest)
            except:
                return HttpResponse('Não foi possivel, provavelmente uma categoria com esta ordem já existe.')
    else:
        form = NewCategoriaForm()
        list = CategoriasMenu.objects.filter(restaurante__restaurante_ref=rest)
    
        return render(request, 'restaurantes/create-categoria.html', {'form': form,'list': list, 'local': local})


@login_required
def deleteCategoria(request, rest, id):
    try:
        get_instance = get_object_or_404(CategoriasMenu, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        get_instance.delete()
        return redirect('create-categoria', rest=rest)
    except:
        return redirect('create-categoria', rest=rest)


# CADASTRO MENU
@login_required
def createMenu(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref=rest)

    if request.method == 'POST':
        form = NewMenuForm(request.POST)
        
        if form.is_valid():
            try: 
                menu = form.save(commit=False)
                menu.restaurante = local
                menu.save()
                return redirect('create-menu', rest=rest)
            except:
                return HttpResponse('Não foi possivel.')
    else:
        form = NewMenuForm()
        menus = Menu.objects.filter(restaurante__restaurante_ref=rest).order_by('nome')
    
        return render(request, 'restaurantes/create-menu.html', {'form': form, 'menus': menus, 'local': local})


@login_required
def deleteMenu(request, rest, id):
    try:
        get_instance = get_object_or_404(Menu, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        get_instance.delete()
        return redirect('create-menu', rest=rest)
    except:
        return redirect('create-menu', rest=rest)


# CADASTRO PRODUTO
@login_required
def createProduto(request, rest):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    list = ItensMenu.objects.filter(restaurante__restaurante_ref=rest).order_by('item')

    if request.method == 'POST':
        form = NewProdutoForm(local, request.POST, request.FILES)
        
        if form.is_valid():
            produto = form.save(commit=False)
            produto.restaurante = local
            produto.save()
            form.save_m2m()
            return redirect('create-produto', rest=rest)
           
    else:
        form = NewProdutoForm(local)
        return render(request, 'restaurantes/create-produto.html', {'form': form, 'list': list, 'local': local})


@login_required
def editProduto(request, rest, id):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    produto = get_object_or_404(ItensMenu, code_id=id)
    form = EditProdutoForm(local, instance=produto)

    if request.method == 'POST':
        form = EditProdutoForm(local, request.POST, request.FILES, instance=produto)        
        if form.is_valid():
            produto = form.save(commit=False)
            produto.save()
            form.save_m2m()
            return redirect('create-produto', rest=rest)
           
    else:
    
        return render(request, 'restaurantes/edit-produto.html', {'form': form, 'produto': produto})


@login_required
def deleteProduto(request, rest, id):
    try:
        produto = get_object_or_404(ItensMenu, code_id=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        produto.delete()
        return redirect('create-produto', rest=rest)
    except:
        return redirect('create-produto', rest=rest)


# CADASTRO ATENDENTE
@login_required
def createAtendente(request, rest): 
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    list_atendentes = AtendentesRestaurante.objects.filter(restaurante__restaurante_ref=rest)

    search = request.GET.get('search')
    search = str(search).lower()
    if search:
        list = CustomUser.objects.filter(email=search)
        return render(request, 'restaurantes/create-atendente.html', {'list': list, 'local': local, 'list_atendentes': list_atendentes})

    return render(request, 'restaurantes/create-atendente.html', {'local': local, 'list_atendentes': list_atendentes})


@login_required
def addAtendente(request, rest, atendente):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente_user = CustomUser.objects.get(email=atendente)
    AtendentesRestaurante.objects.create(atendente=get_atendente_user, restaurante=get_restaurante)
    
    return redirect('create-atendente', rest=rest)


@login_required
def ativarAtendente(request, rest, id):
    try:
        atendente = get_object_or_404(AtendentesRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        if atendente.status == False:
            atendente.status = True
            atendente.save()
        else: 
            atendente.status = False
            atendente.save()    
        return redirect('create-atendente', rest=rest)
    except:
        return redirect('create-atendente', rest=rest)


@login_required
def deleteAtendente(request, rest, id):
    try:
        atendente = get_object_or_404(AtendentesRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        atendente.delete()
        return redirect('create-atendente', rest=rest)
    except:
        return redirect('create-atendente', rest=rest)


# CADASTRO ATENDENTE MASTER
@login_required
def createAtendenteMaster(request, rest):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    list_atendentes = AtendentesMaster.objects.filter(restaurante__restaurante_ref=rest)

    search = request.GET.get('search')
    search = str(search).lower()
    if search:
        list = CustomUser.objects.filter(email=search)
        return render(request, 'restaurantes/create-atendente-master.html', {'list': list, 'local': local, 'list_atendentes': list_atendentes})

    return render(request, 'restaurantes/create-atendente-master.html', {'local': local, 'list_atendentes': list_atendentes})


@login_required
def addAtendenteMaster(request, rest, atendente):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente_user = CustomUser.objects.get(email=atendente)
    AtendentesMaster.objects.create(atendentemaster=get_atendente_user, restaurante=get_restaurante)
    
    return redirect('create-atendente-master', rest=rest)


@login_required
def ativarAtendenteMaster(request, rest, id):
    try:
        atendente = get_object_or_404(AtendentesMaster, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        if atendente.status == False:
            atendente.status = True
            atendente.save()
        else: 
            atendente.status = False
            atendente.save()    
        return redirect('create-atendente-master', rest=rest)
    except:
        return redirect('create-atendente-master', rest=rest)


@login_required
def deleteAtendenteMaster(request, rest, id):
    try:
        atendente = get_object_or_404(AtendentesMaster, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        atendente.delete()
        return redirect('create-atendente-master', rest=rest)
    except:
        return redirect('create-atendente-master', rest=rest)


# CADASTRO CAIXA
@login_required
def createCaixa(request, rest):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    list_atendentes = CaixasRestaurante.objects.filter(restaurante__restaurante_ref=rest)

    search = request.GET.get('search')
    search = str(search).lower()
    if search:
        list = CustomUser.objects.filter(email=search)
        return render(request, 'restaurantes/create-caixa.html', {'list': list, 'local': local, 'list_atendentes': list_atendentes})

    return render(request, 'restaurantes/create-caixa.html', {'local': local, 'list_atendentes': list_atendentes})


@login_required
def addCaixa(request, rest, atendente):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente_user = CustomUser.objects.get(email=atendente)
    CaixasRestaurante.objects.create(caixa=get_atendente_user, restaurante=get_restaurante)
    
    return redirect('create-caixa', rest=rest)


@login_required
def ativarCaixa(request, rest, id):
    try:
        atendente = get_object_or_404(CaixasRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        if atendente.status == False:
            atendente.status = True
            atendente.save()
        else: 
            atendente.status = False
            atendente.save()    
        return redirect('create-caixa', rest=rest)
    except:
        return redirect('create-caixa', rest=rest)



@login_required
def deleteCaixa(request, rest, id):
    try:
        caixa = get_object_or_404(CaixasRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        caixa.delete()
        return redirect('create-caixa', rest=rest)
    except:
        return redirect('create-caixa', rest=rest)


# CADASTRO COZINHA
@login_required
def createCozinha(request, rest):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    list_atendentes = CozinhaRestaurante.objects.filter(restaurante__restaurante_ref=rest)

    search = request.GET.get('search')
    search = str(search).lower()
    if search:
        list = CustomUser.objects.filter(email=search)
        return render(request, 'restaurantes/create-cozinha.html', {'list': list, 'local': local, 'list_atendentes': list_atendentes})

    return render(request, 'restaurantes/create-cozinha.html', {'local': local, 'list_atendentes': list_atendentes})


@login_required
def addCozinha(request, rest, atendente):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente_user = CustomUser.objects.get(email=atendente)
    CozinhaRestaurante.objects.create(cozinha=get_atendente_user, restaurante=get_restaurante)
    
    return redirect('create-cozinha', rest=rest)


@login_required
def ativarCozinha(request, rest, id):
    try:
        atendente = get_object_or_404(CozinhaRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        if atendente.status == False:
            atendente.status = True
            atendente.save()
        else: 
            atendente.status = False
            atendente.save()    
        return redirect('create-cozinha', rest=rest)
    except:
        return redirect('create-cozinha', rest=rest)


@login_required
def deleteCozinha(request, rest, id):
    try:
        cozinha = get_object_or_404(CozinhaRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        cozinha.delete()
        return redirect('create-cozinha', rest=rest)
    except:
        return redirect('create-cozinha', rest=rest)


# CADASTRO BAR
@login_required
def createBar(request, rest):
    local = Restaurante.objects.get(restaurante_ref=rest, user=request.user)
    list_atendentes = BarmanRestaurante.objects.filter(restaurante__restaurante_ref=rest)

    search = request.GET.get('search')
    search = str(search).lower()
    if search:
        list = CustomUser.objects.filter(email=search)
        return render(request, 'restaurantes/create-bar.html', {'list': list, 'local': local, 'list_atendentes': list_atendentes})

    return render(request, 'restaurantes/create-bar.html', {'local': local, 'list_atendentes': list_atendentes})


@login_required
def addBar(request, rest, atendente):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente_user = CustomUser.objects.get(email=atendente)
    BarmanRestaurante.objects.create(barman=get_atendente_user, restaurante=get_restaurante)
    
    return redirect('create-bar', rest=rest)


@login_required
def ativarBar(request, rest, id):
    try:
        atendente = get_object_or_404(BarmanRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        if atendente.status == False:
            atendente.status = True
            atendente.save()
        else: 
            atendente.status = False
            atendente.save()    
        return redirect('create-bar', rest=rest)
    except:
        return redirect('create-bar', rest=rest)


@login_required
def deleteBar(request, rest, id):
    try:
        bar = get_object_or_404(BarmanRestaurante, pk=id, restaurante__restaurante_ref=rest, restaurante__user=request.user)
        bar.delete()
        return redirect('create-bar', rest=rest)
    except:
        return redirect('create-bar', rest=rest)


# INITIAL SETUP FOR FIRST STEPS & INSTRUCTIONS AND FOR HELP SELLING THE APP
@login_required
def gerarCardapio(request, rest):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest)
    get_ordem_categorias1 = CategoriaOrdering.objects.get(order_number=1)
    get_ordem_categorias2 = CategoriaOrdering.objects.get(order_number=2)
    get_ordem_categorias3 = CategoriaOrdering.objects.get(order_number=3)
    get_atendente_ordem1 = Ordering.objects.get(order_number=1)
    OpenDate.objects.get_or_create(date=datetime.today(), restaurante=get_restaurante, opened=True)
    Menu.objects.get_or_create(nome="Noite", restaurante=get_restaurante, ativo=True)
    FormaDePagamento.objects.get_or_create(forma_pagamento="CREDITO", restaurante=get_restaurante)
    FormaDePagamento.objects.get_or_create(forma_pagamento="DEBITO", restaurante=get_restaurante)
    FormaDePagamento.objects.get_or_create(forma_pagamento="DINHEIRO", restaurante=get_restaurante)
    FormaDePagamento.objects.get_or_create(forma_pagamento="TROCO", restaurante=get_restaurante)
    CategoriasMenu.objects.get_or_create(categoria="Pratos", restaurante=get_restaurante, ordem_categoria=get_ordem_categorias1)
    CategoriasMenu.objects.get_or_create(categoria="Bebidas", restaurante=get_restaurante, ordem_categoria=get_ordem_categorias2)
    CategoriasMenu.objects.get_or_create(categoria="Sobremesas", restaurante=get_restaurante, ordem_categoria=get_ordem_categorias3)    
    AtendentesRestaurante.objects.get_or_create(atendente=get_restaurante.user, restaurante=get_restaurante, status=True, ordering=get_atendente_ordem1)
    AtendentesMaster.objects.get_or_create(atendentemaster=get_restaurante.user, restaurante=get_restaurante, status=True)
    CozinhaRestaurante.objects.get_or_create(cozinha=get_restaurante.user, restaurante=get_restaurante, status=True)
    BarmanRestaurante.objects.get_or_create(barman=get_restaurante.user, restaurante=get_restaurante, status=True)
    CaixasRestaurante.objects.get_or_create(caixa=get_restaurante.user, restaurante=get_restaurante, status=True)
    GerenteRestaurante.objects.get_or_create(gerente=get_restaurante.user, restaurante=get_restaurante, status=True)
    TableNumber.objects.get_or_create(table_number=1, restaurante=get_restaurante)
    TableNumber.objects.get_or_create(table_number=2, restaurante=get_restaurante)
    TableNumber.objects.get_or_create(table_number=3, restaurante=get_restaurante)
    ItensMenu.objects.get_or_create(item="Cerveja Heineken 600ml", descricao="Nossas verdinhas estão sempre gelada", name_image= "menu/cervejaheineken.jpeg", restaurante=get_restaurante, price=14, status=True)
    ItensMenu.objects.get_or_create(item="Marguerita", descricao="O drink mais pedido da casa. Feito c/ Tequila José Cuervo.", name_image= "menu/marguerita.jpg", restaurante=get_restaurante, price=19, status=True, bar=True)
    ItensMenu.objects.get_or_create(item="Petit Gateau", descricao="Bolinho fofinho c/ calda de chocolate deliciosa. Você vai amar!", name_image= "menu/petitgateau.jpeg", restaurante=get_restaurante, price=13.9, cozinha=True, status=True)
    ItensMenu.objects.get_or_create(item="Filet Trinchado", descricao="Acompanha arroz e fritas. Serve bem 2 pessoas", name_image= "menu/filetparme.jpeg", restaurante=get_restaurante, price=69, status=True, cozinha=True)    
    UserProfile.objects.get_or_create(user=get_restaurante.user)
    categorias1 = CategoriasMenu.objects.get(ordem_categoria=1, restaurante=get_restaurante)
    categorias2 = CategoriasMenu.objects.get(ordem_categoria=2, restaurante=get_restaurante)
    categorias3 = CategoriasMenu.objects.get(ordem_categoria=3, restaurante=get_restaurante)
    menu = Menu.objects.get(nome="Noite", restaurante=get_restaurante)
    
    Medida.objects.get_or_create(medida="grama", restaurante=get_restaurante)
    Medida.objects.get_or_create(medida="unid", restaurante=get_restaurante)
    Medida.objects.get_or_create(medida="ml", restaurante=get_restaurante)
    medida_grama = Medida.objects.get(medida="grama", restaurante=get_restaurante)
    medida_un = Medida.objects.get(medida="unid", restaurante=get_restaurante)
    medida_ml = Medida.objects.get(medida="ml", restaurante=get_restaurante)
    
    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Filé", price=0.07)    
    ingredientes1 = Ingredientes.objects.get(ingrediente="Filé", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes1, quantity=200, medida=medida_grama, restaurante=get_restaurante)
    ingrediente_1 = IngredientesItem.objects.get(ingrediente=ingredientes1, restaurante=get_restaurante)
    
    for i in ItensMenu.objects.filter(item="Filet Trinchado", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_1.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Arroz", price=0.005)    
    ingredientes2 = Ingredientes.objects.get(ingrediente="Arroz", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes2, quantity=50, medida=medida_grama, restaurante=get_restaurante)
    ingrediente_2 = IngredientesItem.objects.get(ingrediente=ingredientes2, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Filet Trinchado", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_2.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Batata Frita", price=0.01)    
    ingredientes3 = Ingredientes.objects.get(ingrediente="Batata Frita", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes3, quantity=100, medida=medida_grama, restaurante=get_restaurante)
    ingrediente_3 = IngredientesItem.objects.get(ingrediente=ingredientes3, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Filet Trinchado", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_3.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Tequila", price=0.12)    
    ingredientes4 = Ingredientes.objects.get(ingrediente="Tequila", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes4, quantity=30, medida=medida_ml, restaurante=get_restaurante)
    ingrediente_4 = IngredientesItem.objects.get(ingrediente=ingredientes4, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Marguerita", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_4.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Licor de Laranja", price=0.08)    
    ingredientes5 = Ingredientes.objects.get(ingrediente="Licor de Laranja", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes5, quantity=40, medida=medida_ml, restaurante=get_restaurante)
    ingrediente_5 = IngredientesItem.objects.get(ingrediente=ingredientes5, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Marguerita", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_5.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Suco de Limão", price=0.001)    
    ingredientes6 = Ingredientes.objects.get(ingrediente="Suco de Limão", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes6, quantity=50, medida=medida_ml, restaurante=get_restaurante)
    ingrediente_6 = IngredientesItem.objects.get(ingrediente=ingredientes6, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Marguerita", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_6.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Heineken 600ml", price=6.00)    
    ingredientes7 = Ingredientes.objects.get(ingrediente="Heineken 600ml", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes7, quantity=1, medida=medida_un, restaurante=get_restaurante)
    ingrediente_7 = IngredientesItem.objects.get(ingrediente=ingredientes7, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Cerveja Heineken 600ml", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_7.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Bolo de Chocolate", price=0.01)    
    ingredientes8 = Ingredientes.objects.get(ingrediente="Bolo de Chocolate", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes8, quantity=150, medida=medida_grama, restaurante=get_restaurante)
    ingrediente_8 = IngredientesItem.objects.get(ingrediente=ingredientes8, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Petit Gateau", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_8.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Sorvete Creme", price=0.02)    
    ingredientes9 = Ingredientes.objects.get(ingrediente="Sorvete Creme", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes9, quantity=100, medida=medida_grama, restaurante=get_restaurante)
    ingrediente_9 = IngredientesItem.objects.get(ingrediente=ingredientes9, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Petit Gateau", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_9.id)

    Ingredientes.objects.get_or_create(restaurante=get_restaurante, ingrediente="Calda Chocolate Kopenhag", price=0.1)    
    ingredientes10 = Ingredientes.objects.get(ingrediente="Calda Chocolate Kopenhag", restaurante=get_restaurante)
    IngredientesItem.objects.get_or_create(ingrediente=ingredientes10, quantity=10, medida=medida_ml, restaurante=get_restaurante)
    ingrediente_10 = IngredientesItem.objects.get(ingrediente=ingredientes10, restaurante=get_restaurante)    
 
    for i in ItensMenu.objects.filter(item="Petit Gateau", restaurante=get_restaurante):
        i.ingredientes.add(ingrediente_10.id)


    for i in ItensMenu.objects.filter(item="Filet Trinchado", restaurante=get_restaurante):
        i.categoria.add(categorias1.id)

    for i in ItensMenu.objects.filter(item="Cerveja Heineken 600ml", restaurante=get_restaurante):
        i.categoria.add(categorias2.id)

    for i in ItensMenu.objects.filter(item="Marguerita", restaurante=get_restaurante):
        i.categoria.add(categorias2.id)

    for i in ItensMenu.objects.filter(item="Petit Gateau", restaurante=get_restaurante):
        i.categoria.add(categorias3.id)

    for i in ItensMenu.objects.filter(item="Filet Trinchado", restaurante=get_restaurante):
        i.menus.add(menu.id)
    
    for i in ItensMenu.objects.filter(item="Cerveja Heineken 600ml", restaurante=get_restaurante):
        i.menus.add(menu.id)

    for i in ItensMenu.objects.filter(item="Marguerita", restaurante=get_restaurante):
        i.menus.add(menu.id)

    for i in ItensMenu.objects.filter(item="Petit Gateau", restaurante=get_restaurante):
        i.menus.add(menu.id)

    if get_restaurante.cardapio_gerado == True:
        get_cardapio = get_object_or_404(Cardapio, restaurante__restaurante_ref_ao_redor=rest)
        return redirect('view-cardapio-fybasic', rest=rest)

    else:   
        initial = "https://findfy.herokuapp.com/local/"
        restaurante = str(rest)
        cardapio_coder = str(uuid.uuid4())
        myTuple = (initial, restaurante, '/', cardapio_coder)
        x = "".join(myTuple)

        cardapio_check = Cardapio.objects.filter(restaurante=get_restaurante)
        if cardapio_check:
            if(get_restaurante.cardapio_gerado == False):
                get_restaurante.cardapio_gerado = True
                get_restaurante.save()
        else: 
            Cardapio.objects.create(restaurante=get_restaurante, cardapio_code = cardapio_coder, cardapio_oficial_code=x, user=request.user)
            if(get_restaurante.cardapio_gerado == False):
                get_restaurante.cardapio_gerado = True
                get_restaurante.save()
            
        return redirect('view-cardapio-fybasic', rest=rest)



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
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref_ao_redor=rest)
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
    
    return render(request, 'tables/cardapio-oficial.html', {'itensmenu': itensmenu, 'tableuser': tableuser, 'obj': obj, 'code': code,
        'itenscat1': itenscat1, 'itenscat2': itenscat2, 'itenscat3': itenscat3, 
        'itenscat4': itenscat4, 'itenscat5': itenscat5, 'itenscat6': itenscat6,
        'itenscat7': itenscat7, 'itenscat8': itenscat8, 'itenscat9': itenscat9,
        'itenscat10': itenscat10, 'itenscat11': itenscat11, 'itenscat12': itenscat12,
        'itenscat13': itenscat13, 'itenscat14': itenscat14, 'itenscat15': itenscat15,
        'categ1': categ1, 'categ2': categ2, 'categ3': categ3, 
        'categ4': categ4, 'categ5': categ5, 'categ6': categ6, 
        'categ7': categ7, 'categ8': categ8, 'categ9': categ9, 
        'categ10': categ10 })


@login_required
def cardapioFyBasicView(request, rest):
   
    obj = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest, user=request.user, deactivate=False)
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
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref_ao_redor=rest)
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
    newlogo = NewLogoForm()
    newaddress = NewAddressForm(instance=obj)
    newphotoback = NewPhotoBackForm()

    return render(request, 'tables/cardapio-fybasic.html', {'itensmenu': itensmenu, 'tableuser': tableuser, 'obj': obj, 'code': code,
        'itenscat1': itenscat1, 'itenscat2': itenscat2, 'itenscat3': itenscat3, 
        'itenscat4': itenscat4, 'itenscat5': itenscat5, 'itenscat6': itenscat6,
        'itenscat7': itenscat7, 'itenscat8': itenscat8, 'itenscat9': itenscat9,
        'itenscat10': itenscat10, 'itenscat11': itenscat11, 'itenscat12': itenscat12,
        'itenscat13': itenscat13, 'itenscat14': itenscat14, 'itenscat15': itenscat15,
        'categ1': categ1, 'categ2': categ2, 'categ3': categ3, 
        'categ4': categ4, 'categ5': categ5, 'categ6': categ6, 
        'categ7': categ7, 'categ8': categ8, 'categ9': categ9, 
        'categ10': categ10, 'newlogo': newlogo, 'newaddress': newaddress, 'newphotoback': newphotoback })



@login_required
def cardapioFyPlusView(request, rest):
    obj = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest, user=request.user, deactivate=False)
    code = get_object_or_404(Cardapio, restaurante__restaurante_ref_ao_redor=rest)
    get_atendente = get_object_or_404(AtendentesRestaurante, restaurante__restaurante_ref_ao_redor=rest, atendente=request.user)
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
    categ = CategoriasMenu.objects.filter(restaurante__restaurante_ref_ao_redor=rest)
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
    
    return render(request, 'tables/cardapio-fyplus.html', {'itensmenu': itensmenu, 'tableuser': tableuser, 'obj': obj, 'code': code, 'get_atendente': get_atendente,
        'itenscat1': itenscat1, 'itenscat2': itenscat2, 'itenscat3': itenscat3, 
        'itenscat4': itenscat4, 'itenscat5': itenscat5, 'itenscat6': itenscat6,
        'itenscat7': itenscat7, 'itenscat8': itenscat8, 'itenscat9': itenscat9,
        'itenscat10': itenscat10, 'itenscat11': itenscat11, 'itenscat12': itenscat12,
        'itenscat13': itenscat13, 'itenscat14': itenscat14, 'itenscat15': itenscat15,
        'categ1': categ1, 'categ2': categ2, 'categ3': categ3, 
        'categ4': categ4, 'categ5': categ5, 'categ6': categ6, 
        'categ7': categ7, 'categ8': categ8, 'categ9': categ9, 
        'categ10': categ10 })



@login_required
def blockInstrucao_1(request, rest):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_restaurante.instrucoes_1 = True
    get_restaurante.save()

    return redirect('local', rest=rest)
    
   
@login_required
def blockInstrucao_2(request, rest):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_restaurante.instrucoes_2 = True
    get_restaurante.save()

    return redirect('local', rest=rest)


@login_required
def blockInstrucao_3(request, rest):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente = get_object_or_404(AtendentesRestaurante, atendente=request.user, restaurante=get_restaurante)
    get_restaurante.instrucoes_3 = True
    get_restaurante.save()
    
    return redirect('solicitacoes-atendente-instrucoes-view', rest=rest, atendente=get_atendente.code)


@login_required
def blockInstrucao_4(request, rest, mesa):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_restaurante.instrucoes_4 = True
    get_restaurante.save()

    return redirect('confirmed-new-table', rest=rest, mesa=mesa)


@login_required
def blockInstrucao_5(request, rest):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_atendente = get_object_or_404(AtendentesRestaurante, atendente=request.user, restaurante=get_restaurante)
    get_restaurante.instrucoes_5 = True
    get_restaurante.save()
    
    return redirect('solicitacoes-atendente-view', rest=rest, atendente=get_atendente.code)


@login_required
def deactivateLocal(request, rest):
    get_restaurante = get_object_or_404(Restaurante, restaurante_ref=rest, user=request.user)
    get_restaurante.deactivate = True
    get_restaurante.save()
    
    return redirect('/local')



# TO BE REVIEWED
def indexLocais(request):
    google_places = GoogleImport.objects.all()
    list10 = google_places[0:10]
    search = request.GET.get('search')
    locais = Restaurante.objects.filter()
    
    if search:
        google_filter = GoogleImport.objects.filter(name__icontains=search)
    else:
        google_filter = GoogleImport.objects.all()
        list10 = google_filter[0:10]
    
    return render(request, 'restaurantes/ao_redor.html', {'locais': locais, 'list10': list10, 'google_filter': google_filter, 'search': search})


def SiteLocal(request, rest):
    local = get_object_or_404(Restaurante, restaurante_ref_ao_redor=rest)
    local_users = TableUser.objects.filter(table__paid=False, table__restaurante__restaurante_ref_ao_redor=rest)
    site = Site.objects.filter(restaurante__restaurante_ref_ao_redor=rest)    
    return render(request, 'restaurantes/indexlocal.html', {'local': local, 'local_users': local_users})
