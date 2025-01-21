from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

# Inicialização de extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'seuemail@gmail.com'
    app.config['MAIL_PASSWORD'] = 'suasenha'

    db.init_app(app)
    bcrypt.init_app(app)# Estrutura reorganizada para uma melhor separação de responsabilidades e manutenção
    jwt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from .routes import auth
        app.register_blueprint(auth)
        db.create_all()

    return app