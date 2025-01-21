from flask import Blueprint, request, jsonify
from ..models.user_model import User
from .. import db, bcrypt, mail, jwt
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask_jwt_extended import create_access_token

serializer = URLSafeTimedSerializer('sua-chave-secreta')

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password, user_type=data['user_type'])
    db.session.add(new_user)
    db.session.commit()

    # Envia e-mail de validação
    token = serializer.dumps(data['email'], salt='email-confirm')
    confirm_url = f"http://localhost:5000/confirm_email/{token}"
    msg = Message('Confirme seu e-mail', sender='seuemail@gmail.com', recipients=[data['email']])
    msg.body = f'Clique no link para confirmar seu e-mail: {confirm_url}'
    mail.send(msg)

    return jsonify({"message": "Usuário registrado. Verifique seu e-mail para confirmação."}), 201

@auth.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            return jsonify({"message": "E-mail confirmado com sucesso."})
    except Exception as e:
        return jsonify({"error": "Token inválido ou expirado."}), 400

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        if not user.is_verified:
            return jsonify({"error": "E-mail não confirmado."}), 401
        access_token = create_access_token(identity={"id": user.id, "user_type": user.user_type})
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Credenciais inválidas."}), 401

@auth.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        token = serializer.dumps(data['email'], salt='password-reset')
        reset_url = f"http://localhost:5000/reset_password/{token}"
        msg = Message('Redefinição de Senha', sender='seuemail@gmail.com', recipients=[data['email']])
        msg.body = f'Clique no link para redefinir sua senha: {reset_url}'
        mail.send(msg)
        return jsonify({"message": "Instruções para redefinir a senha enviadas por e-mail."}), 200
    return jsonify({"error": "E-mail não encontrado."}), 404

@auth.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            data = request.json
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            db.session.commit()
            return jsonify({"message": "Senha redefinida com sucesso."})
    except Exception as e:
        return jsonify({"error": "Token inválido ou expirado."}), 400
