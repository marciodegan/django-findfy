from django.urls import path, re_path
from django.urls import path


from . import views

urlpatterns = [
    path('', views.indexTables, name="index-tables"),
    path('<uuid:rest>/tables', views.viewTables, name="view-tables"),
    path('<uuid:rest>/tables/<uuid:atendentemaster>', views.viewTablesAll, name="view-tables-all"),
    
#atendente
    path('atendente', views.viewRestaurantesAtendente, name="index-tables-atendente"),    
    path('<uuid:rest>/acgesate/<uuid:atendente>', views.solicitacoesAtendenteView, name="solicitacoes-atendente-view"),
    path('<uuid:rest>/acgesate/<uuid:atendente>/instrucoes', views.solicitacoesAtendenteInstrucoesView, name="solicitacoes-atendente-instrucoes-view"),
    path('<uuid:rest>/acgesate/<uuid:atendente>/instrucoes2', views.solicitacoesAtendenteInstrucoes2View, name="solicitacoes-atendente-instrucoes2-view"),
    path('<uuid:rest>/<uuid:id>/<int:item>/to-cozinha', views.viewTablesAtendenteEnviarCozinha, name="view-tables-atendente-enviar-cozinha"),    
    path('<uuid:rest>/<uuid:id>/<int:item>/to-bar', views.viewTablesAtendenteEnviarBar, name="view-tables-atendente-enviar-bar"),    
    path('<uuid:rest>/<uuid:id>/<int:item>/cancel', views.viewTablesAtendenteCancel, name="solicitacoes-atendente-cancelar"),    

    path('<uuid:rest>/<uuid:atend>/preopen/<uuid:mesa>/', views.PreNewTable, name='pre-new-table-add'),
    path('<uuid:rest>/<uuid:atend>/preopen/<uuid:mesa>/master', views.PreNewTableMasterView, name='pre-new-table-add-master'),
    path('<uuid:rest>/<uuid:mesa>/table-opened/', views.newTable, name='table-add'),
    path('<uuid:rest>/<int:atend>/preopen/<uuid:mesa>/table_add_master/', views.newTableMaster, name='new-table-add-master'),
    path('<uuid:rest>/<uuid:mesa>/confirmed/', views.ConfirmedNewTable, name='confirmed-new-table'),
    # path('tablecode/<int:id>', views.TableView, name='qrcode-view'),
    path('<uuid:rest>/<uuid:id>/<uuid:atend>/garcom', views.EntrarMesaGarcon, name="entrar-mesa-garcom"),
    path('<int:rest>/<int:id>/<int:atend>/garcom-alternativo', views.EntrarMesaGarcomAlternativo, name="entrar-mesa-garcom-alternativo"),

#atendentemaster
    path('atendentemaster', views.AtendenteMasterIndexView, name="index-atendente-master"),
    path('<uuid:rest>/tables/<uuid:atendente>/atendenteall', views.SolicitacoesAtendenteMasterView, name="solicitacoes-atendente-master-view"),
    path('<uuid:rest>/<uuid:id>/<int:item>/to-cozinha/master', views.viewTablesAtendenteEnviarCozinhaMaster, name="view-tables-atendente-enviar-cozinha-master"),    
    path('<int:rest>/<int:mesa>/<int:pk>/cozdmas/<int:atendente>', views.viewTablesAtendenteMasterEnviarCozinha, name="view-tables-atendente-master-enviar-cozinha"),   
    path('<int:rest>/<int:mesa>/<int:pk>/fdsko3f/<int:atendente>', views.viewTablesAtendenteMasterEnviarBar, name="view-tables-atendente-master-enviar-bar"),   
    
#bar
    path('bar', views.BarView, name="index-bar"),
    path('<uuid:rest>/tables/bar', views.viewTablesBar, name="view-tables-bar"),
    path('<uuid:rest>/<uuid:id>/<int:item>/barenviargarcon', views.viewTablesBarEnviarGarcon, name="view-tables-bar-enviar-garcon"),    

#cozinha
    path('cozinha', views.CozinhaView, name="index-cozinha"),
    path('<uuid:rest>/tables/cozinha', views.viewTablesCozinha, name="view-tables-cozinha"),
    path('<uuid:rest>/<uuid:id>/<int:item>/cozinhaenviargarcon', views.viewTablesCozinhaEnviarGarcon, name="view-tables-cozinha-enviar-garcon"),    
    
#cliente
    path('<uuid:rest>/<uuid:id>', views.EntrarMesaCliente, name="entrar-mesa"),
    path('<int:rest>/<int:id>/pagamento_solicitado', views.SolicitacaoDePagamento, name="pagamento-solicitado"),

    # path('<int:rest>/<int:id>/<int:cliente>/cliente', views.EntrarMesaCliente, name="entrar-mesa-cliente"),
    # path('<uuid:rest>/<uuid:id>/<int:item>', views.PreNewTableItem, name="pre-adicionar-item-mesa"),
    # path('<int:rest>/<int:id>/<int:item>/confirmado', views.PreNewTableItemClienteConfirmed, name="pre-adicionar-item-mesa-confirmado"),
    path('confirmado', views.PreNewTableItemClienteConfirmedNew, name="pre-adicionar-item-mesa-confirmado"),
    path('atendenteconfirmado', views.PreNewTableItemAtendente, name="pre-adicionar-item-mesa-confirmado-atendente"),
    path('<uuid:rest>/<uuid:mesa>/<int:pk>', views.NewTableItemAtendente, name="adicionar-item-mesa-garcom"),
    path('<uuid:rest>/<uuid:mesa>/<int:pk>/fdtfda/<uuid:atendente>', views.NewTableItemGarcomMaster, name="new-table-garcom-add-master"),
    path('<int:rest>/<int:id>/solicitacaopagamento', views.SolicitacaoDePagamento, name="solicitacao-de-pagamento"),
    path('<int:rest>/<int:id>/solicitacaopagamentocontafinal', views.SolicitacaoDePagamentoContaFinal, name="solicitacao-de-pagamento-conta-final"),
    path('<int:rest>/<int:id>/clienteaguardaconta', views.ClienteAguardandoConta, name="cliente-aguardando-conta"),
    path('<int:rest>/<int:id>/caixacontaprintview', views.CaixaContaPrintView, name="caixa-conta-print-view"),
    path('<uuid:rest>/<uuid:id>/caixacontalancamento', views.CaixaContaLancamento, name="caixa-conta-lancamento-view"),
    path('<uuid:rest>/<uuid:id>/caixalancamento', views.CaixaLancamento, name="caixa-lancamento-view"),
    path('<uuid:rest>/<uuid:id>/<int:lancamento>/delete', views.CaixaLancamentoDelete, name="caixa-lancamento-delete"),
    path('<int:rest>/<int:id>/garcomveraguardandoconta', views.GarcomVerAguardandoConta, name="garcom-ver-aguardando-conta"),
    path('<int:rest>/<int:id>/garcomconfirmacaofecharconta', views.GarcomConfirmacaoFecharConta, name="garcom-confirmacao-fechar-conta"),
    path('<int:rest>/<int:id>/garcomconfirmadofecharconta', views.GarcomConfirmadoFecharConta, name="garcom-confirmado-fechar-conta"),
    path('<uuid:rest>/gerencia', views.vendas, name="vendas"),
    path('<uuid:rest>/<uuid:mesa>/chamar-atendente', views.chamarAtendente, name="chamar-atendente"),
    path('<uuid:rest>/<uuid:mesa>/deschamar-atendente', views.deschamarAtendente, name="deschamar-atendente"),
    path('<uuid:rest>/<uuid:mesa>/deschamar-atendente-confirma', views.deschamarAtendenteConfirma, name="deschamar-atendente-confirma"),



# caixa
    path('caixa', views.CaixaView, name="index-caixa"),
    path('<uuid:rest>/tables/caixa', views.viewTablesCaixa, name="view-tables-caixa"),
    path('<uuid:rest>/<uuid:mesa>/fechar-mesa-zerada', views.fecharMesaZerada, name="fechar-mesa-zerada"),
    path('<uuid:rest>/<uuid:id>/caixacontaview', views.CaixaContaView, name="caixa-conta-view"),
    path('<uuid:rest>/<uuid:id>/contapaga', views.MesaPaga, name="conta-paga"),

# discontinued
    # path('<int:rest>/<int:id>/<int:item>/praca1aceite', views.viewTablesPraca1Aceite, name="view-tables-praca1-aceite"),   
    # path('<int:rest>/<int:id>/<int:item>/praca1entrega', views.viewTablesPraca1Entrega, name="view-tables-praca1-entrega"),     
    # path('<int:rest>/<int:id>/<int:item>/praca1aceitedirect', views.viewTablesPraca1AceiteDirect, name="view-tables-praca1-aceite-direct"),   
    # path('<int:rest>/<int:id>/<int:item>/praca1entregadirect', views.viewTablesPraca1EntregaDirect, name="view-tables-praca1-entrega-direct"),     
    # path('<int:rest>/<int:id>/<int:item>/praca2aceite', views.viewTablesPraca2Aceite, name="view-tables-praca2-aceite"),   
    # path('<int:rest>/<int:id>/<int:item>/praca2entrega', views.viewTablesPraca2Entrega, name="view-tables-praca2-entrega"),     
    # path('<int:rest>/<int:id>/<int:item>/praca2aceitedirect', views.viewTablesPraca2AceiteDirect, name="view-tables-praca2-aceite-direct"),   
    # path('<int:rest>/<int:id>/<int:item>/praca2entregadirect', views.viewTablesPraca2EntregaDirect, name="view-tables-praca2-entrega-direct"),     
    # path('<int:rest>/<int:id>/<int:item>/praca3aceite', views.viewTablesPraca3Aceite, name="view-tables-praca3-aceite"),   
    # path('<int:rest>/<int:id>/<int:item>/praca3entrega', views.viewTablesPraca3Entrega, name="view-tables-praca3-entrega"),     
    # path('<int:rest>/<int:id>/<int:item>/praca3aceitedirect', views.viewTablesPraca3AceiteDirect, name="view-tables-praca3-aceite-direct"),   
    # path('<int:rest>/<int:id>/<int:item>/praca3entregadirect', views.viewTablesPraca3EntregaDirect, name="view-tables-praca3-entrega-direct"),        
    # path('<int:rest>/<int:id>/<int:item>/praca4aceite', views.viewTablesPraca4Aceite, name="view-tables-praca4-aceite"),   
    # path('<int:rest>/<int:id>/<int:item>/praca4entrega', views.viewTablesPraca4Entrega, name="view-tables-praca4-entrega"),     
    # path('<int:rest>/<int:id>/<int:item>/praca4aceitedirect', views.viewTablesPraca4AceiteDirect, name="view-tables-praca4-aceite-direct"),   
    # path('<int:rest>/<int:id>/<int:item>/praca4entregadirect', views.viewTablesPraca4EntregaDirect, name="view-tables-praca4-entrega-direct"),
    
    # path('<int:rest>/<int:id>/<int:item>/garcon', views.PreNewTableItemGarconConfirmed, name="pre-adicionar-item-mesa-garcon-confirmado"),
    # path('<int:rest>/<int:id>/<int:item>/garcon', views.PreNewTableItemGarconConfirmed, name="pre-adicionar-item-mesa-garcon-confirmado"),
    
    # path('<int:rest>/<int:id>/<int:item>/garcomadd', views.PreNewTableItemGarcom, name="pre-adicionar-item-mesa-garcom"),
    # path('<int:rest>/<int:id>/<int:item>/xkplpfl', views.NewTableItem, name="adicionar-item-mesa"),    

    # path('qrcode/', views.newTable),

    # path('praca1', views.Praca1View, name="index-praca1"),
    # path('praca2', views.Praca2View, name="index-praca2"),
    # path('praca3', views.Praca3View, name="index-praca3"),
    # path('praca4', views.Praca4View, name="index-praca4"),
    # path('<int:rest>/tables/praca1', views.viewTablesPraca1, name="view-tables-praca1"),
    # path('<int:rest>/tables/praca2', views.viewTablesPraca2, name="view-tables-praca2"),
    # path('<int:rest>/tables/praca3', views.viewTablesPraca3, name="view-tables-praca3"),
    # path('<int:rest>/tables/praca4', views.viewTablesPraca4, name="view-tables-praca4"),
]

