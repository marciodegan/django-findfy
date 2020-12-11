from django.contrib.messages.views import SuccessMessageMixin
from accounts.forms import CustomUserCreateForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from accounts.models import CustomUser
from tables.models import TableUser
from django.contrib.auth.views import (
	PasswordChangeView,
	PasswordResetView,
	PasswordResetConfirmView,
	PasswordResetCompleteView,
	)


class UserCreate(SuccessMessageMixin, CreateView):
	model = CustomUser
	form_class = CustomUserCreateForm
	template_name = 'accounts/user-new.html'
	success_url = '/accounts/login'
	success_message = 'Bem-Vindo! Faça o login para começar!'


class UserChange(SuccessMessageMixin, UpdateView):
	model = CustomUser
	form_class = CustomUserChangeForm
	template_name = 'accounts/user-change.html'
	success_url = '/'
	success_message = 'O seu perfil foi alterado'

	def get_queryset(self):

		if self.request.user.is_authenticated:
			return self.model.objects.filter(username=self.request.user)

		else:
			return super().get_queryset().filter(username=None)

class UserDelete(SuccessMessageMixin, DeleteView):
	model = CustomUser
	success_url = '/'
	template_name = 'accounts/user-delete.html'

	def get_queryset(self):

		if self.request.user.is_authenticated:
			return self.model.objects.filter(username=self.request.user)

		else:
			return super().get_queryset().filter(username=None)


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
	template_name = 'accounts/password-change.html'
	success_url = '/'
	success_message = 'A sua senha foi modificada com sucesso.'


class PasswordReset(SuccessMessageMixin, PasswordResetView):
	template_name = 'accounts/password-reset.html'


class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
	success_message = 'A sua senha foi redefinida corretamente. Faça novo login!'
	# success_url = '/accounts/login'


class PasswordResetComplete(SuccessMessageMixin, PasswordResetCompleteView):
	template_name = 'registration/login.html'
	success_message = 'A sua senha foi redefinida corretamente. Faça novo login!'
