from Field import Field


class IncomeTax(Field):
    def __init__(self, name, position_x, position_y, type, tax):
        super().__init__(name, position_x, position_y, type)
        self.tax = tax

    def get_tax(self):
        return self.tax
