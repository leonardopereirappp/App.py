'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'b04d272824427f6330911667b806746f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_projeto.db'

database = SQLAlchemy(app)

database.create_all()    # Depois da primeira vez criada, pode se comentar essa linha de código'''

'''usuario = Usuario(username="Leonardo", email="leonardopereirappp@gmail.com", senha="123456")  # Adicionou uma variável com as informações, mas não está no Banco de Dados [ PYTHON ]
usuario2 = Usuario(username="Rayane", email="Rayysantss@gmail.com", senha="123456")

# Agora bora adicionar essas informações no banco de dados

database.session.add(usuario)  # Adicionou na 'tabela temporária' que depois tem que dar um .commit para adicionar ao banco de dados oficial
database.session.add(usuario2)

database.session.commit()

print(Usuario.query.all())  # Mostrar as variáveis { COM INFORMAÇÕES } inseridas no bd
print(Usuario.query.first())  # Mostrar a primeira variável criada que foi inserida no bd

usuario_teste = Usuario.query.first()
print(usuario_teste.email)
print(usuario_teste.username)
print(usuario_teste.foto_perfil)

# usuario_ray = Usuario.query.filter_by(email='Rayysantssgmail.com')  # Esse filter_by é como se fosse o where do SQL [select * from Usuario where email= 'Rayysantssgmail.com']

# A linha acima vai retornar uma lista de dados com o email => 'Rayysantssgmail.com'

usuario_ray = Usuario.query.filter_by(email='Rayysantss@gmail.com').first()
print(f'\n{usuario_ray.email}')
print(usuario_ray.username)
print(usuario_ray.id)
print(usuario_ray.cursos)


# Adicionando coisas na tabela Post

post1 = Post(titulo="Post do Leozin", corpo="Se liga meu, cê é pixuruco?", id_usuario=1)
database.session.add(post1)
database.session.commit()
print(f"\n{Post.query.all()}")

mostrar_post1 = Post.query.first()

print(mostrar_post1.corpo)
print(mostrar_post1.titulo)
print(mostrar_post1.id_usuario)
'''