from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class BannerVenda(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.rows = 1  # Aqui é a quantidade de linhas que o GridLayout deve ter

        with self.canvas:  # Definindo a cor d fundo para a ScrollView
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_retangulo, size=self.atualizar_retangulo)


        cliente, foto_cliente, produto, foto_produto = kwargs['cliente'], kwargs['foto_cliente'], kwargs['produto'], kwargs['foto_produto']
        data, preco, unidade, quantidade = kwargs['data'], float(kwargs['preco']), kwargs['unidade'], kwargs['quantidade']

        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75), source=f"icones/fotos_clientes/{foto_cliente}")
        esquerda_label = Label(text=f"{cliente}".capitalize(), size_hint=(1, 0.2), pos_hint={'right': 1, 'top': 0.2})
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        meio = FloatLayout()
        meio_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75), source=f"icones/fotos_produtos/{foto_produto}")
        meio_label = Label(text=f"{produto}".capitalize(), size_hint=(1, 0.2), pos_hint={'right': 1, 'top': 0.2})
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        direita = FloatLayout()
        direita_label_data = Label(text=f"Data: {data}", pos_hint={'right': 1, 'top': 0.9}, size_hint=(1, 0.33))
        direita_label_preco = Label(text=f"Preço: {preco:,.2f}", pos_hint={'right': 1, 'top': 0.65}, size_hint=(1, 0.33))
        direita_label_qtde = Label(text=f"{quantidade} {unidade}", pos_hint={'right': 1, 'top': 0.4}, size_hint=(1, 0.33))
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_qtde)
        direita.add_widget(direita_label_data)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_retangulo(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size