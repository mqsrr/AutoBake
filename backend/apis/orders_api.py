import json
import uuid
from http import HTTPStatus
from multiprocessing.pool import ThreadPool

from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.Models.Customer import Customer
from backend.Models.Order import Order
from backend.Models.Pizza import Pizza
from backend.Services.Oven import Oven
from backend.Services.OvenService import OvenService
from backend.database.database import db_session


def connect_to_boards(*args):
    results = []

    with ThreadPool(len(args)) as thread_pool:
        for com_port in args:
            result = thread_pool.apply_async(lambda port: CustomTelemetrix(com_port=port), (com_port,))
            results.append(result)
        return [result.get() for result in results]


def connect_to_ovens(*args):
    arduino_boards = connect_to_boards(*args)
    current_board_id = 1
    list_of_ovens = []

    for arduino_board in arduino_boards:
        list_of_ovens.append(Oven(arduino_board, current_board_id))
        current_board_id += 1

    return list_of_ovens


orders_bp = Blueprint('orders', __name__)
ovens = connect_to_ovens('/dev/cu.usbserial-110')
oven_service = OvenService(ovens)


@orders_bp.route('/dashboards/ovens')
def oven_dashboard():
    return render_template('oven-dashboard.html',
                           ovens=oven_service.ovens,
                           orders_queue=oven_service.order_queue,
                           pizzas_in_queue_to_cook=oven_service.pizza_queue)


@orders_bp.route('/dashboards/orders')
def order_dashboard():
    return render_template('order-dashboard.html', orders=oven_service.order_queue)


@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.filter_by(customer_id=uuid.UUID(get_jwt_identity())).all()
    return jsonify([order.to_json() for order in orders]), HTTPStatus.OK


@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    data = str(data['pizzas']).replace('\'', '\"')
    pizzas = json.loads(data, object_hook=Pizza.pizza_decoder)

    customer = Customer.query.get(uuid.UUID(get_jwt_identity()))
    order = Order(customer, pizzas)

    db_session.add(order)
    db_session.commit()

    print(order.customer.name)
    oven_service.add_order_into_queue(order)
    return jsonify(order.to_json()), HTTPStatus.CREATED


@orders_bp.route('/orders/<string:orderId>', methods=['DELETE'])
@jwt_required()
def delete_order(orderId: str):
    order = Order.query.get(uuid.UUID(orderId))
    if order is None:
        return jsonify({'message': 'Order not found'}), HTTPStatus.NOT_FOUND

    db_session.delete(order)
    db_session.commit()
    return jsonify({'message': 'Order deleted'}), HTTPStatus.NO_CONTENT
