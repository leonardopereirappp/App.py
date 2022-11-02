from . import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))  # Esse método encontra algum item pela PK (Primary Key)


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.png')
    posts = database.relationship('Post', backref='autor', lazy=True)  # Backref serve como uma 'função' para o post, por exemplo: Post().autor nesse caso; O lazy vai retornar todas as informações do autor
    cursos = database.Column(database.String, nullable=False, default='Não informado')  # Um site pro longo prazo seria recomendado uma tabela pros cursos


class Post(database.Model):
    id = database.Column(database.Integer, nullable=True, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Comentarios(database.Model):
    id = database.Column(database.Integer, nullable=True, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
