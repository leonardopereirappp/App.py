# Vamos falar sobre ScreenManager object, que é uma forma de integrar várias telas em um lugar
# Nela, tu precisa passar um id, é como se fosse uma tabela em sql que precisa de uma primary key

# Para isso tu precisa importar o arquivo, que se assemelha um pouco com c/c++/c#
'#:include {pasta}/{nome}.kv'

ex1 = """
#:include kv/HomePage.kv

ScreenManager:
    id: screen_manager
    HomePage:
        nome: "homepage"
        id: homepage

"""

# Lembrando que tu tem que ir no arquivo , que no (ex1) é o kv/HomePage.kv e adicionar uma 'tag' com o nome da classe criada no Python

'''
<HomePage>:
    Label:
        text: "Home Page"
'''