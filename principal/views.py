from django.shortcuts import render, get_object_or_404
from restaurantes.models import Restaurante, AtendentesRestaurante, AtendentesMaster, CozinhaRestaurante, BarmanRestaurante, CaixasRestaurante
from tables.models import TableUser
from profiles.forms import NewPhotoForm
from profiles.models import UserProfile


def index_view(request):
	if request.user.is_anonymous:
		return render(request, 'principal/index.html') 
	else:
		local = Restaurante.objects.filter(user=request.user)
		atendente = AtendentesRestaurante.objects.filter(atendente=request.user)
		atendentemaster = AtendentesMaster.objects.filter(atendentemaster=request.user)
		cozinha = CozinhaRestaurante.objects.filter(cozinha=request.user)
		bar = BarmanRestaurante.objects.filter(barman=request.user)
		caixa = CaixasRestaurante.objects.filter(caixa=request.user)
		form = NewPhotoForm(instance=request.user)
		profile = UserProfile.objects.filter(user=request.user)
		check_table = TableUser.objects.filter(table_user=request.user, table__paid=True)

		return render(request, 'principal/index.html', 
			{'local': local, 'atendente': atendente, 'atendentemaster': atendentemaster,
			'cozinha': cozinha, 'bar': bar, 'caixa': caixa, 'form': form, 'profile': profile, 'check_table': check_table })


def index_user(request):
	local = Restaurante.objects.filter(user=request.user)
	atendente = AtendentesRestaurante.objects.filter(atendente=request.user)
	atendentemaster = AtendentesMaster.objects.filter(atendentemaster=request.user)
	cozinha = CozinhaRestaurante.objects.filter(cozinha=request.user)
	bar = BarmanRestaurante.objects.filter(barman=request.user)
	caixa = CaixasRestaurante.objects.filter(caixa=request.user)
	form = NewPhotoForm(instance=request.user)
	profile = UserProfile.objects.filter(user=request.user)

	return render(request, 'principal/index.html',
		{'local': local, 'atendente': atendente, 'atendentemaster': atendentemaster,
		'cozinha': cozinha, 'bar': bar, 'caixa': caixa, 'form': form, 'profile': profile})


def indexApp(request):
	return render(request, 'principal/index-app.html', {})