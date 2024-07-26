import uuid
from typing import Any

from flask_login import UserMixin
from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import Relationship
from werkzeug.security import generate_password_hash

from backend.Models.Address import Address
from backend.database.database import Base


class Customer(UserMixin, Base):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String(64), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(64), unique=True, nullable=False)

    addresses = Relationship('Address', back_populates='customer', passive_deletes=True)
    orders = Relationship('Order', back_populates='customer', passive_deletes=True)

    def __init__(self, name, email, password, addresses):
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.addresses = addresses

    def to_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'addresses': [address.to_json() for address in self.addresses],
        }

    @staticmethod
    def customer_decoder(customer_dict: dict) -> Any | None:
        if 'name' in customer_dict and 'email' in customer_dict and 'password' in customer_dict and 'street' in customer_dict and 'postcode' in customer_dict:
            return Customer(customer_dict['name'], customer_dict['email'], customer_dict['password'], [Address(customer_dict['street'], customer_dict['postcode'])])
        return None
