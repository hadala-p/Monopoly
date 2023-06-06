from Field import Field


class Estate(Field):
    def __init__(self, name, position_x, position_y, type, price, rent):
        super().__init__(name, position_x, position_y, type)
        self.price = price
        self.rent = rent
        self.owner = None

    def get_price(self):
        return self.price

    def get_rent(self):
        return self.rent

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner
