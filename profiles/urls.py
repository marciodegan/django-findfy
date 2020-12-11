from django.urls import path, re_path

from . import views

urlpatterns = [
    # path('', views.editProfileView, name='edit-profile'),
    path('', views.myProfileView, name='my-profile-view'),
    path('<uuid:id>', views.profileView, name='profile-view'),
    path('<uuid:rest>/<uuid:mesa>/<uuid:id>', views.profileViewFromLocalPage, name='profile-view-from-local-page'),
    path('editvisible', views.editVisible, name='edit-visible'),
    path('editvisible/<uuid:rest>', views.editVisibleLocalPage, name='edit-visible-local-page'),
    path('edit-photo', views.editPhoto, name='edit-profile-photo'),
    path('editcommunicate', views.editCommunicate, name='edit-communicate'),
    path('editcommunicate/<uuid:rest>', views.editCommunicateLocalPage, name='edit-communicate-local-page'),
    path('<uuid:id>/curtida', views.curtida, name='curtida'),
    path('<uuid:rest>/<uuid:mesa>/<uuid:id>/curtida', views.curtidaDirect, name='curtida-direct'),
    path('<uuid:id>/descurtida', views.descurtida, name='descurtida'),
    path('<uuid:rest>/<uuid:mesa>/<uuid:id>/descurtida', views.descurtidaDirect, name='descurtida-direct'),
    path('<uuid:id>/likeanonimo', views.likeAnonimo, name='like-anonimo'),
    path('<uuid:rest>/<uuid:mesa>/<uuid:id>/likeanonimo', views.likeAnonimoDirect, name='like-anonimo-direct'),
    path('<uuid:id>/deslikeanonimo', views.deslikeAnonimo, name='deslike-anonimo'),
    path('<uuid:rest>/<uuid:mesa>/<uuid:id>/deslikeanonimo', views.deslikeAnonimoDirect, name='deslike-anonimo-direct'),
    path('<uuid:id>/bloquear', views.bloquear, name='bloquear'),
    path('<uuid:id>/desbloquear', views.desbloquear, name='desbloquear'),
    path('bloquear-instrucao-estabelecimento', views.blockInstrucaoEstabelecimento, name='bloquear-instrucao-estabelecimento'),



    # path('enviarmensagem', views.EnviarMensagemView, name="enviar-mensagem"),

]