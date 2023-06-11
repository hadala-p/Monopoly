from Field import Field


class Estate(Field):
    def __init__(self, name, position_x, position_y, type, price):
        super().__init__(name, position_x, position_y, type)
        self.price = price
        self.number_of_houses = 0
        self.rent = price // 10 + self.number_of_houses * (price // 4)
        self.house_price = self.number_of_houses * 20
        self.owner = None

    def get_price(self):
        return self.price

    def get_rent(self):
        return self.rent

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner

    def get_number_of_hauses(self):
        return self.number_of_houses

    def buy_home(self):
        self.number_of_houses += 1
