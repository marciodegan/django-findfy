from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.indexLocal, name="index-local"),
    path('locais', views.indexLocal, name="index-locais"),
    path('<uuid:rest>', views.local, name="local"),
    path('<uuid:rest>/<uuid:mesa>/local-page', views.localPageView, name="local-page-view"),
    path('createlocal', views.createLocal, name="create-local"),
    path('create-local-post', views.createLocalPost, name="create-local-post"),
    path('<uuid:rest>/edit-local', views.editLocal, name="edit-local"),
    path('<uuid:rest>/edit-photo', views.editPhoto, name="edit-photo"),
    path('<uuid:rest>/edit-photo-back', views.editPhotoBack, name="edit-photo-back"),
    path('<uuid:rest>/edit-address', views.editAddress, name="edit-address"),
    path('<uuid:rest>/<int:id>/fechar-local', views.fecharLocal, name="fechar-local"),
    path('<uuid:rest>/data-operacional', views.createDate, name="data-operacional"),

    # DESATIVAR LOCAL
    path('<uuid:rest>/deactivate-local', views.deactivateLocal, name="deactivate-local"),

    # CARDÁPIOS
    path('<uuid:rest>/create-cardapio', views.gerarCardapio, name="create-cardapio"),
    path('<uuid:rest>/<uuid:cardapio>', views.cardapioView, name="view-cardapio-oficial"),
    path('<uuid:rest>/fybasic', views.cardapioFyBasicView, name="view-cardapio-fybasic"),
    path('<uuid:rest>/fyplus', views.cardapioFyPlusView, name="view-cardapio-fyplus"),
    
    # MESA
    path('<uuid:rest>/createmesa', views.createTable, name="create-mesa"),
    path('<uuid:rest>/<int:id>/deletemesa', views.deleteMesa, name="delete-mesa"),
    
    # CATEGORIA
    path('<uuid:rest>/createcategoria', views.createCategoria, name="create-categoria"),
    path('<uuid:rest>/<int:id>/deletecategoria', views.deleteCategoria, name="delete-categoria"),

    # MENU
    path('<uuid:rest>/createmenu', views.createMenu, name="create-menu"),
    path('<uuid:rest>/<int:id>/deletemenu', views.deleteMenu, name="delete-menu"),
    
    # PRODUTO
    path('<uuid:rest>/createproduto', views.createProduto, name="create-produto"),
    path('<uuid:rest>/<uuid:id>/editproduto', views.editProduto, name="edit-produto"),
    path('<uuid:rest>/<uuid:id>/deleteproduto', views.deleteProduto, name="delete-produto"),
    # path('<uuid:rest>/<int:id>', views.editProduto, name="edit-produto"),
    
    # ATENDENTE
    path('<uuid:rest>/create-atendente', views.createAtendente, name="create-atendente"),
    path('<uuid:rest>/<str:atendente>/add-atendente', views.addAtendente, name="add-atendente"),
    path('<uuid:rest>/<int:id>/ativar-atendente', views.ativarAtendente, name="ativar-atendente"),
    path('<uuid:rest>/<int:id>/delete-atendente', views.deleteAtendente, name="delete-atendente"),

    # ATENDENTE MASTER
    path('<uuid:rest>/create-atendente-master', views.createAtendenteMaster, name="create-atendente-master"),
    path('<uuid:rest>/<str:atendente>/add-atendente-master', views.addAtendenteMaster, name="add-atendente-master"),
    path('<uuid:rest>/<int:id>/ativar-atendente-master', views.ativarAtendenteMaster, name="ativar-atendente-master"),
    path('<uuid:rest>/<int:id>/delete-atendente-master', views.deleteAtendenteMaster, name="delete-atendente-master"),

    # COZINHA URLs
    path('<uuid:rest>/create-cozinha', views.createCozinha, name="create-cozinha"),
    path('<uuid:rest>/<str:atendente>/add-cozinha', views.addCozinha, name="add-cozinha"),
    path('<uuid:rest>/<int:id>/ativar-cozinha', views.ativarCozinha, name="ativar-cozinha"),
    path('<uuid:rest>/<int:id>/delete-cozinha', views.deleteCozinha, name="delete-cozinha"),
    
    # BAR URLs
    path('<uuid:rest>/create-bar', views.createBar, name="create-bar"),
    path('<uuid:rest>/<str:atendente>/add-bar', views.addBar, name="add-bar"),
    path('<uuid:rest>/<int:id>/ativar-bar', views.ativarBar, name="ativar-bar"),
    path('<uuid:rest>/<int:id>/delete-bar', views.deleteBar, name="delete-bar"),
    
    # CAIXA URLs
    path('<uuid:rest>/create-caixa', views.createCaixa, name="create-caixa"),
    path('<uuid:rest>/<str:atendente>/add-caixa', views.addCaixa, name="add-caixa"),
    path('<uuid:rest>/<int:id>/ativar-caixa', views.ativarCaixa, name="ativar-caixa"),
    path('<uuid:rest>/<int:id>/delete-caixa', views.deleteCaixa, name="delete-caixa"),
    
    # INSTRUÇÕES
    path('<uuid:rest>/block-instrucao-1', views.blockInstrucao_1, name="block-instrucao1"),
    path('<uuid:rest>/block-instrucao-2', views.blockInstrucao_2, name="block-instrucao2"),
    path('<uuid:rest>/block-instrucao-3', views.blockInstrucao_3, name="block-instrucao3"),
    path('<uuid:rest>/<uuid:mesa>/block-instrucao-4', views.blockInstrucao_4, name="block-instrucao4"),
    path('<uuid:rest>/block-instrucao-5', views.blockInstrucao_5, name="block-instrucao5"),
    
    # TO BE REVIEWED
    path('insta', TemplateView.as_view(template_name='restaurantes/insta.html', extra_context={"instagram_profile_name": "elevado_bar"}))

]



