from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_mail import Message
from .. import db, bcrypt, mail
from ..models.user_model import User

auth = Blueprint('auth', __name__)

# Rota para login
@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={"id": user.id, "email": user.email})
        return jsonify({"access_token": access_token, "message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

# Rota para registro de usuário
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')  # 'client' ou 'provider'

    if not email or not password or not user_type:
        return jsonify({"error": "Email, senha e tipo de usuário são obrigatórios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email já cadastrado"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201

# Rota para recuperação de senha
@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Exemplo simples de envio de email
    reset_link = f"http://example.com/reset-password?email={email}"  # Link fictício
    msg = Message(
        subject="Recuperação de senha",
        sender="seuemail@gmail.com",
        recipients=[email],
        body=f"Olá, clique no link para redefinir sua senha: {reset_link}"
    )
    mail.send(msg)

    return jsonify({"message": "Instruções de recuperação enviadas para o email"}), 200
