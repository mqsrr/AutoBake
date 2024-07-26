import json
from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from werkzeug.security import check_password_hash

from backend.Models.Customer import Customer
from backend.database.database import db_session

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login_customer():
    json_body = request.json
    email = json_body['email']
    password = json_body['password']

    customer = Customer.query.filter_by(email=email).first()
    if not customer or not check_password_hash(customer.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=customer.id)
    return jsonify({'token': access_token, 'customer-id': customer.id, 'customer-name': customer.name}), HTTPStatus.OK


@auth_bp.route('/auth/signup', methods=['POST'])
def register_customer():
    json_body = request.json
    json_body = str(json_body).replace('\'', '\"')

    customer = json.loads(json_body, object_hook=Customer.customer_decoder)
    existing_customer = Customer.query.filter_by(email=customer.email).first()

    if existing_customer:
        return jsonify({'message': 'Email is already registered'}), 400

    db_session.add(customer)
    db_session.commit()

    access_token = create_access_token(identity=customer.id)
    return jsonify({'token': access_token, 'customer-id': customer.id, 'customer-name': customer.name}), HTTPStatus.CREATED


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response
