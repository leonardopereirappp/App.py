from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import Usuario
from flask_login import current_user


class FormRedefinirSenha(FlaskForm):
    email = EmailField('Digite o seu E-mail: ', validators=[DataRequired()])
    senha = PasswordField('Digite sua Senha atual: ', validators=[DataRequired(), Length(6, 20)])
    novasenha = PasswordField('Redefinir sua Senha atual: ', validators=[DataRequired(), Length(6, 20)])
    novasenhab = PasswordField('Redefinir sua Senha atual: ', validators=[DataRequired(), Length(6, 20)])
    botao_redefinir_senha = SubmitField('Redefinir Senha')


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário: ', validators=[DataRequired()])
    email = EmailField('Digite o seu E-mail: ', validators=[DataRequired()])
    senha = PasswordField('Digite sua Senha: ', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmação de senha: ', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):  # o validation submit recebe toda função que começa com validate_ automaticamente.
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:  # Se o input (e-mail) já existir, mostra isso
            raise ValidationError("E-mail já cadastrado.")


class FormLogin(FlaskForm):
    email = EmailField('Digite o seu E-mail: ', validators=[DataRequired()])
    senha = PasswordField('Digite sua Senha: ', validators=[DataRequired(), Length(6, 20)])
    esqueci = StringField('Esqueci minha Senha: ')
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário: ', validators=[DataRequired()])
    email = EmailField('Redefinir o seu E-mail: ', validators=[DataRequired()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['png', 'jpg'])])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editarperfil = SubmitField('Confirmar mudanças')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail!')


class FormCriarPost(FlaskForm):
    titulo = StringField('Assunto: ', validators=[DataRequired(), Length(1, 140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit_post = SubmitField('Criar Post')
    botao_submit_post2 = SubmitField('Editar Post')


class FormCriarComentario(FlaskForm):
    titulo = StringField('Assunto: ', validators=[DataRequired(), Length(1, 140)])
    corpo = TextAreaField('Escreva seu comentário aqui', validators=[DataRequired()])
    botao_submit_com = SubmitField('Criar Comentario')
    botao_submit_com2 = SubmitField('Editar Comentario')
