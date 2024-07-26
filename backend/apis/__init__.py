from flask import Flask

from backend.apis.auth_api import auth_bp
from backend.apis.customers_api import customers_bp
from backend.apis.orders_api import orders_bp
from backend.database.database import init_db


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(customers_bp)


def initialize_db() -> None:
    from backend.Models import Customer, Address, Order, Pizza
    init_db()
