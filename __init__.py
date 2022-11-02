from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b04d272824427f6330911667b806746f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_projeto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

database = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Para as funções com login_required no routes
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar essa página!'
login_manager.login_message_category = 'alert-info'


from . import routes  # Trás a informação aqui porque se importar antes, vai dar erro porque precisa-se do app para importar o routes
