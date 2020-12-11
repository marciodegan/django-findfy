from django import forms

from .models import Table, ValoresCaixa, TableItens, FormaDePagamento

class TableForm(forms.ModelForm):

    class Meta:
        model = Table
        fields = ('restaurante',)


class LancamentoForm(forms.ModelForm):

    class Meta:
        model = ValoresCaixa
        fields = ('valor', 'forma_pagamento')
    
    def __init__(self, local, *args, **kwargs):
        super(LancamentoForm, self).__init__(*args, **kwargs)
        self.fields['forma_pagamento'].queryset = FormaDePagamento.objects.filter(restaurante=local)


class DateForm(forms.ModelForm):

    class Meta:
        model = TableItens
        fields = ('date',)
    
