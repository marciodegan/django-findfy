# NOT IN USE AT THE MOMENT
from accounts.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import random
import string
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

# from atendentes.models import Atendente
from restaurantes.models import Restaurante, AtendentesRestaurante
from menus.models import ItensMenu, CategoriasMenu
from accounts.models import CustomUser
from . models import EnviarMensagem
from . forms import MessageForm


@login_required
def EnviarMensagemView(request, id):
    profile = get_object_or_404(CustomUser, pk=id)
    if request.method == 'POST':
        form = MessageForm()
        if form.is_valid():
            message = form.save(commit=False)
            message_from = request.user
            
        EnviarMensagem.objects.create(message_from=request.user, message_to=profile, mensagem=mensagem)
    mensagens_to = EnviarMensagem.objects.filter(message_from=request.user, message_to=profile)
    mensagens_from = EnviarMensagem.objects.filter(message_from=profile, message_to=request.user) 
    mensagens = EnviarMensagem.objects.filter(message_to=request.user.id)
    
    return render(request, 'profiles/profile.html', {'profile': profile, 'mensagens_to': mensagens_to, 'mensagens_from': mensagens_from, 'mensagens': mensagens})


