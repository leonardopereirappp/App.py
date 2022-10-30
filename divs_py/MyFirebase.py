import requests
from kivy.app import App

class MyFirebase:
    chave_api = 'AIzaSyAAzstdjZyiPpIqJRsmemohFdW_tNp3Wo8'
    pass

    def criar_conta(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.chave_api}'
        info = {'email': email, 'password': senha, 'returnSecureToken': True}
        print(email, senha)
        req = requests.post(url=link, data=info)
        req_dict = req.json()
        if req.ok:
            # req_dict['localId'] # Id do usuário
            # req_dict['refreshToken'] # Token que mantém o usuário logado
            # req_dict['idToken'] # Token de autenticação do usuário
            refreshToken = req_dict['refreshToken']
            local_id = req_dict['localId']
            idToken = req_dict['idToken']
            meu_app = App.get_running_app()
            meu_app.local_id = local_id
            meu_app.id_token = idToken
            with open('refreshToken.txt', 'w') as arquivo:
                arquivo.write(refreshToken)
            link = f'https://siteteste0314-default-rtdb.firebaseio.com/{local_id}.json?auth={idToken}'
            req_id = requests.get(f"https://siteteste0314-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={idToken}")
            id_vendedor = req_id.json()
            info_user = f'{{"foto_perfil": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            req_user = requests.patch(url=link, data=info_user)
            # Atualizar o valor do próximo_id_vendedor
            proximo_id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(url=f'https://siteteste0314-default-rtdb.firebaseio.com/.json?auth={idToken}', data=info_id_vendedor)
            meu_app.carrega_info_usuario()
            print("Passou pelo carregamento")
            meu_app.mudar_tela("homepage")
        else:
            error_message = req_dict['error']['message']
            meu_app = App.get_running_app()
            page_login = meu_app.root.ids['loginpage']  # Aqui não passamos o self.root porque queremos alterar um item da classe no main.py e não nessa daqui
            page_login.ids['message_login'].text = f"{error_message}".capitalize()
            page_login.ids['message_login'].color = (1, 0, 0, 1)

    def acessar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.chave_api}"
        info = {'email': email, 'password': senha, 'returnSecureToken': True}
        req = requests.post(url=link, data=info)
        req_dict = req.json()
        if req.ok:
            refreshToken, local_id, id_token = req_dict['refreshToken'], req_dict['localId'], req_dict['idToken']
            meu_app = App.get_running_app()
            meu_app.local_id = local_id
            meu_app.id_token = id_token
            with open('refreshToken.txt', 'w') as arquivo:
                arquivo.write(refreshToken)
            meu_app.carrega_info_usuario()
            meu_app.mudar_tela("homepage")
        else:
            error_message = req_dict['error']['message']
            meu_app = App.get_running_app()
            page_login = meu_app.root.ids['loginpage']  # Aqui não passamos o self.root porque queremos alterar um item da classe no main.py e não nessa daqui
            page_login.ids['message_login'].text = f"{error_message}".capitalize()
            page_login.ids['message_login'].color = (1, 0, 0, 1)

    def trocar_token(self, refreshtoken):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.chave_api}"
        info = {"grant_type": "refresh_token", "refresh_token": refreshtoken}
        req = requests.post(url=link, data=info)
        req_dict = req.json()
        local_id, id_token = req_dict["user_id"], req_dict["id_token"]
        return local_id, id_token
