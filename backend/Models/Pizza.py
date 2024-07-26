import uuid
from typing import Any

from sqlalchemy import Column, UUID, ForeignKey, String, Integer
from sqlalchemy.orm import Relationship

from backend.database.database import Base


class Pizza(Base):
    __tablename__ = "pizzas"
    cooking_time = 10

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String(64), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=True, index=True)

    order = Relationship("Order", back_populates="pizzas", passive_deletes=True)

    def __init__(self, order_id: int, title: str, quantity: int):
        self.id = uuid.uuid4()
        self.order_id = order_id
        self.title = title
        self.quantity = quantity

    @staticmethod
    def pizza_decoder(pizza_dict: dict) -> Any | None:
        if 'title' in pizza_dict and 'quantity' in pizza_dict:
            return Pizza(0, pizza_dict['title'], pizza_dict['quantity'])
        return None

    def to_json(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'quantity': self.quantity,
        }
