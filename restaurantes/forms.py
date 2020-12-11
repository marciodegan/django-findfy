from django import forms

from .models import Restaurante, AtendentesRestaurante, AtendentesMaster, CozinhaRestaurante, BarmanRestaurante, CaixasRestaurante, OpenDate
from tables.models import TableNumber
from menus.models import CategoriasMenu, Menu, ItensMenu, IngredientesItem


class OpenDateForm(forms.ModelForm):

    class Meta:
        model = OpenDate
        fields = ('date', 'opened')
        labels = {
            'date': 'Data Operacional',
            'opened': 'Local Aberto'
        }
        help_texts = {
            'date': 'É obrigatório definir a data do funcionamento. Preferencialmente ser a data atual.',
            'opened': 'Se não estiver, o local não abre mesas, nem recebe pedidos.',                        
        }

class NewPhotoForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = ('logo',)
        labels = {
            'logo': 'Adicione uma foto',
                     
        }


class NewRestauranteForm(forms.ModelForm):
    
    class Meta:
        model = Restaurante
                
        fields = ('name',)
        labels = {
            'name': 'Nome do estabelecimento:',
                     
        }
        help_texts = {
            'name': 'Ex.: Restaurante da Maria',            
        } 
       

class NewLocalForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = ('name',)
        labels = {
            'name': 'Nome do estabelecimento:',                     
        }
        

class NewLogoForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = ('logo',)
        labels = {
            'logo': 'Logomarca (para o menu)',
                     
        }

class NewPhotoBackForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = ('imagem_menu',)
        labels = {
            'imagem_menu': 'Imagem de Fundo',
                     
        }

class NewAddressForm(forms.ModelForm):
   
    class Meta:
        model = Restaurante
        fields = ('endereco','bairro', 'cidade', 'estado', 'telefone', 'zap', )
        labels = {
            'endereco': 'Endereço',
        }
        


class EditLocalForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = ('name', 'endereco', 'bairro', 'cidade', 'estado', 'telefone', 'zap', 'ativo', 'cliente_pede', 'quem_esta', 'mensagem_do_dia',)
        labels = {
            'name': 'Nome do estabelecimento:',
            'cliente_pede': 'Cliente pode pedir pelo menu',
            'ativo': 'Ativo',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'quem_esta': 'Quem está no local'                     
        }


class NewTableForm(forms.ModelForm):

    class Meta:
        model = TableNumber
        fields = ('table_number',)
        labels = {
            'table_number': 'Número da Mesa',
        }
        help_texts = {
            'table_number': 'Numeração das suas mesas. Ex.: 1, 2, 3...Não pode repetir o mesmo número',            
        } 


class NewCategoriaForm(forms.ModelForm):

    class Meta:
        model = CategoriasMenu
        fields = ('categoria', 'ordem_categoria')
        labels = {
            'ordem_categoria': 'Posição no menu',
        }
        help_texts = {
            'categoria': 'Ex.: Pratos / Bebidas / Drinks',
            'ordem_categoria': 'Define a ordem de apresentação no menu',
            
        } 

class NewMenuForm(forms.ModelForm):
    
    class Meta:
        model = Menu
        fields = ('nome', 'ativo',)
        labels = {
            'nome': 'Nome para o menu:',}
        
        help_texts = {
            'nome': 'Ex.: Jantar / Noite / Almoço',
        }


class NewProdutoForm(forms.ModelForm):

    class Meta:
        model = ItensMenu
        fields = ('status', 'item', 'descricao', 'categoria', 'name_image', 'menus', 'price', 'cozinha', 'bar',)
        labels = {
            'item': 'Nome do produto',
            'price': 'Preço',
            'descricao': 'Descrição',
            'name_image': 'Foto',
            'menus': 'Menus',
            'status': 'Mostrar produto no menu',
            'cozinha': 'Cozinha',
            'bar': 'Bar',
            'price': 'Preço',
        }
        help_texts = {
            'descricao': 'Aparece no menu, logo abaixo do nome. Ex.: Acompanha arroz e fritas...',
            'menus': 'Quais os menus que este produto faz parte',
            'cozinha': 'Indica se este item vai para cozinha ao ser solicitado',
            'bar': 'Indica se este item vai para cozinha ao ser solicitado',
        }    


    def __init__(self, local, *args, **kwargs):
        super(NewProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriasMenu.objects.filter(restaurante=local)
        self.fields['menus'].queryset = Menu.objects.filter(restaurante=local)
    
    
class EditProdutoForm(forms.ModelForm):

    class Meta:
        model = ItensMenu
        fields = ('item', 'descricao', 'categoria', 'name_image', 'menus', 'price', 'status', 'cozinha', 'bar', 'praca1', 'ingpraca1a', 'ingpraca1b','ingpraca1c','ingpraca1d','praca2', 'ingpraca2a','ingpraca2b','ingpraca2c','ingpraca2d','praca3', 'ingpraca3a','ingpraca3b','ingpraca3c','ingpraca3d','praca4','ingpraca4a','ingpraca4b','ingpraca4c','ingpraca4d',)
        labels = {
            'item': 'Nome do produto',
            'price': 'Preço',
            'descricao': 'Descrição',
            'name_image': 'Foto',
            'menus': 'Menus que este produto faz parte',
            'status': 'Produto Ativo',
            'cozinha': 'VAI P/ COZINHA',
            'bar': 'VAI P/ BAR',
            'price': 'Preço',
            'praca1': 'VAI p/ PRAÇA # 1',
            'praca2': 'VAI p/ PRAÇA # 2',
            'praca3': 'VAI p/ PRAÇA # 3',
            'praca4': 'VAI p/ PRAÇA # 4',
            'ingpraca1a': 'Praça#1 / Ingredientes 1',
            'ingpraca1b': 'Praça#1 / Ingredientes 2',
            'ingpraca1c': 'Praça#1 / Ingredientes 3',
            'ingpraca1d': 'Praça#1 / Ingredientes 4',
            'ingpraca2a': 'Praça#2 / Ingredientes 1',
            'ingpraca2b': 'Praça#2 / Ingredientes 2',
            'ingpraca2c': 'Praça#2 / Ingredientes 3',
            'ingpraca2d': 'Praça#2 / Ingredientes 4',
            'ingpraca3a': 'Praça#3 / Ingredientes 1',
            'ingpraca3b': 'Praça#3 / Ingredientes 2',
            'ingpraca3c': 'Praça#3 / Ingredientes 3',
            'ingpraca3d': 'Praça#3 / Ingredientes 4',
            'ingpraca4a': 'Praça#4 / Ingredientes 1',
            'ingpraca4b': 'Praça#4 / Ingredientes 2',
            'ingpraca4c': 'Praça#4 / Ingredientes 3',
            'ingpraca4d': 'Praça#4 / Ingredientes 4',

        }    


    def __init__(self, local, *args, **kwargs):
        super(EditProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriasMenu.objects.filter(restaurante=local)
        self.fields['menus'].queryset = Menu.objects.filter(restaurante=local)
    

# class EditIngredientesForm(forms.ModelForm):
#     class Meta:
#         model = IngredientesItem
#         fields = ('ingredientes', 'quantity')
#         labels = {
#             'item': 'Nome do produto',
#             'ingredientes': 'Ingrediente',
#             'quantity': 'Quantidade',
#         }


class NewAtendenteForm(forms.ModelForm):
    class Meta:
        model = AtendentesRestaurante
        fields = ('atendente', 'status', 'ordering')
        labels = {
            'atendente': 'Selecionar Atendente',
            'status': 'ATIVO',
            'ordering': 'Ordernação para tela Master',
        }
        help_texts = {
            'ordering': 'Não importa o número, mas é obrigatório selecionar.'
        }    


class NewAtendenteMasterForm(forms.ModelForm):

    class Meta:
        model = AtendentesMaster
        fields = ('atendentemaster', 'status')
        labels = {
            'atendentemaster': 'Selecionar Atendente Master',
            'status': 'ATIVO'
        }
        help_texts = {
            'atendentemaster': 'Utilize atendentes MASTER para gerenciar solicitações de todos atendentes em um computador central no salão'
        }    


class NewCozinhaForm(forms.ModelForm):

    class Meta:
        model = CozinhaRestaurante
        fields = ('cozinha', 'status')
        labels = {
            'cozinha': 'Selecionar Cozinheiro',
            'status': 'ATIVO'
        }    


class NewBarForm(forms.ModelForm):

    class Meta:
        model = BarmanRestaurante
        fields = ('barman', 'status')
        labels = {
            'barman': 'Selecionar Atendente',
            'status': 'ATIVO'
        }


class NewCaixaForm(forms.ModelForm):

    class Meta:
        model = CaixasRestaurante
        fields = ('caixa', 'status')
        labels = {
            'caixa': 'Selecionar Caixa',
            'status': 'ATIVO'
        }
