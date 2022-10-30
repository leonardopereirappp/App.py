from kivy.app import App
from kivy.lang import Builder
from divs_py.telas import *
from divs_py.botoes import *
from divs_py.Banner_Venda import BannerVenda
from divs_py.MyFirebase import MyFirebase
from divs_py.Banner_Vendedor import BannerVendedor
import os
import requests
from datetime import date
from functools import partial  # Essa importação serve pra passar um parametro em uma função que está sendo usada como parametro

GUI = Builder.load_file('main.kv')  # A parte visual (interface gráfica) se chama GUI


class MainApp(App):

    clientes = None
    produtos = None
    unidades = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI  # É como se fosse o return do flask para ir para o html, mas no site!

    def on_start(self):
        # carregar as fotos de perfil
        arquivos = os.listdir('icones/fotos_perfil')
        pagina_fotoperfil = self.root.ids['fotoperfilpage'].ids['lista_fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f'icones/fotos_perfil/{foto}', on_release=partial(self.mudar_fotoperfil, foto))
            pagina_fotoperfil.add_widget(imagem)

        # carregar as fotos dos clientes
        arquivos = os.listdir('icones/fotos_clientes')
        pagina_adicionar_vendas = self.root.ids['adicionarvendaspage'].ids['lista_clientes']
        for foto_clientes in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_clientes}", on_release=partial(self.selecionar_clientes, foto_clientes))
            nome, _ = os.path.splitext(foto_clientes)  # Separar o nome da extensão em duas variáveis: exemplo: Nome.png => Nome, .png
            nome = f"{nome}".capitalize()
            label = LabelButton(text=nome, on_release=partial(self.selecionar_clientes, foto_clientes))
            pagina_adicionar_vendas.add_widget(imagem)
            pagina_adicionar_vendas.add_widget(label)

        # carregar as fotos dos produtos
        arquivos = os.listdir('icones/fotos_produtos')
        pagina_adicionar_vendas = self.root.ids['adicionarvendaspage'].ids['lista_produtos']
        for foto_produtos in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produtos}", on_release=partial(self.selecionar_produtos, foto_produtos))
            nome, _ = os.path.splitext(foto_produtos)
            nome = f"{nome}".capitalize()
            label = LabelButton(text=nome, on_release=partial(self.selecionar_produtos, foto_produtos))
            pagina_adicionar_vendas.add_widget(imagem)
            pagina_adicionar_vendas.add_widget(label)

        # carregar a data
        data = self.root.ids['adicionarvendaspage'].ids['data_atual']
        data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"
        self.data = date.today().strftime('%d/%m/%Y')


        # carrega as infos do usuário
        self.carrega_info_usuario()

    def mudar_fotoperfil(self, foto, *args):
        sitesj_bd = fr'https://siteteste0314-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}'  # Sempre nesse tipo de link, coloque o .json no final
        self.root.ids['foto_perfil'].source = f'icones/fotos_perfil/{foto}'
        req = requests.patch(f'{sitesj_bd}', data=f'{{"foto_perfil": "{foto}"}}')  # As chaves duplas é um dict e a simples é a variável na f-string
        self.foto_perfil = foto
        self.mudar_tela("ajustespage")

    def add_vendedor(self, id_vendedor):
        req = requests.get(url=f'https://siteteste0314-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"')
        req_json = req.json()
        if req_json == {}:
            # Exibir a mensagem de fracasso com a cor vermelha
            pagina_adicionarvendedor = self.root.ids["adicionarvendedorespage"].ids["mensagem_add_vendedor"]
            pagina_adicionarvendedor.text = "Usuário não encontrado"
            pagina_adicionarvendedor.color = (1, 0, 0, 1)
        else:
            equipe = self.equipe.split(",")
            if id_vendedor in equipe:
                # Exibir a mensagem de fracasso com a cor 'ciana'
                faz_parte_equipe = self.root.ids["adicionarvendedorespage"].ids["mensagem_add_vendedor"]
                faz_parte_equipe.text = "Vendedor já faz parte da equipe"
                faz_parte_equipe.color = (0.46, 0.9, 1, 1)
            elif id_vendedor == self.id_vendedor:
                faz_parte_equipe = self.root.ids["adicionarvendedorespage"].ids["mensagem_add_vendedor"]
                faz_parte_equipe.text = "Você já faz parte da equipe"
                faz_parte_equipe.color = (0.46, 0.9, 1, 1)
            else:
                # Concatenando o self.equipe antigo com o atual
                self.equipe = self.equipe + f",{id_vendedor}"
                info = f'{{"equipe": "{self.equipe}"}}'
                # Adicionando as informações no banco de dados
                req = requests.patch(url=fr'https://siteteste0314-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data=info)
                pagina_listar_vendedores = self.root.ids["listarvendedorespage"].ids["lista_vendedores"]
                # Atualizando os itens no visual (adicionando o novo banner na página do banner_vendedor) em tempo real [sem precisar reiniciar o app]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor)
                pagina_listar_vendedores.add_widget(banner_vendedor)
                # Exibir a mensagem de sucesso com a cor verde
                success_work = self.root.ids["adicionarvendedorespage"].ids["mensagem_add_vendedor"]
                success_work.text = "Vendedor adicionado com sucesso"
                success_work.color = (0, 1, 0, 1)


    def carrega_info_usuario(self):

        try:
            with open("refreshToken.txt", "r") as arquivo:
                refreshToken = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refreshToken)
            self.local_id = local_id
            self.id_token = id_token
            # Pegar infos do usuário no database
            sitesj_bd = fr'https://siteteste0314-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}'  # Sempre nesse tipo de link, coloque o .json no final
            bd_info = requests.get(sitesj_bd).json()
            # Preencher a foto de perfil
            foto_perfil = bd_info['foto_perfil']
            self.foto_perfil = foto_perfil
            self.root.ids['foto_perfil'].source = f'icones/fotos_perfil/{foto_perfil}'
            # Preencher ID único
            id_vendedor = bd_info['id_vendedor']
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids["ajustespage"]
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID único é: {id_vendedor}"
            # Preenche o total de vendas
            total_vendas = bd_info["total_vendas"]
            self.total_vendas = total_vendas
            pagina_principal = self.root.ids["homepage"]
            pagina_principal.ids["total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {total_vendas}[/b]"
            try:
                vendas = bd_info['vendas']
                self.vendas = vendas
                lista_vendas = self.root.ids['homepage'].ids['lista_vendas']
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                         produto=venda['produto'], foto_produto=venda['foto_produto'], data=venda['data'],
                                         preco=venda['preco'], unidade=venda['unidade'], quantidade=venda['quantidade'])
                    lista_vendas.add_widget(banner)
            except Exception as erro:
                print(erro)
                pass
            # Preenche os vendedores da equipe
            equipe = bd_info['equipe']
            self.equipe = equipe
            lista_equipe = equipe.split(',')
            pagina_listar_vendedores = self.root.ids["listarvendedorespage"].ids["lista_vendedores"]
            for id_outro_vendedor in lista_equipe:
                if id_outro_vendedor != "":
                    banner_vendedor = BannerVendedor(id_vendedor=id_outro_vendedor)
                    pagina_listar_vendedores.add_widget(banner_vendedor)

            self.mudar_tela("homepage")
        except Exception:
            pass

    def mudar_tela(self, id_tela):  # Vai receber o id da página, lá do .kv
        gerenciador_telas = self.root.ids["screen_manager"]  # Pegar o gerenciador de telas
        gerenciador_telas.current = id_tela  # Mudar para a tela que quer

    def muda_tela_troca_foto(self, id_tela):
        self.mudar_tela(id_tela)
        self.root.ids['foto_perfil'].source = f'icones/fotos_perfil/{self.foto_perfil}'

    def selecionar_clientes(self, foto, *args):
        # Pintar de azul a letra do item selecionado
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"].ids["lista_clientes"]
        texto_pagina = self.root.ids["adicionarvendaspage"].ids["selecionar_clientes"]
        self.clientes = f"{foto}".replace(".png","")
        self.foto_clientes = foto
        texto_pagina.color = (1, 1, 1, 1)
        for item in list(pagina_adicionar_vendas.children):
            item.color = (1, 1, 1, 1)
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 0.76, 0.8, 1)
            except Exception:
                pass

    def selecionar_produtos(self, foto, *args):
        # Pintar de azul a letra do item selecionado
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"].ids["lista_produtos"]
        texto_pagina = self.root.ids["adicionarvendaspage"].ids["selecionar_produto"]
        self.produtos = f"{foto}".replace(".png","")
        self.foto_produtos = foto
        texto_pagina.color = (1, 1, 1, 1)
        for item in list(pagina_adicionar_vendas.children):
            item.color = (1, 1, 1, 1)
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 0.76, 0.8, 1)
            except Exception:
                pass

    def selecionar_unidades(self, id, *args):
        self.unidades = f"{id}".replace("unidades_","")
        # Pintar de azul a letra do item selecionado
        for item in self.root.ids["adicionarvendaspage"].ids:
            if "unidades" in item and id == item:
                self.root.ids["adicionarvendaspage"].ids[item].color = (0, 0.76, 0.8, 1)
            elif "unidades" in item:
                self.root.ids["adicionarvendaspage"].ids[item].color = (1, 1, 1, 1)

    def adicionar_venda(self):
        preco, quantidade = self.root.ids["adicionarvendaspage"].ids["preco_total"].text, self.root.ids["adicionarvendaspage"].ids["qtde_total"].text
        cliente, produto, unidade = self.clientes, self.produtos, self.unidades
        if not cliente:
            self.root.ids["adicionarvendaspage"].ids["selecionar_clientes"].color = (1, 0, 0, 1)
        if not produto:
            self.root.ids["adicionarvendaspage"].ids["selecionar_produto"].color = (1, 0, 0, 1)
        if not unidade:
            self.root.ids["adicionarvendaspage"].ids["unidades_kg"].color = (1, 0, 0, 1)
            self.root.ids["adicionarvendaspage"].ids["unidades_unidades"].color = (1, 0, 0, 1)
            self.root.ids["adicionarvendaspage"].ids["unidades_litros"].color = (1, 0, 0, 1)
        if not preco:
            self.root.ids["adicionarvendaspage"].ids["preco_total_texto"].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
                self.root.ids["adicionarvendaspage"].ids["preco_total_texto"].color = (1, 1, 1, 1)
            except Exception:
                self.root.ids["adicionarvendaspage"].ids["preco_total_texto"].color = (1, 0, 0, 1)
        if not quantidade:
            self.root.ids["adicionarvendaspage"].ids["qtde_total_texto"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = int(quantidade)
                self.root.ids["adicionarvendaspage"].ids["qtde_total_texto"].color = (1, 1, 1, 1)
            except Exception:
                self.root.ids["adicionarvendaspage"].ids["qtde_total_texto"].color = (1, 0, 0, 1)
        if cliente and produto and unidade and preco and quantidade:
            foto_cliente, foto_produto, data = self.foto_clientes, self.foto_produtos, self.data
            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}", "foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", "preco": "{preco}", "quantidade": "{quantidade}"}}'
            link = f"https://siteteste0314-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}"
            requests.post(url=link, data=info)
            # No final de tudo, volta a ser tudo None
            self.clientes = None
            self.produtos = None
            self.unidades = None
            banner = BannerVenda(cliente=cliente, foto_cliente=foto_cliente, produto=produto, foto_produto=foto_produto, data=data, preco=preco, unidade=unidade, quantidade=quantidade)
            self.root.ids['homepage'].ids['lista_vendas'].add_widget(banner)
            link = f"https://siteteste0314-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}"
            req = requests.get(url=link)
            total_vendas = float(req.json())
            total_vendas += preco
            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(f"https://siteteste0314-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}", data=info)
            self.root.ids["homepage"].ids["total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {total_vendas}[/b]"
            self.mudar_tela("homepage")
            pass
        pass

    def carregar_todas_vendas(self):
        pagina_todasvendas = self.root.ids["todasvendaspage"].ids["lista_vendas"]
        for item in list(pagina_todasvendas.children):
            pagina_todasvendas.remove_widget(item)
        # Preencher a página todas as vendas page e redirecionar para a página
        # Pegar infos da empresa
        sitesj_bd = r'https://siteteste0314-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"'  # Sempre nesse tipo de link, coloque o .json no final
        bd_info = requests.get(sitesj_bd).json()
        # Preencher a foto da empresa
        self.root.ids['foto_perfil'].source = f'icones/fotos_perfil/hash.png'
        self.total_vendas_hash = 0
        for id_usuario in bd_info:
            try:
                vendas = bd_info[id_usuario]["vendas"]
                for id_vendas in vendas:
                    venda = vendas[id_vendas]
                    cliente, foto_cliente, produto, foto_produto, data, preco, unidade, quantidade = venda["cliente"], venda["foto_cliente"], venda["produto"], venda["foto_produto"], venda["data"], venda["preco"], venda["unidade"], venda["quantidade"]
                    self.total_vendas_hash += float(preco)
                    banner = BannerVenda(cliente=cliente, foto_cliente=foto_cliente, produto=produto, foto_produto=foto_produto, data=data, preco=preco, unidade=unidade, quantidade=quantidade)
                    self.root.ids['todasvendaspage'].ids['lista_vendas'].add_widget(banner)
            except Exception as erro:
                pass

        # Preenche o total de vendas
        self.root.ids["todasvendaspage"].ids["total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {self.total_vendas_hash}[/b]"
        self.mudar_tela("todasvendaspage")

    def carregar_vendasvendedor(self, dict_info_vendedor, *args):
        self.root.ids["vendasoutrovendedorpage"].ids["total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {dict_info_vendedor['total_vendas']}[/b]"
        self.root.ids["foto_perfil"].source = f'icones/fotos_perfil/{dict_info_vendedor["foto_perfil"]}'
        try:
            vendas = dict_info_vendedor["vendas"]
            pagina_todasvendas = self.root.ids["vendasoutrovendedorpage"].ids["lista_vendas"]
            for item in list(pagina_todasvendas.children):
                pagina_todasvendas.remove_widget(item)
            for id_vendas in vendas:
                venda = vendas[id_vendas]
                cliente, foto_cliente, produto, foto_produto, data, preco, unidade, quantidade = venda["cliente"], venda["foto_cliente"], venda["produto"], venda["foto_produto"], venda["data"], venda["preco"], venda["unidade"], venda["quantidade"]
                banner = BannerVenda(cliente=cliente, foto_cliente=foto_cliente, produto=produto, foto_produto=foto_produto, data=data, preco=preco, unidade=unidade, quantidade=quantidade)
                self.root.ids['vendasoutrovendedorpage'].ids['lista_vendas'].add_widget(banner)
        except Exception as erro:
            print(erro)
        self.mudar_tela("vendasoutrovendedorpage")

# No kivy, cada tela de app (html) tem uma classe única, assim como o Flask com o @app.route({html})
app = MainApp()
app.run()
