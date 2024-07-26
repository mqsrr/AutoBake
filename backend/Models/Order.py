from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Relationship

from backend.Models.Customer import Customer
from backend.Models.OrderState import OrderState
from backend.Models.Pizza import Pizza
from backend.database.database import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    pizzas = Relationship('Pizza', back_populates='order', passive_deletes=True)
    customer = Relationship('Customer', back_populates='orders', passive_deletes=True)

    order_state = OrderState.PENDING

    def __init__(self, customer: Customer, pizzas: [Pizza]) -> None:
        self.customer_id = customer.id
        self.customer = customer
        self.pizzas = pizzas

    def to_json(self):
        return {
            'id': str(self.id),
            'customer_id': str(self.customer_id),
            'state': self.order_state.value,
            'pizzas': [pizza.to_json() for pizza in self.pizzas],
        }