from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Case, When, Count

from restaurantes.models import Restaurante, AtendentesRestaurante
from menus.models import ItensMenu, CategoriasMenu
from accounts.models import CustomUser
from mensagens.models import EnviarMensagem
from profiles.models import UserProfile, Liker

from profiles.forms import UserProfileForm, NewPhotoForm
from django.http import JsonResponse

# from atendentes.models import Atendente
# import random
# import string


@login_required
def myProfileView(request):
    UserProfile.objects.get_or_create(user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = NewPhotoForm(request.POST or None, request.FILES or None, instance=profile)
    
        if form.is_valid():
            form.save()

            return redirect('my-profile-view')
        
    else:
        profile = get_object_or_404(UserProfile, user=request.user)
        form = NewPhotoForm()
        messages = EnviarMensagem.objects.filter(message_to=request.user)
        likers = Liker.objects.filter(like_to=request.user, curtida=True)    
        like_check = Liker.objects.filter(like_to=request.user).values('curtida')
        like_anon_check = Liker.objects.filter(like_to=request.user).values('like_anonimo')
        like_counter = 0
        like_anon_counter = 0
        
        if like_check.exists():
            like = like_check.filter(curtida=True)
            if like.exists():
                like_counter = like.aggregate(count=Count('curtida'))
                
        if like_anon_check.exists():
            like_a = like_anon_check.filter(like_anonimo=True)
            if like_a.exists():
                like_anon_counter = like_a.aggregate(count=Count('like_anonimo'))
       
    return render(request, 'profiles/my-profile.html', {'profile': profile, 'form': form, 'messages': messages, 'like_counter': like_counter, 'like_anon_counter': like_anon_counter, 'likers': likers, 'form': form })


@login_required
def editProfileView(request):
    try:
        user = get_object_or_404(UserProfile, user=request.user)
    except:
        UserProfile.objects.create(user=request.user)
    
    user = get_object_or_404(UserProfile, user=request.user)
    mensagens = EnviarMensagem.objects.filter(message_to=request.user.id)
           

@login_required
def editVisible(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user.visible == True:
        user.visible = False
    else:
        user.visible = True
    user.save()

    return redirect('/profile')


# resolve this
@login_required
def editVisibleLocalPage(request, rest):
    user = get_object_or_404(UserProfile, user=request.user)
    if user.visible == True:
        user.visible = False
    else:
        user.visible = True
    user.save()

    return redirect('local-page-view', rest=rest)


@login_required
def editPhoto(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    form = NewPhotoForm(instance=userprofile)

    if request.method == 'POST':
        form = NewPhotoForm(request.POST, request.FILES, instance=userprofile)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('/profile')


@login_required
def profileView(request, mesa, id):
    try:
        profile = get_object_or_404(UserProfile, code=id, user=request.user)
        like_check = Liker.objects.filter(like_to=request.user)
        # like = like_check.filter(curtida=True)
        # likeanonimo = like_check.filter(like_anonimo=True)
        # blocker = like_check.filter(block=True)
        return redirect('my-profile-view')
    except:
        profiler = get_object_or_404(UserProfile, code=id)
        like_check = Liker.objects.filter(like_from=request.user, like_to=profiler.user.id)
        like = like_check.filter(curtida=True)
        likeanonimo = like_check.filter(like_anonimo=True)
        blocker = like_check.filter(block=True)
            
        return render(request, 'profiles/profile.html', {'profile': profiler, 'like': like, 'likeanonimo': likeanonimo, 'blocker': blocker, 'mesa': mesa})
        

@login_required
def profileViewFromLocalPage(request, rest, mesa, id):
    try:
        profile = get_object_or_404(UserProfile, code=id, user=request.user)
        like_check = Liker.objects.filter(like_to=request.user)
        # like = like_check.filter(curtida=True)
        # likeanonimo = like_check.filter(like_anonimo=True)
        # blocker = like_check.filter(block=True)
        return redirect('my-profile-view')
    except:
        profiler = get_object_or_404(UserProfile, code=id)
        like_check = Liker.objects.filter(like_from=request.user, like_to=profiler.user.id)
        like = like_check.filter(curtida=True)
        likeanonimo = like_check.filter(like_anonimo=True)
        blocker = like_check.filter(block=True)
            
        return render(request, 'profiles/profile-from-local-page.html', {'profile': profiler, 'like': like, 'likeanonimo': likeanonimo, 'blocker': blocker, 'mesa': mesa, 'rest': rest})
        

@login_required
def curtida(request, id):
    get_to = get_object_or_404(UserProfile, code=id)
    Liker.objects.get_or_create(like_from=request.user, like_to=get_to.user)
    check = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user)
    check.curtida = True
    check.save()      
    return redirect('profile-view', id=get_to.code)


@login_required
def curtidaDirect(request, rest, mesa, id):
    get_to = get_object_or_404(UserProfile, code=id)
    Liker.objects.get_or_create(like_from=request.user, like_to=get_to.user)
    check = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user)
    check.curtida = True
    check.save()      
    return redirect('profile-view-from-local-page', rest=rest, mesa=mesa, id=id)


@login_required
def descurtida(request, id):
    get_to = get_object_or_404(UserProfile, code=id)
    checks = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user.id)
    checks.curtida = False
    checks.save()
    return redirect('profile-view', id=get_to.code)


@login_required
def descurtidaDirect(request, rest, mesa, id):
    get_to = get_object_or_404(UserProfile, code=id)
    checks = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user.id)
    checks.curtida = False
    checks.save()
    return redirect('profile-view-from-local-page', rest=rest, mesa=mesa, id=id)


@login_required
def likeAnonimo(request, id):
    get_to = get_object_or_404(UserProfile, code=id)
    Liker.objects.get_or_create(like_from=request.user, like_to=get_to.user)
    check = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user)
    check.like_anonimo = True
    check.save()      
    return redirect('profile-view', id=get_to.code)


@login_required
def likeAnonimoDirect(request, rest, mesa, id):
    get_to = get_object_or_404(UserProfile, code=id)
    Liker.objects.get_or_create(like_from=request.user, like_to=get_to.user)
    check = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user)
    check.like_anonimo = True
    check.save()      
    return redirect('profile-view-from-local-page', rest=rest, mesa=mesa, id=id)


@login_required
def deslikeAnonimo(request, id):
    get_to = get_object_or_404(UserProfile, code=id)
    checks = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user.id)
    checks.like_anonimo = False
    checks.save()
    return redirect('profile-view', id=get_to.code)


@login_required
def deslikeAnonimoDirect(request, rest, mesa, id):
    get_to = get_object_or_404(UserProfile, code=id)
    checks = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user.id)
    checks.like_anonimo = False
    checks.save()
    return redirect('profile-view-from-local-page', rest=rest, mesa=mesa, id=id)


@login_required
def bloquear(request, id):
    get_to = get_object_or_404(UserProfile, code=id)
    Liker.objects.get_or_create(like_from=request.user, like_to=get_to.user.id)
    check = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user.id)
    check.block = True
    check.save()      
    return redirect('profile-view', id=get_to.code)


@login_required
def desbloquear(request, id):
    get_to = get_object_or_404(UserProfile, code=id)
    check = get_object_or_404(Liker, like_from=request.user, like_to=get_to.user.id)
    check.block = False
    check.save()
    return redirect('profile-view', id=get_to.code)


@login_required
def blockInstrucaoEstabelecimento(request):
    get_userprofile = get_object_or_404(UserProfile, user=request.user)
    get_userprofile.instrucao_estabelecimento = True
    get_userprofile.save()

    return redirect('index-local')


# saved for furture use
@login_required
def editCommunicate(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user.communicate == True:
        user.communicate = False
    else:
        user.communicate = True
    user.save()

    return redirect('/profile')


@login_required
def editCommunicateLocalPage(request, rest):
    user = get_object_or_404(UserProfile, user=request.user)
    if user.communicate == True:
        user.communicate = False
    else:
        user.communicate = True
    user.save()

    return redirect('local-page-view', rest=rest)