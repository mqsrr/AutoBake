class Address:

    def __init__(self, id, street, post_code):
        self.id = id
        self.street = street
        self.post_code = post_code

    def to_json(self):
        return {
            'id': str(self.id),
            'street': self.street,
            'postcode': self.post_code,
        }