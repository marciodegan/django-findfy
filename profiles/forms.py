from django import forms

from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar', 'is_atendente','user')


class NewPhotoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar',)
        labels = {
            'avatar': 'Adicione uma foto',
                     
        }