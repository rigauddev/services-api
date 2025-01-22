from flask import Blueprint, request, jsonify
from ..models.user_model import User
from .. import db, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login bem-sucedido"}), 200
    return jsonify({"message": "Credenciais inválidas"}), 401

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

    new_user = User(email=email, password=password, user_type='client')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201
