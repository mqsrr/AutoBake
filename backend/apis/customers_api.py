import json
import uuid
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.Models.Address import Address
from backend.Models.Customer import Customer
from backend.database.database import db_session

customers_bp = Blueprint('customers_bp', __name__)


@customers_bp.route('/customers/me', methods=['GET'])
@jwt_required()
def get_current_customer():
    current_customer = Customer.query.get(uuid.UUID(get_jwt_identity()))
    if current_customer is None:
        return jsonify({'message': 'Couldn\'t find current customer!'}), HTTPStatus.BAD_REQUEST

    return jsonify(current_customer.to_json()), HTTPStatus.OK


@customers_bp.route('/customers', methods=['PUT'])
@jwt_required()
def update_customer():
    json_body = request.json

    customer_name = json_body['name']
    address_json = json_body['addresses']

    address_json = str(address_json).replace('\'', '\"')
    addresses = json.loads(address_json, object_hook=Address.address_decoder)

    customer = Customer.query.get(uuid.UUID(get_jwt_identity()))

    customer.addresses = addresses
    customer.name = customer_name

    db_session.commit()

    return jsonify(customer.to_json()), HTTPStatus.OK
