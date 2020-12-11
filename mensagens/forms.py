from django import forms

from .models import EnviarMensagem

class MessageForm(forms.ModelForm):

    class Meta:
        model = EnviarMensagem
        fields = ('mensagem',)
        