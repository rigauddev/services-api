from flask import Blueprint, request, jsonify
from ..models.user_model import User
from .. import db, bcrypt

providers = Blueprint('providers', __name__)

@providers.route('/providers', methods=['POST'])
def register_provider():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_provider = User(email=data['email'], password=hashed_password, user_type='provider')
    db.session.add(new_provider)
    db.session.commit()
    return jsonify({"message": "Prestador cadastrado com sucesso."}), 201