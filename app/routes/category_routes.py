from flask import Blueprint, request, jsonify
from ..models.category_model import Category
from .. import db

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
def get_categories():
    all_categories = Category.query.all()
    return jsonify([{"id": cat.id, "name": cat.name, "description": cat.description} for cat in all_categories]), 200

@categories.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    new_category = Category(name=data['name'], description=data.get('description'))
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Categoria criada com sucesso."}), 201

@categories.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    category = Category.query.get_or_404(id)
    category.name = data['name']
    category.description = data.get('description')
    db.session.commit()
    return jsonify({"message": "Categoria atualizada com sucesso."}), 200

@categories.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Categoria removida com sucesso."}), 200