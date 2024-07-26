from typing import Any

from frontend.Models.Address import Address


class Customer:

    def __init__(self, id, name, email, password, addresses):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
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
