from django.urls import path, re_path

from . import views

urlpatterns = [
    path('<id>', views.EnviarMensagemView, name="enviar-mensagem"),

]