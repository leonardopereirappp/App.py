import secrets
from . import *  # O . refere ao arquivo '__init__.py'
from flask import render_template, url_for, request, flash, redirect, abort
from .forms import FormLogin, FormCriarConta, FormEditarPerfil, FormRedefinirSenha, FormCriarPost, FormCriarComentario
from .models import Usuario, Post, Comentarios
from flask_login import login_user, logout_user, current_user, login_required
import os
from PIL import Image


@app.route('/')
def home():
    return redirect(url_for('posts'))


@app.route('/post', methods=['GET', 'POST'])
def posts():
    posts = Post.query.order_by(Post.id.desc())  # Ordenar os posts em ordem decrescente para quem postar agora, aparecer lá em cima
    coms = Comentarios.query.order_by(Comentarios.id.desc())
    return render_template('home.html', posts=posts, coms=coms)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/esqueciminhasenha', methods=['GET', 'POST'])
def trocar_senha():
    form = FormRedefinirSenha()  # Puxou o Form do redefinir a senha
    if form.validate_on_submit() and 'botao_redefinir_senha' in request.form:   # Confirmou que foi o botão do redefinir a senha
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            senha_crypt = bcrypt.generate_password_hash(form.novasenha.data)
            usuario.senha = senha_crypt
            database.session.commit()
            flash(f"Senha atualizada com sucesso", 'alert-success')  # Exibir mensagem de login bem sucedido  # O data é o resultado do que o cara preencheu
            return redirect(url_for('login'))  # E redirecionar o cara para outro lugar
        else:
            flash(f"Confira seus dados", 'alert-danger')  # Exibir mensagem de login bem sucedido  # O data é o resultado do que o cara preencheu
    else:
        flash(f"Senha Atual incorreta",'alert-danger')  # Exibir mensagem de login bem sucedido  # O data é o resultado do que o cara preencheu
    return render_template('esqueci.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    formlogin = FormLogin()
    formcriarconta = FormCriarConta()
    if formlogin.validate_on_submit() and 'botao_submit_login' in request.form:   # Essas duas condições é para nosso site que tem dois formulário em uma mesma página
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, str(formlogin.senha.data)):
            login_user(usuario, remember=formlogin.lembrar_dados.data)
            flash(f"Login feito com sucesso no e-mail: {formlogin.email.data}", 'alert-success')  # Exibir mensagem de login bem sucedido  # O data é o resultado do que o cara preencheu
            par_next = request.args.get('next')
            if par_next:  # Se existir um caso onde a pessoa clicou em uma página que precisa de acesso, logou e vai ser redirecionada pra página que queria ver
                return redirect(par_next)
            else:
                return redirect(url_for('posts'))  # E redirecionar o cara para outro lugar
        else:
            flash(f"Falha no Login. E-mail ou senha incorretos! ", 'alert-danger')  # Exibir mensagem de login bem sucedido  # O data é o resultado do que o cara preencheu
    if formcriarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f"Conta criada com sucesso no e-mail: {formcriarconta.email.data}", 'alert-success')
        return redirect(url_for('posts'))
    return render_template('login.html', formlogin=formlogin, formcriarconta=formcriarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f"Logout feito com sucesso!", 'alert-success')
    return redirect(url_for('posts'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)  # Para usar uma variável no html, tu precisa passar como parâmetro nessa linha de código, é só pensar: tem que retornar o valor para usar ele.


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    formcriarpost = FormCriarPost()
    if formcriarpost.validate_on_submit() and 'botao_submit_post' in request.form:
        post = Post(titulo=formcriarpost.titulo.data, corpo=formcriarpost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f"Post criado com sucesso", 'alert-success')
        return redirect(url_for('posts'))
    return render_template('criarpost.html', formcriarpost=formcriarpost)


@app.route('/usuarios')
@login_required
def usuarios():
    usuario = Usuario.query.all()
    return render_template('usuarios.html', usuario=usuario)


def salvar_imagem(imagem):
    nome_imagem, extensao = os.path.splitext(imagem.filename)
    nome_imagem = f"{nome_imagem}{secrets.token_hex(8)}{extensao}"  # Adicionar um código aleatório no nome da imagem
    caminho = fr"{app.root_path}\static\fotos_perfil\{nome_imagem}"
    tamanho = (400, 400)  # Reduzir o tamanho da imagem
    imagem_reduzida = Image.open(imagem)  # Reduzir o tamanho da imagem
    imagem_reduzida.thumbnail(tamanho)  # Reduzir o tamanho da imagem
    imagem_reduzida.save(caminho)  # Salvar a imagem na pasta foto_perfil
    return nome_imagem


def atualizar_cursos(form):
    lista_cursos = [var.label.text for var in form if 'curso_' in var.name and var.data]
    return str(';'.join(lista_cursos))


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    form_np = FormRedefinirSenha()
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem   # Mudar o campo foto_perfil do usuario para o novo nome da imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f"Perfil atualizado com sucesso", 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":  # Quando a gente clica no form, tu ta enviando POST, mas quando a página carrega tu tem o GET como resposta, portanto ao carregar a página:
        form.email.data = current_user.email
        form.username.data = current_user.username
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form, form_np=form_np)


@app.route('/post/<post_id>', methods=['GET', 'POST'])  # O post_id é a variável que vai retornar por exemplo /post/1/ ; /post/2 ; /post/3
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)  # O get retorna o post que tem o id igual ao post_id (porque ele é uma chave primária)
    comentario = FormCriarComentario()
    if current_user == post.autor:
        form = FormCriarPost()
        if form:  # Lógica de criar post
            if request.method == 'GET':
                form.titulo.data = post.titulo
                form.corpo.data = post.corpo
            elif form.validate_on_submit():
                post.titulo = form.titulo.data
                post.corpo = form.corpo.data
                database.session.commit()
                flash(f"Post atualizado com sucesso", 'alert-success')
                return redirect(url_for('posts'))
    else:
        form = None
    return render_template('post.html', post=post, form=form, comentario=comentario)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])  # O post_id é a variável que vai retornar por exemplo /post/1/ ; /post/2 ; /post/3
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso', 'alert-success')
        return redirect(url_for('posts'))
    else:
        abort(403)


@app.route('/post/criar_comentario', methods=['GET', 'POST'])
def criar_comentario():
    formcriarcomentario = FormCriarComentario()
    if formcriarcomentario.validate_on_submit() and 'botao_submit_com' in request.form:
        coms = Comentarios(titulo=formcriarcomentario.titulo.data, corpo=formcriarcomentario.corpo.data)
        database.session.add(coms)
        database.session.commit()
        flash(f"Comentário postado com sucesso", 'alert-success')
        return redirect(url_for('posts'))
    return render_template('criar_comentario.html', formcriarcomentario=formcriarcomentario)



