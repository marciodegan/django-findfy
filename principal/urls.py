from django.urls import path
from principal.views import index_view, index_user, indexApp


urlpatterns = [
	path('', index_view, name='index'),
	path('<int:user>', index_user, name='index-user'),
	path('findfy', indexApp, name='index-app'),
]
