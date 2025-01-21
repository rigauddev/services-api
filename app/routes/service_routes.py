from flask import Blueprint, request, jsonify
from ..models.service_model import Service
from .. import db

services = Blueprint('services', __name__)

@services.route('/services', methods=['GET'])
def get_services():
    category = request.args.get('category')
    query = Service.query
    if category:
        query = query.filter_by(category_id=category)
    all_services = query.all()
    return jsonify([{"id": srv.id, "name": srv.name, "description": srv.description, "category_id": srv.category_id} for srv in all_services]), 200

@services.route('/services', methods=['POST'])
def create_service():
    data = request.json
    new_service = Service(name=data['name'], description=data['description'], category_id=data['category_id'], provider_id=data['provider_id'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Serviço criado com sucesso."}), 201