from Field import Field


class RailRoad(Field):
    def __init__(self, name, position_x, position_y, type, price):
        super().__init__(name, position_x, position_y, type)
        self.price = price
        self.rent = 25
        self.owner = None
        self.value = price

    def get_price(self):
        return self.price

    def add_rent(self):
        self.rent += 25

    def get_rent(self):
        return self.rent

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner

    def get_value(self):
        return self.value
