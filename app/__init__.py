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
    
    # Configurações da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'seuemail@gmail.com'
    app.config['MAIL_PASSWORD'] = 'suasenha'

    # Inicialização das extensões com a instância do Flask
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Importação e registro dos blueprints (rotas)
    with app.app_context():
        from .routes.auth_routes import auth
        from .routes.category_routes import categories
        from .routes.provider_routes import providers
        from .routes.service_routes import services

        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(categories, url_prefix='/categories')
        app.register_blueprint(providers, url_prefix='/providers')
        app.register_blueprint(services, url_prefix='/services')


        # Criação do banco de dados
        db.create_all()

        print("Rotas registradas:")
        for rule in app.url_map.iter_rules():
            print(f"{rule} -> {rule.endpoint}")


    return app


