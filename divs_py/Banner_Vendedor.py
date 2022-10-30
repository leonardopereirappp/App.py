from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from .botoes import ImageButton, LabelButton
from kivy.app import App
import requests
from functools import partial

class BannerVendedor(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()
        with self.canvas:  # Definindo a cor d fundo para a ScrollView
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_retangulo, size=self.atualizar_retangulo)

        id_vendedor = kwargs["id_vendedor"]
        link = f'https://siteteste0314-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"'  # Quando um link tem um ?, isso significa que tu ta passando parametros para ele
        req = requests.get(link)  # <Response [200]>
        req_json = req.json()
        valor = list(req_json.values())[0]
        foto_perfil, total_vendas = valor["foto_perfil"], valor["total_vendas"]
        meu_app = App.get_running_app()
        imagem = ImageButton(source=f"icones/fotos_perfil/{foto_perfil}", pos_hint={"right": 0.4, "top": 0.9}, size_hint=(0.3, 0.8), on_release=partial(meu_app.carregar_vendasvendedor, valor))
        label_id = LabelButton(text=f"Id vendedor: {id_vendedor}", pos_hint={"right": 0.9, "top": 0.9}, size_hint=(0.5, 0.5), on_release=partial(meu_app.carregar_vendasvendedor, valor))
        label_total = LabelButton(text=f"Total de vendas: R${total_vendas}", pos_hint={"right": 0.9, "top": 0.6}, size_hint=(0.5, 0.5), on_release=partial(meu_app.carregar_vendasvendedor, valor))


        self.add_widget(imagem)
        self.add_widget(label_id)
        self.add_widget(label_total)


    def atualizar_retangulo(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size
