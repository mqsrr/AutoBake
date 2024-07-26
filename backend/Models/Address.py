import uuid
from typing import Any

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import Relationship

from backend.database.database import Base


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    street = Column(String(64), nullable=False)
    post_code = Column(String(64), nullable=False)
    customer_id = Column(ForeignKey('customers.id', ondelete='CASCADE'), nullable=True, index=True)

    customer = Relationship('Customer', back_populates='addresses', passive_deletes=True)

    def __init__(self, street, post_code):
        self.id = uuid.uuid4()
        self.street = street
        self.post_code = post_code

    def to_json(self):
        return {
            'id': str(self.id),
            'street': self.street,
            'postcode': self.post_code,
        }

    @staticmethod
    def address_decoder(address_dict: dict) -> Any | None:
        if 'street' in address_dict and 'postcode' in address_dict:
            return Address(address_dict['street'], address_dict['postcode'])
        return None
