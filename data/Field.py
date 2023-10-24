class Field:
    def __init__(self, name, position_x, position_y, type):
        self.name = name
        self.position_x = position_x
        self.position_y = position_y
        self.type = type

    def get_name(self):
        return self.name

    def get_coordinates(self):
        return self.position_x, self.position_y

    def get_type(self):
        return self.type
